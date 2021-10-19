import threading
import time
from typing import List
import copy

from app.rbs_experiment.entities import RbsRqmSettings, RbsRqmStatus, RbsRqmRandom, RbsRqmChanneling, \
    RbsRqmMinimizeYield, RbsRqmFixed, RecipeType, PositionCoordinates, StatusModel, empty_rbs_rqm, RbsRqm, \
    empty_settings
import app.rbs_experiment.rbs as rbs_lib
import app.rbs_experiment.yield_plot as plot


#use this function to potentially exit the thread
def make_count_callback(rbs_rqm_status: RbsRqmStatus):
    counts_at_start = rbs_rqm_status.accumulated_charge

    def count_callback(counter_data):
        charge = float(counter_data["charge(nC)"])
        target_charge = float(counter_data["target_charge(nC)"])
        if charge < target_charge:
            rbs_rqm_status.accumulated_charge = counts_at_start + charge
        else:
            rbs_rqm_status.accumulated_charge = counts_at_start + target_charge

    return count_callback


def _make_minimize_yield_recipe(index, recipe, vary_coordinate):
    return RbsRqmMinimizeYield(type=RecipeType.minimize_yield, sample_id=recipe.sample_id,
                               file_stem=recipe.file_stem + str(index),
                               total_charge=recipe.yield_charge_total,
                               vary_coordinate=vary_coordinate, integration_window=
                               recipe.yield_integration_window,
                               optimize_detector_index=recipe.yield_optimize_detector_index)


def _make_fixed_recipe(recipe):
    return RbsRqmFixed(type=RecipeType.fixed, sample_id=recipe.sample_id,
                       file_stem=recipe.file_stem + "_fixed",
                       charge_total=recipe.random_fixed_charge_total)


def _make_random_recipe(recipe):
    return RbsRqmRandom(type=RecipeType.random, sample_id=recipe.sample_id,
                        file_stem=recipe.file_stem + "_random",
                        charge_total=recipe.random_fixed_charge_total,
                        start_position={"theta": -2},
                        vary_coordinate=recipe.random_vary_coordinate)


def _get_total_counts_random(recipe: RbsRqmRandom):
    return recipe.charge_total


def _get_total_counts_channeling(recipe: RbsRqmChanneling):
    yield_optimize_total_charge = recipe.yield_charge_total * len(recipe.yield_vary_coordinates)
    compare_total_charge = 2 * recipe.random_fixed_charge_total
    return yield_optimize_total_charge + compare_total_charge


class RecipeListRunner:
    _rbs: rbs_lib.Rbs
    _rqm: RbsRqm
    _status: RbsRqmStatus
    _status_lock: threading.Lock()

    def __init__(self, setup: rbs_lib.Rbs):
        self._rbs = setup
        self._rqm = empty_rbs_rqm
        self._status = RbsRqmStatus(run_status=StatusModel.Idle, active_recipe="", accumulated_charge=0, accumulated_charge_target=0)

    def __setattr__(self, name, value):
        """Makes setting status thread-safe"""
        print("setattr")
        if name == "_status":
            print("locked in set _status")
            with self.lock:
                super().__setattr__(name, value)
        else:
            super().__setattr__(name, value)

    def __getattribute__(self, name):
        """Makes getting status thread-safe"""
        print("getattr")
        if name == "_status":
            with self.lock:
                print("locked in get _status")
                return object.__getattribute__(self, name)
        else:
            return object.__getattribute__(self, name)

    def _minimize_yield(self, recipe: RbsRqmMinimizeYield):
        self._rbs.move(recipe.start_position)
        positions = rbs_lib.get_position_range(recipe.vary_coordinate)
        self._rbs.prepare_counting(recipe.total_charge / len(positions))

        detector_optimize = self._rqm.settings.detectors[recipe.optimize_detector_index]
        energy_yields = []

        for position in positions:
            start = time.time()
            self._rbs.prepare_data_acquisition()
            self._rbs.move_and_count(position, make_count_callback(self._status))
            data = self._rbs.get_packed_histogram(detector_optimize)
            integrated_energy_yield = rbs_lib.get_sum(data, recipe.integration_window)
            energy_yields.append(integrated_energy_yield)
            run_time = time.time() - start
            file_stem = recipe.file_stem + "_" + rbs_lib.single_coordinate_to_string(position, recipe.vary_coordinate)
            total_charge = self._rbs.get_charge()
            self._rbs.flush_histograms(self._rqm.settings, recipe.sample_id, file_stem, run_time, total_charge)

        min_position = rbs_lib.get_minimum_yield_position(self._rqm.settings.rqm_number, recipe, positions, energy_yields)
        self._rbs.move(min_position)

    def run_random(self, recipe: RbsRqmRandom):
        self._rbs.move(recipe.start_position)
        positions = rbs_lib.get_position_range(recipe.vary_coordinate)
        self._rbs.prepare_counting(recipe.charge_total / len(positions))
        self._rbs.prepare_data_acquisition()

        start = time.time()

        total_charge = 0
        for index, position in enumerate(positions):
            self._rbs.move_and_count(position, make_count_callback(self._status))
            total_charge += self._rbs.get_charge()

        end = time.time()
        run_time = end - start
        random_histograms = self._rbs.flush_histograms(self._rqm.settings, recipe.sample_id, recipe.file_stem, run_time,
                                                       total_charge)
        self._rbs.stop_data_acquisition()
        return random_histograms

    def run_fixed(self, recipe: RbsRqmFixed):
        start = time.time()
        self._rbs.prepare_counting(recipe.charge_total)
        self._rbs.prepare_data_acquisition()

        self._rbs.count(make_count_callback(self._status))
        end = time.time()
        run_time = end - start

        total_charge = self._rbs.get_charge()
        fixed_histograms = self._rbs.flush_histograms(self._rqm.settings, recipe.sample_id, recipe.file_stem, run_time,
                                                      total_charge)
        return fixed_histograms

    def run_channeling(self, recipe: RbsRqmChanneling):
        self._rbs.move(recipe.start_position)

        for index, vary_coordinate in enumerate(recipe.yield_vary_coordinates):
            yield_recipe = _make_minimize_yield_recipe(index, recipe, vary_coordinate)
            self._rqm.settings.sub_folder = recipe.file_stem + "_" + str(index) + "_vary_" + str(vary_coordinate.name)
            self._minimize_yield(yield_recipe)
        self._rqm.settings.sub_folder = ""

        fixed_histograms = self.run_fixed(_make_fixed_recipe(recipe))
        random_histograms = self.run_random(_make_random_recipe(recipe))

        plot.plot_compare(self._rqm.settings, recipe.file_stem, fixed_histograms, random_histograms)

    def run_rqm(self, rbs_rqm: RbsRqm):
        self._status.run_status = StatusModel.Running
        self._rqm = rbs_rqm

        for recipe in rbs_rqm.recipes:
            self._status.accumulated_charge = 0
            self._status.accumulated_charge_target = 0
            self._status.active_recipe = recipe.sample_id

            if recipe.type == RecipeType.channeling:
                self._status.accumulated_charge_target = _get_total_counts_channeling(recipe)
                self.run_channeling(recipe)
            if recipe.type == RecipeType.random:
                self._status.accumulated_charge_target = _get_total_counts_random(recipe)
                self.run_random(recipe)

        self._status.run_status = StatusModel.Idle
        self._status.active_recipe = ""
        self._status.accumulated_charge = 0
        self._status.accumulated_charge_target = 0
