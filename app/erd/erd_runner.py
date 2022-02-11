import copy
import queue
from collections import deque
from datetime import timedelta, datetime
from queue import Queue
from typing import List, Union

from app.erd.data_serializer import ErdDataSerializer
from app.erd.entities import ErdRqm, Erd, PositionCoordinates, ErdRqmStatus, empty_erd_rqm, empty_erd_status, \
    ActiveRecipe
from app.erd.erd_setup import ErdSetup, get_z_range
from hive_exception import HiveError, AbortedError
from threading import Thread, Lock
import time
import logging
from app.setup.config import GlobalConfig

env_config = GlobalConfig()
faker = env_config.FAKER


class ErdRunner(Thread):
    _rqms: List[ErdRqm]
    _past_rqms: deque[ErdRqm]
    _active_rqm: ErdRqm
    _failed_rqms: deque[ErdRqm]
    _status: ErdRqmStatus
    _erd_setup: ErdSetup
    _data_serializer: ErdDataSerializer
    _abort: bool
    _lock: Lock
    _error: Union[None, Exception]

    def __init__(self, erd_setup: ErdSetup, erd_data_serializer):
        Thread.__init__(self)
        self._lock = Lock()
        self._rqms = []
        self._active_rqm = empty_erd_rqm
        self._lock = Lock()
        self._erd_setup = erd_setup
        self._abort = False
        self._past_rqms = deque(maxlen=5)
        self._failed_rqms = deque(maxlen=5)
        self._status = empty_erd_status
        self._data_serializer = erd_data_serializer
        self._error = None

    def resume(self):
        with self._lock:
            self._abort = False

    def abort(self):
        with self._lock:
            self._abort = True

    def get_state(self):
        with self._lock:
            rqms = copy.deepcopy(self._rqms)
            past_rqms = copy.deepcopy(list(self._past_rqms))
            failed_rqms = copy.deepcopy(list(self._failed_rqms))
            active_rqm = self._active_rqm
        rbs_state = {"queue": rqms, "active_rqm": active_rqm, "done": past_rqms, "failed": failed_rqms}
        rbs_state.update(self._status.dict())
        return rbs_state

    def add_rqm_to_queue(self, rqm: ErdRqm):
        with self._lock:
            self._rqms.append(rqm)

    def _clear_rqms(self):
        with self._lock:
            self._rqms.clear()
            self._past_rqms.clear()

    def _pop_rqm(self):
        with self._lock:
            if self._rqms:
                return self._rqms.pop(0)
            else:
                return empty_erd_rqm

    def _set_active_rqm(self, rqm):
        with self._lock:
            self._active_rqm = rqm
            self._status.active_rqm_status = []
            if rqm != empty_erd_rqm:
                self._status.run_status = "Running"
            else:
                self._status.run_status = "Idle"

    def _should_abort(self):
        with self._lock:
            return copy.deepcopy(self._abort)

    def _clear_abort(self):
        with self._lock:
            self._abort = False


    '''
    for progress - this should come from the erd_setup and come directly from the mpa3 daemon. (run_time vs 
    run_time_target.) now there is a potential for >100% progress which is odd
    '''
    def _run_recipe(self, recipe: Erd):
        logging.info("\t[RQM] Recipe start: " + str(recipe))
        with self._lock:
            self._status.active_rqm_status.append(ActiveRecipe(recipe_id = recipe.file_stem,
                                                               run_time=timedelta(0),
                                                               run_time_target=recipe.measuring_time_sec))

        recipe_start_time = datetime.now()
        error_value = Queue()
        t = Thread(target=run_erd_recipe, args=(recipe, self._erd_setup, self._data_serializer, error_value))
        t.start()
        while t.is_alive():
            self._status.active_rqm_status[-1].run_time = datetime.now() - recipe_start_time
            time.sleep(1)
            if self._should_abort():
                self._erd_setup.abort()
        t.join()
        self._error = error_value.get()

    def _write_result(self, rqm):
        with self._lock:
            rqm_dict = rqm.dict()
            if self._error:
                rqm_dict["error_state"] = str(self._error)
                logging.error("[RQM] RQM Failure:'" + str(rqm) + "'")
                logging.error("[RQM] RQM Failed with error:'" + str(self._error) + "'")
                self._failed_rqms.appendleft(rqm_dict)
                self._error = None
            else:
                rqm_dict["error_state"] = "Done with no errors"
                logging.info("[RQM] RQM Done:'" + str(rqm) + "'")
                self._past_rqms.appendleft(rqm)
            self._data_serializer.save_rqm(rqm_dict)

    ''' Abort should be a model instead of a boolean, this allows more fine-grained abortion control'''
    def _handle_abort(self):
        if self._should_abort():
            logging.error("[RQM] Abort: Clearing Schedule")
            self._clear_rqms()
            self._clear_abort()
            self._erd_setup.resume()

    def run(self):
        while True:
            time.sleep(1)
            rqm = self._pop_rqm()
            self._set_active_rqm(rqm)
            if rqm != empty_erd_rqm:
                self._data_serializer.set_base_folder(rqm.rqm_number)
                logging.info("[RQM] RQM Start: '" + str(rqm) + "'")
                for recipe in rqm.recipes:
                    self._run_recipe(recipe)
                    if self._should_abort():
                        self._error = AbortedError("Aborted RQM")
                        break
                self._write_result(rqm)
            self._handle_abort()


def run_erd_recipe(recipe: Erd, erd_setup: ErdSetup, erd_data_serializer: ErdDataSerializer, error: Queue):
    error_value = None
    try:
        erd_setup.move(PositionCoordinates(z=recipe.z_start, theta=recipe.theta))
        erd_setup.wait_for_arrival()
        erd_setup.configure_acquisition(recipe.measuring_time_sec, recipe.file_stem)
        erd_setup.start_acquisition()
        erd_setup.wait_for_acquisition_started()
        z_range = get_z_range(recipe.z_start, recipe.z_end, recipe.z_increment)
        wait_time = recipe.measuring_time_sec / len(z_range)
        logging.info("testing positions: " + str(z_range) + "wait_time_sec between steps: " + str(
            wait_time) + ", total measurement time: " + str(recipe.measuring_time_sec))
        for z in z_range:
            erd_setup.move(z)
            erd_setup.wait_for(wait_time)

        erd_setup.wait_for_acquisition_done()
        erd_data_serializer.save_histogram(erd_setup.get_histogram(), recipe.file_stem)
    except HiveError as e:
        error_value = e
    error.put(error_value)


