import copy
from collections import deque
from shutil import copy2
import logging
from typing import List, Union

from app.rbs.data_serializer import RbsDataSerializer
from app.rbs.entities import RbsRqm, empty_rbs_rqm, RbsRqmStatus, empty_rqm_status, \
    StatusModel, RecipeType, RbsRqmRandom, RbsRqmChanneling
from app.rbs.recipe_list_runner import RecipeListRunner
from threading import Thread, Lock
import traceback
import time
import app.rbs.rbs_setup as rbs_lib


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


class RqmDispatcher(Thread):
    _rqms: List[RbsRqm]
    _past_rqms: deque[RbsRqm]
    _active_rqm: RbsRqm
    _status: RbsRqmStatus
    _data_serializer: RbsDataSerializer
    _rbs: rbs_lib.RbsSetup
    _abort: bool
    _lock: Lock

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
            self._status.active_sample_id = ""
            self._status.accumulated_charge = 0
            self._status.accumulated_charge_target = 0
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
        with self._lock:
            self._status.active_sample_id = recipe.sample_id
            self._status.accumulated_charge_target = _get_total_counts(recipe)
            self._rbs.charge_offset = 0

        t = Thread(target=self.recipe_runner.run_recipe, args=(recipe, self._rbs, self._data_serializer))
        t.start()
        while t.is_alive():
            self._update_charge_status()
            time.sleep(0.5)
            if self._should_abort():
                if not self._rbs.aborted():
                    self._rbs.abort()
                if not self._data_serializer.aborted():
                    self._data_serializer.abort()

    def _update_charge_status(self):
        with self._lock:
            self._status.accumulated_charge = self._rbs.get_corrected_total_accumulated_charge()

    def run(self):
        while True:
            time.sleep(1)
            rqm = self._pop_rqm()
            self._set_active_rqm(rqm)
            if rqm != empty_rbs_rqm:
                self._data_serializer.set_base_folder(rqm.rqm_number)
                self._rbs.set_active_detectors(rqm.detectors)
                for recipe in rqm.recipes:
                    self._run_recipe(recipe)
                    if self._should_abort():
                        break
                with self._lock:
                    if self.recipe_runner.error:
                        rqm_dict = rqm.dict()
                        rqm_dict["failure"] = str(self.recipe_runner.error)
                        logging.error("RQM '" + str(rqm.rqm_number) +
                                      "' failed with message: " + str(self.recipe_runner.error))
                        self._failed_rqms.appendleft(rqm_dict)
                        self.recipe_runner.error = None
                        self._data_serializer.save_rqm(rqm_dict)
                    else:
                        self._past_rqms.appendleft(rqm)
                        rqm_dict = rqm.dict()
                        rqm_dict["failure"] = "RQM '" + str(rqm.rqm_number) + "' passed without failure."
                        self._data_serializer.save_rqm(rqm_dict)

            if self._should_abort():
                self._clear_rqms()
                self._clear_abort()
                self._rbs.resume()
                self._data_serializer.resume()

            if self.recipe_runner.error:
                print("RQM Failed with error: " + str(self.recipe_runner.error))
                self.recipe_runner.error = None