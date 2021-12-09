import copy
import queue
from collections import deque
from queue import Queue
from typing import List, Union

from app.erd.entities import ErdRqm, Erd, PositionCoordinates, ErdRqmStatus, empty_erd_rqm
from app.erd.erd_setup import ErdSetup, get_z_range
from hive_exception import HiveError
from threading import Thread, Lock
import time
import logging


def run_erd_recipe(recipe: Erd, erd_setup: ErdSetup, error: Queue):
    errored = None
    try:
        erd_setup.move(PositionCoordinates(z=recipe.z_start, theta=recipe.theta))
        erd_setup.wait_for_arrival()
        erd_setup.configure_acquisition(recipe.measuring_time_sec, recipe.file_stem)
        erd_setup.start_acquisition()
        erd_setup.wait_for_acquisition_started()
        z_range = get_z_range(recipe.z_start, recipe.z_end, recipe.z_increment)
        wait_time = recipe.measuring_time_sec/len(z_range)
        logging.info("positions: " + str(z_range) + "wait_time_sec between steps: " + str(wait_time) + ", total measurement time: " + str(recipe.measuring_time_sec))
        for z in z_range:
            erd_setup.move(z)
            time.sleep(recipe.measuring_time_sec/len(z_range))
        erd_setup.wait_for_acquisition_done()
    except HiveError as e:
        errored = e
    error.put(errored)


class ErdRunner(Thread):
    _rqms: List[ErdRqm]
    _past_rqms: deque[ErdRqm]
    _active_rqm: ErdRqm
    _failed_rqms: deque[ErdRqm]
    _status: ErdRqmStatus
    _erd_setup: ErdSetup
    _abort: bool
    _lock: Lock
    _error: Union[None, Exception]

    def __init__(self, erd_setup: ErdSetup):
        Thread.__init__(self)
        self._lock = Lock()
        self.rqms = []
        self._active_rqm = empty_erd_rqm
        self._lock = Lock()
        self._erd_setup = erd_setup
        self._abort = False
        self._past_rqms = deque(maxlen=5)
        self._failed_rqms = deque(maxlen=5)

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
            self._status.active_sample_id = ""
            self._status.run_time = 0
            self._status.run_time_target = 0
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

    def _run_recipe(self, recipe: Erd):
        logging.info("\t[RQM] Recipe start: " + str(recipe))
        with self._lock:
            self._status.active_sample_id = recipe.sample_id
            self._status.run_time_target = recipe.measuring_time_sec

        error_value = Queue()
        t = Thread(target=run_erd_recipe, args=(recipe, self._erd_setup, error_value))
        t.start()
        while t.is_alive():
            time.sleep(1)
            self._status.run_time += 1
            if self._should_abort():
                self._erd_setup.abort()
        self._error = error_value.get()

    def _write_result(self, rqm):
        with self._lock:
            rqm_dict = rqm.dict()
            if self._should_abort():
                rqm_dict["failure"] = "RQM '" + str(rqm.rqm_number) + "' aborted"
                logging.error("[RQM] RQM Abort: '" + str(rqm) + "'")
            elif self._error:
                rqm_dict["failure"] = str(self._error)
                logging.error("[RQM] RQM Failure:'" + str(rqm) + "'")
                self._failed_rqms.appendleft(rqm_dict)
                self._error = None
            else:
                rqm_dict["failure"] = "[RQM] Done:'" + str(rqm) + "'"
                logging.info("[RQM] RQM Done:'" + str(rqm) + "'")
                self._past_rqms.appendleft(rqm)

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
                logging.info("[RQM] RQM Start: '" + str(rqm) + "'")
                for recipe in rqm.recipes:
                    self._run_recipe(recipe)
                    if self._should_abort():
                        break
                self._write_result(rqm)
            self._handle_abort()
