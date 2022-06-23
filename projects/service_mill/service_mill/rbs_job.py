import logging
import copy
import traceback
from datetime import datetime, timedelta
from typing import List, Union

from pydantic import BaseModel

import rbs_yield_angle_fit as fit
from hive.hardware_control.rbs_entities import RbsData, PositionCoordinates

from hive_exception import FitError
from rbs_data_serializer import RbsDataSerializer
from rbs_entities import RbsJobModel, RecipeType, RbsRqmRandom, RbsRqmChanneling, RbsRqmFixed, RbsRqmMinimizeYield, \
    VaryCoordinate, Window
from hive.hardware_control.rbs_setup import RbsSetup
from job import Job
import numpy as np


class RbsRecipeStatus(BaseModel):
    recipe_id: str
    start_time: datetime
    run_time: timedelta
    accumulated_charge_corrected: float
    accumulated_charge_target: float
    progress: str


empty_rbs_recipe_status = RbsRecipeStatus(recipe_id="", start_time=datetime.now(), run_time=0,
                                          accumulated_charge_corrected=0,
                                          accumulated_charge_target=0, progress="0.0%")


class RbsJob(Job):
    _data_serializer: RbsDataSerializer
    _rbs_setup: RbsSetup
    _job_model: RbsJobModel
    _did_error: bool
    _error_message: str
    _active_recipe_status: RbsRecipeStatus
    _finished_recipes: List[RbsRecipeStatus]
    _aborted: bool

    def __init__(self, job_model: RbsJobModel, rbs_setup: RbsSetup, data_serializer: RbsDataSerializer):
        self._rbs_setup = rbs_setup
        self._data_serializer = data_serializer
        self._job_model = job_model
        self._did_error = False
        self._error_message = "No Error"
        self._run_time = timedelta(0)
        self._active_recipe_status = copy.deepcopy(empty_rbs_recipe_status)
        self._finished_recipes = []
        self._aborted = False

    def execute(self):
        self._data_serializer.prepare_job(self._job_model)
        self._rbs_setup.initialize(self._job_model.detectors)
        logging.info("[RBS] Job Start: '" + str(self._job_model) + "'")

        for recipe in self._job_model.recipes:
            if self._aborted:
                break
            try:
                self._run_recipe(recipe)
            except Exception as e:
                logging.error("[RBS] Recipe: {" + str(recipe) + "}\nfailed with message: " + str(e))
                self._did_error = True
                self._error_message = str(e)
                logging.error(traceback.format_exc())
                self._finished_recipes = []
                break
            self._finish_recipe()

        self._data_serializer.finalize_job(self._job_model, self.get_status())
        self._rbs_setup.finish()

    def get_status(self):
        self._update_active_recipe()
        finished_recipes = [recipe.dict() for recipe in self._finished_recipes]
        status = {"job": self._job_model.dict(), "active_recipe": self._active_recipe_status.dict(),
                  "finished_recipes": finished_recipes, "error_state": self._error_message}
        return status

    def abort(self):
        logging.info("[RBS] Recipe" + str(self._active_recipe_status) + "aborted")
        self._aborted = True
        self._error_message = str("Aborted RQM")
        self._rbs_setup.abort()
        self._data_serializer.abort()
        self._active_recipe_status = copy.deepcopy(empty_rbs_recipe_status)

    def completed(self) -> bool:
        if self._did_error:
            return False
        if self._aborted:
            return False
        return True

    def empty(self):
        return False

    def _update_active_recipe(self):
        if self._active_recipe_status != empty_rbs_recipe_status:
            self._active_recipe_status.run_time = datetime.now() - self._active_recipe_status.start_time
            try:
                self._active_recipe_status.accumulated_charge_corrected = self._rbs_setup.get_corrected_total_accumulated_charge()
                active_recipe = self._active_recipe_status

                if active_recipe.accumulated_charge_target != 0:
                    progress = active_recipe.accumulated_charge_corrected / active_recipe.accumulated_charge_target * 100
                    self._active_recipe_status.progress = "{:.2f}%".format(progress)
                else:
                    self._active_recipe_status.progress = "0.00%"
            except Exception as e:
                logging.error(traceback.format_exc())
                self._did_error = True
                self._error_message = str(e)

    def _run_recipe(self, recipe):
        self._rbs_setup.charge_offset = 0
        self._active_recipe_status.start_time = datetime.now()
        self._active_recipe_status.recipe_id = recipe.file_stem
        self._active_recipe_status.accumulated_charge_target = _get_total_counts(recipe)
        if recipe.type == RecipeType.random:
            run_random(recipe, self._rbs_setup, self._data_serializer)
            self._data_serializer.save_recipe_result(self._job_model.job_id, recipe)
        if recipe.type == RecipeType.channeling:
            run_channeling(recipe, self._rbs_setup, self._data_serializer)

    def _finish_recipe(self):
        self._update_active_recipe()
        self._finished_recipes.append(copy.deepcopy(self._active_recipe_status))
        self._active_recipe_status = copy.deepcopy(empty_rbs_recipe_status)


def run_random(recipe: RbsRqmRandom, rbs: RbsSetup, data_serializer: RbsDataSerializer):
    rbs.move(recipe.start_position)
    positions = get_positions_as_coordinate(recipe.vary_coordinate)
    rbs.prepare_counting_with_target(recipe.charge_total / len(positions))
    rbs.start_data_acquisition()

    for index, position in enumerate(positions):
        rbs.move_and_count(position)
    rbs.stop_data_acquisition()

    rbs_data = rbs.get_status(True)
    data_serializer.save_histograms(rbs_data, recipe.file_stem, recipe.sample_id)
    data_serializer.plot_histograms(rbs_data, recipe.file_stem)
    return rbs_data


def run_channeling(recipe: RbsRqmChanneling, rbs: RbsSetup, data_serializer: RbsDataSerializer):
    rbs.move(recipe.start_position)

    for index, vary_coordinate in enumerate(recipe.yield_vary_coordinates):
        yield_recipe = _make_minimize_yield_recipe(recipe, vary_coordinate)
        yield_recipe.file_stem = recipe.file_stem + "_" + str(index) + "_vary_" + str(vary_coordinate.name)
        data_serializer.prepare_yield_step(recipe.file_stem + "_" + str(index) + "_vary_" + str(vary_coordinate.name))
        try:
            _minimize_yield(yield_recipe, rbs, data_serializer)
        except FitError as e:
            logging.error(e)
            data_serializer.fitting_fail(recipe.file_stem, str(e))

    data_serializer.finalize_yield_step()

    fixed_histograms = _run_fixed(_make_fixed_recipe(recipe), rbs, data_serializer).histograms
    random_histograms = run_random(_make_random_recipe(recipe), rbs, data_serializer).histograms
    data_serializer.plot_compare(fixed_histograms, random_histograms, recipe.file_stem)


def _run_fixed(recipe: RbsRqmFixed, rbs: RbsSetup, data_serializer: RbsDataSerializer) -> RbsData:
    rbs.prepare_counting_with_target(recipe.charge_total)
    rbs.start_data_acquisition()
    rbs.count()
    rbs.stop_data_acquisition()

    rbs_data = rbs.get_status(True)
    data_serializer.save_histograms(rbs_data, recipe.file_stem, recipe.sample_id)
    data_serializer.plot_histograms(rbs_data, recipe.file_stem)
    return rbs_data


def _minimize_yield(recipe: RbsRqmMinimizeYield, rbs: RbsSetup, data_serializer: RbsDataSerializer):
    rbs.move(recipe.start_position)
    positions = get_positions_as_coordinate(recipe.vary_coordinate)
    rbs.prepare_counting_with_target(recipe.total_charge / len(positions))

    detector_optimize = rbs.get_detectors()[recipe.optimize_detector_index]
    energy_yields = []

    for position in positions:
        rbs.start_data_acquisition()
        rbs.move_and_count(position)
        rbs.stop_data_acquisition()

        data = rbs.get_packed_histogram(detector_optimize)
        integrated_energy_yield = get_sum(data, recipe.integration_window)
        energy_yields.append(integrated_energy_yield)

        rbs_data = rbs.get_status(True)
        file_stem = recipe.file_stem + "_" + single_coordinate_to_string(position, recipe.vary_coordinate)
        data_serializer.save_histograms(rbs_data, file_stem, recipe.sample_id)
        data_serializer.plot_histograms(rbs_data, file_stem)

    angles = get_positions_as_float(recipe.vary_coordinate)
    try:
        smooth_angles, smooth_yields = fit.fit_and_smooth(angles, energy_yields)
    except Exception:
        logging.error(traceback.format_exc())
        raise FitError("Failed to fit the specified angular yields")
    min_angle = fit.get_angle_for_minimum_yield(smooth_angles, smooth_yields)
    min_position = convert_float_to_coordinate(recipe.vary_coordinate.name, min_angle)

    data_serializer.store_yields(recipe.file_stem, angles, energy_yields)
    data_serializer.plot_energy_yields(recipe.file_stem, angles, energy_yields, smooth_angles, smooth_yields)
    rbs.move(min_position)


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
