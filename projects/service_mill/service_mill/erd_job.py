import logging
import copy
import traceback
import numpy as np
from datetime import datetime, timedelta
from typing import List

from pydantic import BaseModel

from erd_data_serializer import ErdDataSerializer
from erd_entities import ErdJobModel, ErdRecipe
from hive.hardware_control.erd_setup import ErdSetup, PositionCoordinates

from job import Job
from hive_exception import HiveError


class ErdRecipeStatus(BaseModel):
    recipe_id: str
    start_time: datetime
    run_time: timedelta
    measurement_time: float
    measurement_time_target: float
    progress: str


empty_erd_recipe_status = ErdRecipeStatus(recipe_id="", start_time=datetime.now(), run_time=0,
                                          measurement_time=0, measurement_time_target=0, progress="0.0%")


class ErdJob(Job):
    _data_serializer: ErdDataSerializer
    _erd_setup: ErdSetup
    _job_model: ErdJobModel
    _did_error: bool
    _error_message: str
    _active_recipe: ErdRecipeStatus
    _finished_recipes: List[ErdRecipeStatus]
    _aborted: bool

    def __init__(self, job_model: ErdJobModel, erd_setup: ErdSetup, data_serializer: ErdDataSerializer):
        self._erd_setup = erd_setup
        self._data_serializer = data_serializer
        self._job_model = job_model
        self._did_error = False
        self._error_message = "No Error"
        self._run_time = timedelta(0)
        self._active_recipe = empty_erd_recipe_status
        self._finished_recipes = []
        self._aborted = False

    def execute(self):
        self._data_serializer.prepare_job(self._job_model)
        self._erd_setup.reupload_config()

        logging.info("[RQM ERD] RQM Start: '" + str(self._job_model) + "'")
        for recipe in self._job_model.recipes:
            if self._aborted:
                break
            try:
                self._run_recipe(recipe)
            except Exception as e:
                logging.error("[ERD] Recipe: {" + str(recipe) + "}\nfailed with message: " + str(e))
                self._did_error = True
                self._error_message = str(e)
                logging.error(traceback.format_exc())
                self._finished_recipes = []
                break
            self._finish_recipe()

        self._data_serializer.finalize_job(self._job_model, self.get_status())
        self._erd_setup.resume()

    def get_status(self):
        self._update_active_recipe()
        finished_recipes = [recipe.dict() for recipe in self._finished_recipes]
        status = {"job": self._job_model.dict(), "active_recipe": self._active_recipe.dict(),
                  "finished_recipes": finished_recipes, "error_state": self._error_message}
        return status

    def _update_active_recipe(self):
        self._active_recipe.run_time = datetime.now() - self._active_recipe.start_time
        self._active_recipe.measurement_time = self._erd_setup.get_measurement_time()
        if self._active_recipe.measurement_time_target != 0:
            progress = self._active_recipe.measurement_time / self._active_recipe.measurement_time_target * 100
            self._active_recipe.progress = "{:.2f}%".format(progress)
        else:
            self._active_recipe.progress = "0.00%"


    def abort(self):
        logging.info("[RQM ERD] RQM abort")
        self._aborted = True
        self._error_message = str("Aborted RQM")
        self._erd_setup.abort()
        self._data_serializer.abort()
        self._active_recipe = copy.deepcopy(empty_erd_recipe_status)

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
        self._update_active_recipe()
        self._finished_recipes.append(copy.deepcopy(self._active_recipe))
        self._active_recipe = empty_erd_recipe_status


def run_erd_recipe(recipe: ErdRecipe, erd_setup: ErdSetup, erd_data_serializer: ErdDataSerializer):
    erd_setup.move(PositionCoordinates(z=recipe.z_start, theta=recipe.theta))
    erd_setup.wait_for_arrival()
    erd_setup.configure_acquisition(recipe.measuring_time_sec, recipe.file_stem)
    erd_setup.start_acquisition()
    erd_setup.wait_for_acquisition_started()
    z_range = get_z_range(recipe.z_start, recipe.z_end, recipe.z_increment, recipe.z_repeat)
    if len(z_range) == 0:
        raise HiveError("Invalid z range")
    wait_time = recipe.measuring_time_sec / len(z_range)
    _log_recipe(recipe, wait_time, z_range)
    for z in z_range:
        erd_setup.move(z)
        erd_setup.wait_for(wait_time)

    erd_setup.wait_for_acquisition_done()
    erd_setup.convert_data_to_ascii()
    erd_data_serializer.save_recipe_result(erd_setup.get_status(get_histogram=True), recipe)


def _log_recipe(recipe, wait_time, z_range):
    position_list = "("
    position_list += "; ".join([str(position.z) for position in z_range])
    position_list += ")"
    logging.info("Recipe: " + recipe.file_stem + ", wait_time_sec between steps: " + str(wait_time) +
                 ", total measurement time: " + str(recipe.measuring_time_sec) +
                 ", z-positions: \n\t" + position_list)


def get_z_range(start, end, increment, repeat=1) -> List[PositionCoordinates]:
    if increment == 0:
        positions = [PositionCoordinates(z=start)]
    else:
        coordinate_range = np.arange(start, end + increment, increment)
        logging.info("start: " + str(start) + ", end: " + str(end) + ", inc: " + str(increment))
        numpy_z_steps = np.around(coordinate_range, decimals=2)
        positions = [PositionCoordinates(z=float(z_step)) for z_step in numpy_z_steps]

    repeated_positions = []
    [repeated_positions.extend(positions) for _ in range(repeat)]
    return repeated_positions
