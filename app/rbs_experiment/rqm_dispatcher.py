import copy
import queue
import sys
from pathlib import Path
from queue import Queue
from shutil import copy2
import logging
from typing import List, Union

from app.rbs_experiment.data_serializer import RbsDataSerializer
from app.rbs_experiment.entities import RbsRqm, DispatcherConfig, empty_rbs_rqm, RbsRqmStatus, empty_rqm_status, \
    StatusModel, RecipeType, RbsRqmRandom, RbsRqmChanneling
from app.rbs_experiment.recipe_list_runner import RecipeListRunner
from threading import Thread, Lock, Condition
import traceback
import time
import app.rbs_experiment.rbs as rbs_lib


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
    _active_rqm: RbsRqm
    _status: RbsRqmStatus
    _data_serializer: RbsDataSerializer
    _rbs: rbs_lib.Rbs
    _abort: bool
    _lock: Lock

    def __init__(self, recipe_runner: RecipeListRunner, data_serializer:RbsDataSerializer, rbs: rbs_lib.Rbs):
        Thread.__init__(self)
        self.recipe_runner = recipe_runner
        self.pause_condition = Condition()
        self.enqueue_rqm = Condition()
        self._status_lock = Lock()
        self._rqms = []
        self._active_rqm = empty_rbs_rqm
        self._status = empty_rqm_status
        self._data_serializer = data_serializer
        self._rbs = rbs
        self._lock = Lock()
        self._abort = False

    def abort(self):
        with self._lock:
            self._abort = True

    def get_state(self):
        with self.enqueue_rqm:
            rqms = copy.deepcopy(self._rqms)
            active_rqm = self._active_rqm
        rbs_state = {"queue": rqms, "active_rqm": active_rqm, "status": self._status}
        return rbs_state

    def rqm_start(self):
        with self._status_lock:
            self._status.run_status = StatusModel.Running

    def rqm_end(self):
        with self._status_lock:
            self._status.run_status = StatusModel.Idle
            self._status.active_recipe_sample_id = ""
            self._status.accumulated_charge = 0

    def add_rqm_to_queue(self, rqm):
        with self.enqueue_rqm:
            self._rqms.append(rqm)

#TODO: This function needs (a lot of) cleanup
    def run_recipe(self, recipe: Union[RbsRqmRandom, RbsRqmChanneling]):
        with self._status_lock:
            self._status.active_recipe_sample_id = recipe.sample_id
            self._status.accumulated_charge_target = _get_total_counts(recipe)
            counts_at_start = self._status.accumulated_charge_target

        command_list = []
        if recipe.type == RecipeType.random:
            command_list = self.recipe_runner.run_random(recipe, self._rbs, self._data_serializer)

        for command in command_list:
            t = Thread(target=command)
            t.start()
            while t.is_alive():
                with self._lock:
                    if self._abort:
                        break
                charge = self._rbs.get_charge()
                target_charge = self._rbs.get_target_charge()
                logging.info("thread still alive, charge: " + str(charge) + "target_charge:" + str(target_charge))
                with self._status_lock:
                    if charge < target_charge:
                        self._status.accumulated_charge = counts_at_start + charge
                    else:
                        self._status.accumulated_charge = counts_at_start + target_charge
                time.sleep(1)
            with self._lock:
                if self._abort:
                    self._abort = False
                    break

        command_list.clear()


    def run(self):
        while True:
            time.sleep(1)
            if not self._rqms:
                continue
            with self.enqueue_rqm:
                active_rqm = self._rqms.pop(0)
                self._active_rqm = active_rqm

            self._data_serializer.set_base_folder(active_rqm.rqm_number)
            self._rbs.set_active_detectors(active_rqm.detectors)

            for recipe in active_rqm.recipes:
                self.run_recipe(recipe)
