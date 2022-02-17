import logging
import copy
from datetime import datetime, timedelta
from typing import List

from pydantic import BaseModel

from app.erd.data_serializer import ErdDataSerializer
from app.erd.entities import ErdRqm, ErdRecipe, PositionCoordinates
from app.erd.erd_setup import ErdSetup, get_z_range
from app.rqm.rqm_action_plan import RqmActionPlan
from app.trends.trend import Trend
from hive_exception import HiveError


class ErdRecipeStatus(BaseModel):
    recipe_id: str
    start_time: datetime
    run_time: timedelta
    measurement_time: float
    measurement_time_target: float


empty_erd_recipe_status = ErdRecipeStatus(recipe_id="", start_time=datetime.now(), run_time=0,
                                          measurement_time=0, measurement_time_target=0)


class ErdAction(RqmActionPlan):
    _data_serializer: ErdDataSerializer
    _erd_setup: ErdSetup
    _job : ErdRqm
    _did_error: bool
    _error_message: str
    _active_recipe: ErdRecipeStatus
    _finished_recipes: List[ErdRecipeStatus]
    _aborted: bool
    _trends: List[Trend]

    def __init__(self, job: ErdRqm, erd_setup: ErdSetup, data_serializer: ErdDataSerializer, trends:List[Trend]):
        self._erd_setup = erd_setup
        self._data_serializer = data_serializer
        self._job = job
        self._did_error = False
        self._error_message = "No Error"
        self._run_time = timedelta(0)
        self._active_recipe = empty_erd_recipe_status
        self._finished_recipes = []
        self._aborted = False
        self._trends = trends

    def execute(self):
        self._data_serializer.set_base_folder(self._job.rqm_number)
        start_time=datetime.now()

        logging.info("[RQM ERD] RQM Start: '" + str(self._job) + "'")
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
        self._erd_setup.resume()
        self._data_serializer.resume()

    def serialize(self):
        self._active_recipe.run_time = datetime.now() - self._active_recipe.start_time
        self._active_recipe.measurement_time = self._erd_setup.get_measurement_time()
        finished_recipes = [recipe.dict() for recipe in self._finished_recipes]

        status = {"rqm": self._job.dict(), "active_recipe": self._active_recipe.dict(),
                  "finished_recipes": finished_recipes, "error_state": self._error_message}
        return status

    def abort(self):
        logging.info("[RQM ERD] RQM abort")
        self._aborted = True
        self._error_message = str("Aborted RQM")
        self._erd_setup.abort()
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
        self._active_recipe.start_time = datetime.now()
        self._active_recipe.recipe_id = recipe.file_stem
        self._active_recipe.run_time = timedelta(0)
        self._active_recipe.measurement_time = 0
        self._active_recipe.measurement_time_target = recipe.measuring_time_sec
        run_erd_recipe(recipe, self._erd_setup, self._data_serializer)

    def _finish_recipe(self):
        self.serialize()
        self._finished_recipes.append(copy.deepcopy(self._active_recipe))
        self._active_recipe = empty_erd_recipe_status


def run_erd_recipe(recipe: ErdRecipe, erd_setup: ErdSetup, erd_data_serializer: ErdDataSerializer):
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









