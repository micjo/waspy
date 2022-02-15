import copy
from collections import deque
from datetime import timedelta, datetime
from shutil import copy2
import logging
from typing import List, Union

from app.rbs.data_serializer import RbsDataSerializer
from app.rbs.entities import RbsRqm, empty_rbs_rqm, RbsRqmStatus, empty_rqm_status, \
    StatusModel, RecipeType, RbsRqmRandom, RbsRqmChanneling, ActiveRecipe
from app.rbs.recipe_list_runner import RecipeListRunner
from threading import Thread, Lock
import traceback
import time
import app.rbs.rbs_setup as rbs_lib
from hive_exception import AbortedError
from app.setup.config import GlobalConfig

env_config = GlobalConfig()
faker = env_config.FAKER


class RbsRunner(Thread):
    _rqms: List[RbsRqm]
    _past_rqms: deque[RbsRqm]
    _active_rqm: RbsRqm
    _status: RbsRqmStatus
    _data_serializer: RbsDataSerializer
    _rbs: rbs_lib.RbsSetup
    _abort: bool
    _lock: Lock
    _error: Union[None, Exception]

    def __init__(self, recipe_runner: RecipeListRunner, data_serializer: RbsDataSerializer, rbs: rbs_lib.RbsSetup):
        Thread.__init__(self)
        self.recipe_runner = recipe_runner
        self._rqms = []
        self._active_rqm = empty_rbs_rqm
        self._status = empty_rqm_status
        self._data_serializer = data_serializer
        self._rbs = rbs
        self._lock = Lock()
        self._abort = False
        self._past_rqms = deque(maxlen=5)
        self._failed_rqms = deque(maxlen=5)
        self._error = None

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

    def add_rqm_to_queue(self, rqm: RbsRqm):
        with self._lock:
            self._rqms.append(rqm)

    def run(self):
        while True:
            time.sleep(1)
            rqm = self._pop_rqm()
            self._set_active_rqm(rqm)
            if rqm != empty_rbs_rqm:
                self._data_serializer.set_base_folder(rqm.rqm_number)
                self._rbs.set_active_detectors(rqm.detectors)
                logging.info("[RQM] RQM Start: '" + str(rqm) + "'")
                for recipe in rqm.recipes:
                    self._run_recipe(recipe)
                    if self._should_abort():
                        self._error = AbortedError("Aborted RQM")
                        break
                self._write_result(rqm)
            self._handle_abort()

    def abort_scheduled_rqm(self, rqm_number:str):
        with self._lock:
            for rqm in self._rqms:
                if rqm.rqm_number == rqm_number:
                    self._rqms.remove(rqm)

    def _clear_rqms(self):
        with self._lock:
            self._rqms.clear()
            self._past_rqms.clear()

    def _pop_rqm(self):
        with self._lock:
            if self._rqms:
                return self._rqms.pop(0)
            else:
                return empty_rbs_rqm

    def _set_active_rqm(self, rqm):
        with self._lock:
            self._active_rqm = rqm
            self._status.active_rqm_status = []
            if rqm != empty_rbs_rqm:
                self._status.run_status = StatusModel.Running
            else:
                self._status.run_status = StatusModel.Idle

    def _should_abort(self):
        with self._lock:
            return copy.deepcopy(self._abort)

    def _clear_abort(self):
        with self._lock:
            self._abort = False

    def _run_recipe(self, recipe: Union[RbsRqmRandom, RbsRqmChanneling]):
        logging.info("\t[RQM] Recipe start: " + str(recipe))
        with self._lock:
            self._rbs.charge_offset = 0
            self._status.active_rqm_status.append(ActiveRecipe(recipe_id=recipe.file_stem,
                                                               run_time=timedelta(0),
                                                               accumulated_charge_corrected=0,
                                                               accumulated_charge_target=_get_total_counts(recipe)))
        recipe_start_time = datetime.now()
        t = Thread(target=self.recipe_runner.run_recipe, args=(recipe, self._rbs, self._data_serializer))
        t.start()
        while t.is_alive():
            self._update_charge_status()
            with self._lock:
                self._status.active_rqm_status[-1].run_time = datetime.now() - recipe_start_time

            time.sleep(0.5)
            if self._should_abort():
                if not self._rbs.aborted():
                    self._rbs.abort()
                if not self._data_serializer.aborted():
                    self._data_serializer.abort()
        t.join()
        self._error = self.recipe_runner.error
        self.recipe_runner.error = None

    def _update_charge_status(self):
        with self._lock:
            if faker:
                self._status.active_rqm_status[-1].accumulated_charge_corrected += 10
            else:
                self._status.active_rqm_status[-1].accumulated_charge_corrected = \
                    self._rbs.get_corrected_total_accumulated_charge()

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
                rqm_dict["error_state"] = "[RQM] Done with no errors"
                logging.info("[RQM] RQM Done:'" + str(rqm) + "'")
                self._past_rqms.appendleft(rqm)
            self._data_serializer.save_rqm(rqm_dict)

    def _handle_abort(self):
        if self._should_abort():
            logging.error("[RQM] Abort: Clearing Schedule")
            self._clear_rqms()
            self._clear_abort()
            self._rbs.resume()
            self._data_serializer.resume()



def _pick_first_file_from_path(path):
    files = [file for file in sorted(path.iterdir()) if file.is_file()]
    try:
        return files[0]
    except:
        return ""


def move_and_try_copy(file, move_folder, copy_folder):
    file.replace(move_folder / file.name)
    file = move_folder / file.name
    try:
        copy2(file, copy_folder)
    except:
        logging.error(traceback.format_exc())
    return file


def _get_total_counts_random(recipe: RbsRqmRandom):
    return recipe.charge_total


def _get_total_counts_channeling(recipe: RbsRqmChanneling):
    yield_optimize_total_charge = recipe.yield_charge_total * len(recipe.yield_vary_coordinates)
    compare_total_charge = 2 * recipe.random_fixed_charge_total
    return yield_optimize_total_charge + compare_total_charge


def _get_total_counts(recipe: Union[RbsRqmRandom, RbsRqmChanneling]):
    if recipe.type == RecipeType.channeling:
        return _get_total_counts_channeling(recipe)
    if recipe.type == RecipeType.random:
        return _get_total_counts_random(recipe)
