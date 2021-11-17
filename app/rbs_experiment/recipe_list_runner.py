import sys
import time
import traceback
from typing import List, Union, Callable
import copy

from app.rbs_experiment.data_serializer import RbsDataSerializer
from app.rbs_experiment.entities import RbsRqmStatus, RbsRqmRandom, RbsRqmChanneling, \
    RbsRqmMinimizeYield, RbsRqmFixed, RecipeType, StatusModel, RbsRqm, RbsData, VaryCoordinate, \
    CoordinateEnum, PositionCoordinates, empty_rqm_status
import app.rbs_experiment.rbs as rbs_lib
from threading import Thread, Lock
from queue import Queue
import app.rbs_experiment.yield_angle_fit as fit
from functools import partial
from hive_exception import HiveError as HiveError


def make_count_callback(rbs_rqm_status: RbsRqmStatus):
    counts_at_start = rbs_rqm_status.accumulated_charge

    def count_callback(counter_data):
        charge = float(counter_data["charge(nC)"])
        target_charge = float(counter_data["target_charge(nC)"])
        if charge < target_charge:
            rbs_rqm_status.accumulated_charge = counts_at_start + charge
        else:
            rbs_rqm_status.accumulated_charge = counts_at_start + target_charge

        return False

    return count_callback


def _make_minimize_yield_recipe(recipe, vary_coordinate):
    return RbsRqmMinimizeYield(type=RecipeType.minimize_yield, sample_id=recipe.sample_id,
                               file_stem=recipe.file_stem,
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


def _get_minimum_yield_angle(angles: List[float], energy_yields: List[int]) -> float:
    min_angle = fit.get_angle_for_minimum_yield(angles, energy_yields)
    return min_angle


class RecipeListRunner():
    rqm_queue: Queue[RbsRqm]
    _active_rqm: RbsRqm
    _status: RbsRqmStatus
    _data_serializer: RbsDataSerializer
    _rbs: rbs_lib.Rbs
    error: Union[None, Exception]

    def __init__(self, setup: rbs_lib.Rbs, data_serializer: RbsDataSerializer):
        self._rbs = setup
        self._data_serializer = data_serializer
        self._status = empty_rqm_status
        self.error = None

    def _get_count_callback(self):
        counts_at_start = self._status.accumulated_charge

        def count_callback(counter_data):
            charge = float(counter_data["charge(nC)"])
            target_charge = float(counter_data["target_charge(nC)"])
            if charge < target_charge:
                self._status.accumulated_charge = counts_at_start + charge
            else:
                self._status.accumulated_charge = counts_at_start + target_charge
        return count_callback

    def _minimize_yield(self, recipe: RbsRqmMinimizeYield, rbs: rbs_lib.Rbs, data_serializer: RbsDataSerializer):
        rbs.move(recipe.start_position)
        positions = rbs_lib.get_positions_as_coordinate(recipe.vary_coordinate)
        rbs.prepare_counting(recipe.total_charge / len(positions))

        detector_optimize = rbs.get_detectors()[recipe.optimize_detector_index]
        energy_yields = []

        for position in positions:
            rbs.prepare_data_acquisition()
            rbs.move_and_count(position)
            rbs.stop_data_acquisition()

            data = rbs.get_packed_histogram(detector_optimize)
            integrated_energy_yield = rbs_lib.get_sum(data, recipe.integration_window)
            energy_yields.append(integrated_energy_yield)

            rbs_data = rbs.get_status(True)
            file_stem = recipe.file_stem + "_" + rbs_lib.single_coordinate_to_string(position, recipe.vary_coordinate)
            data_serializer.save_histograms(rbs_data, file_stem, recipe.sample_id)
            data_serializer.plot_histograms(rbs_data, file_stem)

        angles = rbs_lib.get_positions_as_float(recipe.vary_coordinate)
        smooth_angles, smooth_yields = fit.fit_and_smooth(angles, energy_yields)
        min_angle = fit.get_angle_for_minimum_yield(smooth_angles, smooth_yields)
        min_position = rbs_lib.convert_float_to_coordinate(recipe.vary_coordinate.name, min_angle)

        data_serializer.store_yields(recipe.file_stem, angles, energy_yields)
        data_serializer.plot_energy_yields(recipe.file_stem, angles, energy_yields, smooth_angles, smooth_yields)
        rbs.move(min_position)

    def run_random(self, recipe: RbsRqmRandom, rbs: rbs_lib.Rbs, data_serializer: RbsDataSerializer, clear_offset=True):
        if clear_offset:
            rbs.clear_total_accumulated_charge()
        rbs.move(recipe.start_position)
        positions = rbs_lib.get_positions_as_coordinate(recipe.vary_coordinate)
        rbs.prepare_counting(recipe.charge_total / len(positions))
        rbs.prepare_data_acquisition()

        for index, position in enumerate(positions):
            rbs.move_and_count(position)
        rbs.stop_data_acquisition()

        rbs_data = rbs.get_status(True)
        data_serializer.save_histograms(rbs_data, recipe.file_stem, recipe.sample_id)
        data_serializer.plot_histograms(rbs_data, recipe.file_stem)
        return rbs_data

    def configure_store(self, rqm: RbsRqm):
        self._data_serializer.set_base_folder(rqm.rqm_number)
        self._rbs.set_active_detectors(rqm.detectors)

    def run_fixed(self, recipe: RbsRqmFixed, rbs: rbs_lib.Rbs, data_serializer: RbsDataSerializer) -> RbsData:
        rbs.prepare_counting(recipe.charge_total)
        rbs.prepare_data_acquisition()
        rbs.count()
        rbs.stop_data_acquisition()

        rbs_data = rbs.get_status(True)
        data_serializer.save_histograms(rbs_data, recipe.file_stem, recipe.sample_id)
        data_serializer.plot_histograms(rbs_data, recipe.file_stem)
        return rbs_data

    def run_channeling(self, recipe: RbsRqmChanneling, rbs: rbs_lib.Rbs, data_serializer: RbsDataSerializer):
        rbs.clear_total_accumulated_charge()
        rbs.move(recipe.start_position)

        for index, vary_coordinate in enumerate(recipe.yield_vary_coordinates):
            yield_recipe = _make_minimize_yield_recipe(recipe, vary_coordinate)
            yield_recipe.file_stem = recipe.file_stem + "_" + str(index) + "_vary_" + str(vary_coordinate.name)
            data_serializer.set_sub_folder(recipe.file_stem + "_" + str(index) + "_vary_" + str(vary_coordinate.name))
            self._minimize_yield(yield_recipe, rbs, data_serializer)
        data_serializer.clear_sub_folder()

        fixed_histograms = self.run_fixed(_make_fixed_recipe(recipe), rbs, data_serializer).histograms
        random_histograms = self.run_random(_make_random_recipe(recipe), rbs, data_serializer, False).histograms
        detectors = rbs.get_detectors()
        data_serializer.plot_compare(detectors, fixed_histograms, random_histograms, recipe.file_stem)

    def run_recipe(self, recipe: Union[RbsRqmRandom, RbsRqmChanneling], rbs: rbs_lib.Rbs, data_serializer: RbsDataSerializer):
        try:
            if recipe.type == RecipeType.random:
                self.run_random(recipe, rbs, data_serializer)
            if recipe.type == RecipeType.channeling:
                self.run_channeling(recipe, rbs, data_serializer)
        except HiveError as e:
            self.error = e
