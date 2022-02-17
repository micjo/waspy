import logging
import copy
from datetime import datetime, timedelta
from typing import List, Union

from pydantic import BaseModel

from app.rbs import yield_angle_fit as fit
from app.rbs.data_serializer import RbsDataSerializer
from app.rbs.entities import RbsRqm, RecipeType, RbsRqmRandom, RbsRqmChanneling, RbsRqmFixed, RbsData, \
    RbsRqmMinimizeYield
from app.rbs.rbs_setup import RbsSetup, get_positions_as_coordinate, get_sum, single_coordinate_to_string, \
    get_positions_as_float, convert_float_to_coordinate
from app.rqm.rqm_action_plan import RqmActionPlan
from app.trends.trend import Trend
from hive_exception import HiveError


class RbsRecipeStatus(BaseModel):
    recipe_id: str
    start_time: datetime
    run_time: timedelta
    accumulated_charge_corrected: float
    accumulated_charge_target: float


empty_rbs_recipe_status = RbsRecipeStatus(recipe_id="", start_time=datetime.now(), run_time=0,
                                          accumulated_charge_corrected=0,
                                          accumulated_charge_target=0)


class RbsAction(RqmActionPlan):
    _data_serializer: RbsDataSerializer
    _rbs_setup: RbsSetup
    _job: RbsRqm
    _did_error: bool
    _error_message: str
    _active_recipe: RbsRecipeStatus
    _finished_recipes: List[RbsRecipeStatus]
    _aborted: bool
    _trends: List[Trend]

    def __init__(self, job: RbsRqm, rbs_setup: RbsSetup, data_serializer: RbsDataSerializer, trends: List[Trend]):
        self._rbs_setup = rbs_setup
        self._data_serializer = data_serializer
        self._job = job
        self._did_error = False
        self._error_message = "No Error"
        self._run_time = timedelta(0)
        self._active_recipe = empty_rbs_recipe_status
        self._finished_recipes = []
        self._aborted = False
        self._trends = trends

    def execute(self):
        self._data_serializer.set_base_folder(self._job.rqm_number)
        self._rbs_setup.set_active_detectors(self._job.detectors)
        start_time = datetime.now()

        logging.info("[RQM RBS] RQM Start: '" + str(self._job) + "'")
        for recipe in self._job.recipes:
            if self._aborted:
                break
            try:
                self._run_recipe(recipe)
            except HiveError as e:
                self._did_error = True
                self._error_message = str(e)
                break
            finally:
                self._finish_recipe()

        end_time = datetime.now()
        for trend in self._trends:
            trend_values = trend.get_values(start_time, end_time, timedelta(seconds=1))
            self._data_serializer.save_trends(trend.get_file_stem(), trend_values)

        self._data_serializer.save_rqm(self.serialize())
        self._rbs_setup.resume()
        self._data_serializer.resume()

    def serialize(self):
        self._active_recipe.run_time = datetime.now() - self._active_recipe.start_time
        self._active_recipe.accumulated_charge_corrected = self._rbs_setup.get_corrected_total_accumulated_charge()
        finished_recipes = [recipe.dict() for recipe in self._finished_recipes]

        status = {"rqm": self._job.dict(), "active_recipe": self._active_recipe.dict(),
                  "finished_recipes": finished_recipes, "error_state": self._error_message}
        return status

    def abort(self):
        logging.info("[RQM RBS] RQM abort")
        self._aborted = True
        self._error_message = str("Aborted RQM")
        self._rbs_setup.abort()
        self._data_serializer.abort()

    def completed(self) -> bool:
        if self._did_error:
            return False
        if self._aborted:
            return False
        return True

    def empty(self):
        return False

    def _run_recipe(self, recipe):
        self._rbs_setup.charge_offset = 0
        self._active_recipe.start_time = datetime.now()
        self._active_recipe.recipe_id = recipe.file_stem
        self._active_recipe.accumulated_charge_target = _get_total_counts(recipe)
        if recipe.type == RecipeType.random:
            run_random(recipe, self._rbs_setup, self._data_serializer)
        if recipe.type == RecipeType.channeling:
            run_channeling(recipe, self._rbs_setup, self._data_serializer)

    def _finish_recipe(self):
        self.serialize()
        self._finished_recipes.append(copy.deepcopy(self._active_recipe))
        self._active_recipe = empty_rbs_recipe_status


def run_random(recipe: RbsRqmRandom, rbs: RbsSetup, data_serializer: RbsDataSerializer, clear_offset=True):
    if clear_offset:
        rbs.clear_total_accumulated_charge()
    rbs.move(recipe.start_position)
    positions = get_positions_as_coordinate(recipe.vary_coordinate)
    rbs.prepare_counting(recipe.charge_total / len(positions))
    rbs.prepare_data_acquisition()

    for index, position in enumerate(positions):
        rbs.move_and_count(position)
    rbs.stop_data_acquisition()

    rbs_data = rbs.get_status(True)
    data_serializer.save_histograms(rbs_data, recipe.file_stem, recipe.sample_id)
    data_serializer.plot_histograms(rbs_data, recipe.file_stem)
    return rbs_data


def run_channeling(recipe: RbsRqmChanneling, rbs: RbsSetup, data_serializer: RbsDataSerializer):
    rbs.clear_total_accumulated_charge()
    rbs.move(recipe.start_position)

    for index, vary_coordinate in enumerate(recipe.yield_vary_coordinates):
        yield_recipe = _make_minimize_yield_recipe(recipe, vary_coordinate)
        yield_recipe.file_stem = recipe.file_stem + "_" + str(index) + "_vary_" + str(vary_coordinate.name)
        data_serializer.set_sub_folder(recipe.file_stem + "_" + str(index) + "_vary_" + str(vary_coordinate.name))
        _minimize_yield(yield_recipe, rbs, data_serializer)
    data_serializer.clear_sub_folder()

    fixed_histograms = _run_fixed(_make_fixed_recipe(recipe), rbs, data_serializer).histograms
    random_histograms = run_random(_make_random_recipe(recipe), rbs, data_serializer, False).histograms
    detectors = rbs.get_detectors()
    data_serializer.plot_compare(detectors, fixed_histograms, random_histograms, recipe.file_stem)


def _run_fixed(self, recipe: RbsRqmFixed, rbs: RbsSetup, data_serializer: RbsDataSerializer) -> RbsData:
    rbs.prepare_counting(recipe.charge_total)
    rbs.prepare_data_acquisition()
    rbs.count()
    rbs.stop_data_acquisition()

    rbs_data = rbs.get_status(True)
    data_serializer.save_histograms(rbs_data, recipe.file_stem, recipe.sample_id)
    data_serializer.plot_histograms(rbs_data, recipe.file_stem)
    return rbs_data


def _minimize_yield(recipe: RbsRqmMinimizeYield, rbs: RbsSetup, data_serializer: RbsDataSerializer):
    rbs.move(recipe.start_position)
    positions = get_positions_as_coordinate(recipe.vary_coordinate)
    rbs.prepare_counting(recipe.total_charge / len(positions))

    detector_optimize = rbs.get_detectors()[recipe.optimize_detector_index]
    energy_yields = []

    for position in positions:
        rbs.prepare_data_acquisition()
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
    smooth_angles, smooth_yields = fit.fit_and_smooth(angles, energy_yields)
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
