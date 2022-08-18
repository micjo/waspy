import logging
import copy
from datetime import datetime, timedelta
from typing import List, Union

from pydantic import BaseModel

import hive.rbs_yield_angle_fit as fit
from waspy.hardware_control.hive_exception import AbortedError
from waspy.hardware_control.rbs_entities import RbsData, PositionCoordinates

from hive.rbs_data_serializer import RbsDataSerializer
from hive.rbs_entities import RbsJobModel, RecipeType, RbsStepwise, RbsChanneling, RbsSingleStep, RbsStepwiseLeast, \
    VaryCoordinate, Window
from waspy.hardware_control.rbs_setup import RbsSetup
from hive.job import Job
import numpy as np


class RbsRecipeStatus(BaseModel):
    name: str
    start_time: datetime
    run_time: timedelta
    accumulated_charge_corrected: float
    accumulated_charge_target: float
    progress: str
    sample: str


empty_rbs_recipe_status = RbsRecipeStatus(name="", sample="", start_time=datetime.now(), run_time=0,
                                          accumulated_charge_corrected=0,
                                          accumulated_charge_target=0, progress="0.0%")


class RbsJob(Job):
    _data_serializer: RbsDataSerializer
    _rbs_setup: RbsSetup
    _job_model: RbsJobModel
    _active_recipe_status: RbsRecipeStatus
    _finished_recipes: List[RbsRecipeStatus]
    _aborted: bool
    _running: bool

    def __init__(self, job_model: RbsJobModel, rbs_setup: RbsSetup, data_serializer: RbsDataSerializer):
        self._rbs_setup = rbs_setup
        self._data_serializer = data_serializer
        self._job_model = job_model
        self._run_time = timedelta(0)
        self._active_recipe_status = copy.deepcopy(empty_rbs_recipe_status)
        self._finished_recipes = []
        self._aborted = False
        self._running = False

    def setup(self):
        self._data_serializer.prepare_job(self._job_model)
        self._rbs_setup.clear_charge_offset()

    def exec(self):
        """ Can raise: AbortedError, HardwareError"""
        for recipe in self._job_model.recipes:
            self._run_recipe(recipe)
            self._finish_recipe()

    def teardown(self):
        self._data_serializer.finalize_job(self._job_model, self.serialize())
        self._rbs_setup.finish()

    def terminate(self, message: str) -> None:
        self._data_serializer.terminate_job(self._job_model.name, message)

    def serialize(self):
        self._update_active_recipe()
        finished_recipes = [recipe.dict() for recipe in self._finished_recipes]
        status = {"job": self._job_model.dict(), "active_recipe": self._active_recipe_status.dict(),
                  "finished_recipes": finished_recipes}
        return status

    def abort(self):
        logging.info("[RBS] Recipe" + str(self._active_recipe_status) + "aborted")
        self._aborted = True
        self._rbs_setup.abort()
        self._data_serializer.abort()

    def _update_active_recipe(self):
        """ Can raise: HardwareError"""
        if self._running:
            self._active_recipe_status.run_time = datetime.now() - self._active_recipe_status.start_time
            self._active_recipe_status.accumulated_charge_corrected = self._rbs_setup.get_corrected_total_accumulated_charge()
            active_recipe = self._active_recipe_status

            if active_recipe.accumulated_charge_target != 0:
                progress = active_recipe.accumulated_charge_corrected / active_recipe.accumulated_charge_target * 100
            else:
                progress = 0
            self._active_recipe_status.progress = "{:.2f}".format(progress)

    def _run_recipe(self, recipe):
        if self._aborted:
            raise AbortedError("Job Terminated")

        self._rbs_setup.charge_offset = 0
        self._active_recipe_status.start_time = datetime.now()
        self._active_recipe_status.name = recipe.name
        self._active_recipe_status.accumulated_charge_target = _get_total_counts(recipe)
        self._running = True
        if recipe.type == RecipeType.RANDOM:
            run_random(recipe, self._rbs_setup, self._data_serializer)
        if recipe.type == RecipeType.CHANNELING:
            run_channeling(recipe, self._rbs_setup, self._data_serializer)
        self._running = True

    def _finish_recipe(self):
        self._update_active_recipe()
        self._finished_recipes.append(copy.deepcopy(self._active_recipe_status))
        self._active_recipe_status = copy.deepcopy(empty_rbs_recipe_status)


def run_random(recipe: RbsStepwise, rbs: RbsSetup, data_serializer: RbsDataSerializer):
    start_time = datetime.now()
    rbs.move(recipe.start_position)
    positions = get_positions_as_coordinate(recipe.vary_coordinate)
    rbs.prepare_counting_with_target(recipe.charge_total / len(positions))
    rbs.start_data_acquisition()

    for index, position in enumerate(positions):
        rbs.move_and_count(position)
    rbs.stop_data_acquisition()

    rbs_data = rbs.get_status(True)
    data_serializer.save_histograms(rbs_data, recipe.name, recipe.sample)
    data_serializer.plot_histograms(rbs_data, recipe.name)
    data_serializer.stepwise_finish(recipe, start_time)
    return rbs_data


def run_channeling(recipe: RbsChanneling, rbs: RbsSetup, data_serializer: RbsDataSerializer):
    rbs.move(recipe.start_position)

    for index, vary_coordinate in enumerate(recipe.yield_vary_coordinates):
        stepwise_least_recipe = _make_stepwise_least_recipe(recipe, vary_coordinate, index)
        data_serializer.cd_folder(stepwise_least_recipe.name)
        _stepwise_least(stepwise_least_recipe, rbs, data_serializer)
        data_serializer.cd_folder_up()

    data_serializer.clear_sub_folder()

    fixed_histograms = _run_fixed(_make_single_step_recipe(recipe), rbs, data_serializer).histograms
    random_histograms = run_random(_make_stepwise_recipe(recipe), rbs, data_serializer).histograms
    data_serializer.plot_compare(fixed_histograms, random_histograms, recipe.name)


def _run_fixed(recipe: RbsSingleStep, rbs: RbsSetup, data_serializer: RbsDataSerializer) -> RbsData:
    start_time = datetime.now()

    rbs.prepare_counting_with_target(recipe.charge_total)
    rbs.start_data_acquisition()
    rbs.count()
    rbs.stop_data_acquisition()

    rbs_data = rbs.get_status(True)
    data_serializer.save_histograms(rbs_data, recipe.name, recipe.sample)
    data_serializer.plot_histograms(rbs_data, recipe.name)

    data_serializer.single_step_finish(recipe, start_time)
    return rbs_data


def _stepwise_least(recipe: RbsStepwiseLeast, rbs: RbsSetup, data_serializer: RbsDataSerializer):
    start_time = datetime.now()

    rbs.move(recipe.start_position)
    positions = get_positions_as_coordinate(recipe.vary_coordinate)
    rbs.prepare_counting_with_target(recipe.total_charge / len(positions))

    detector_optimize = rbs.get_detector(recipe.optimize_detector_identifier)
    energy_yields = []

    data_serializer.cd_folder("yield_data")

    for position in positions:
        rbs.start_data_acquisition()
        rbs.move_and_count(position)
        rbs.stop_data_acquisition()

        data = rbs.get_packed_histogram(detector_optimize)
        integrated_energy_yield = get_sum(data, recipe.integration_window)
        energy_yields.append(integrated_energy_yield)

        rbs_data = rbs.get_status(True)
        file_stem = recipe.name + "_" + single_coordinate_to_string(position, recipe.vary_coordinate)
        data_serializer.save_histograms(rbs_data, file_stem, recipe.sample)
        data_serializer.plot_histograms(rbs_data, file_stem)

    data_serializer.cd_folder_up()
    angles = get_positions_as_float(recipe.vary_coordinate)
    data_serializer.store_yields(recipe.name, angles, energy_yields)

    try:
        smooth_angles, smooth_yields = fit.fit_and_smooth(angles, energy_yields)
        min_angle = fit.get_angle_for_minimum_yield(smooth_angles, smooth_yields)
        min_position = convert_float_to_coordinate(recipe.vary_coordinate.name, min_angle)
        data_serializer.plot_energy_yields(recipe.name, angles, energy_yields, smooth_angles, smooth_yields)
        rbs.move(min_position)
        data_serializer.stepwise_least_finish(recipe, angles, energy_yields, min_angle, start_time)
    except RuntimeError as e:
        logging.error(e)
        data_serializer.stepwise_least_terminate(recipe, angles, energy_yields, str(e), start_time)


def _make_stepwise_least_recipe(recipe, vary_coordinate, index: int):
    return RbsStepwiseLeast(type=RecipeType.ANGULAR_YIELD, sample=recipe.sample,
                            name=recipe.name + "_" + str(index) + "_vary_" + str(vary_coordinate.name),
                            total_charge=recipe.yield_charge_total,
                            vary_coordinate=vary_coordinate, integration_window=
                            recipe.yield_integration_window,
                            optimize_detector_identifier=recipe.yield_optimize_detector_identifier)


def _make_single_step_recipe(recipe):
    return RbsSingleStep(type=RecipeType.FIXED, sample=recipe.sample,
                         name=recipe.name + "_fixed",
                         charge_total=recipe.random_fixed_charge_total)


def _make_stepwise_recipe(recipe):
    return RbsStepwise(type=RecipeType.RANDOM, sample=recipe.sample,
                       name=recipe.name + "_random",
                       charge_total=recipe.random_fixed_charge_total,
                       start_position={"theta": -2},
                       vary_coordinate=recipe.random_vary_coordinate)


def _get_total_counts_stepwise(recipe: RbsStepwise):
    return recipe.charge_total


def _get_total_counts_channeling(recipe: RbsChanneling):
    yield_optimize_total_charge = recipe.yield_charge_total * len(recipe.yield_vary_coordinates)
    compare_total_charge = 2 * recipe.random_fixed_charge_total
    return yield_optimize_total_charge + compare_total_charge


def _get_total_counts(recipe: Union[RbsStepwise, RbsChanneling]):
    if recipe.type == RecipeType.CHANNELING:
        return _get_total_counts_channeling(recipe)
    if recipe.type == RecipeType.RANDOM:
        return _get_total_counts_stepwise(recipe)


def single_coordinate_to_string(position: PositionCoordinates, coordinate: VaryCoordinate) -> str:
    position_value = position.dict()[coordinate.name]
    return coordinate.name[0] + "_" + str(position_value)


def get_positions_as_coordinate(vary_coordinate: VaryCoordinate) -> List[PositionCoordinates]:
    angles = get_positions_as_float(vary_coordinate)
    positions = [PositionCoordinates.parse_obj({vary_coordinate.name: angle}) for angle in angles]
    return positions


def get_positions_as_float(vary_coordinate: VaryCoordinate) -> List[float]:
    if vary_coordinate.increment == 0:
        return [vary_coordinate.start]
    coordinate_range = np.arange(vary_coordinate.start, vary_coordinate.end + vary_coordinate.increment,
                                 vary_coordinate.increment)
    numpy_array = np.around(coordinate_range, decimals=2)
    return [float(x) for x in numpy_array]


def convert_float_to_coordinate(coordinate_name: str, position: float) -> PositionCoordinates:
    return PositionCoordinates.parse_obj({coordinate_name: position})


def get_sum(data: List[int], window: Window) -> int:
    return sum(data[window.start:window.end])
