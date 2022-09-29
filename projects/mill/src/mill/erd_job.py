import logging
import copy
import numpy as np
from datetime import datetime, timedelta
from typing import List

from pydantic import BaseModel

from mill.erd_data_serializer import ErdDataSerializer
from mill.erd_entities import ErdJobModel, ErdRecipe
from waspy.iba.erd_setup import ErdSetup, PositionCoordinates

from mill.job import Job
from mill.mill_error import MillError, AbortedError


class ErdRecipeStatus(BaseModel):
    name: str
    start_time: datetime
    run_time: timedelta
    measurement_time: float
    measurement_time_target: float
    progress: str
    sample: str


empty_erd_recipe_status = ErdRecipeStatus(name="", sample="", start_time=datetime.now(), run_time=0,
                                          measurement_time=0, measurement_time_target=0, progress="0.0%")


class ErdJob(Job):
    _data_serializer: ErdDataSerializer
    _erd_setup: ErdSetup
    _job_model: ErdJobModel
    _active_recipe: ErdRecipeStatus
    _finished_recipes: List[ErdRecipeStatus]
    _aborted: bool
    _running: bool

    def __init__(self, job_model: ErdJobModel, erd_setup: ErdSetup, data_serializer: ErdDataSerializer):
        self._erd_setup = erd_setup
        self._data_serializer = data_serializer
        self._job_model = job_model
        self._run_time = timedelta(0)
        self._active_recipe = copy.deepcopy(empty_erd_recipe_status)
        self._finished_recipes = []
        self._aborted = False
        self._running = False

    def setup(self) -> None:
        self._data_serializer.prepare_job(self._job_model)
        self._erd_setup.reupload_config()

    def exec(self):
        """ Can raise: AbortedError, HardwareError"""
        for recipe in self._job_model.recipes:
            self._run_recipe(recipe)
            self._finish_recipe()

    def teardown(self):
        self._data_serializer.finalize_job(self._job_model, self.serialize())
        self._erd_setup.resume()

    def terminate(self, message: str) -> None:
        self._data_serializer.terminate_job(self._job_model.name, message)

    def serialize(self):
        self._update_active_recipe()
        finished_recipes = [recipe.dict() for recipe in self._finished_recipes]
        status = {"job": self._job_model.dict(), "active_recipe": self._active_recipe.dict(),
                  "finished_recipes": finished_recipes}
        return status

    def _update_active_recipe(self):
        """Can raise: HardwareError"""

        if self._running:
            self._active_recipe.run_time = datetime.now() - self._active_recipe.start_time
            self._active_recipe.measurement_time = self._erd_setup.get_measurement_time()
            progress = self._active_recipe.measurement_time / self._active_recipe.measurement_time_target * 100
            self._active_recipe.progress = "{:.2f}%".format(progress)

    def abort(self):
        logging.info("[ERD] Recipe" + str(self._active_recipe) + "aborted")
        self._aborted = True
        self._erd_setup.abort()
        self._data_serializer.abort()

    def _run_recipe(self, recipe):
        if self._aborted:
            raise AbortedError("Job Terminated")

        self._running = True
        self._active_recipe.start_time = datetime.now()
        self._active_recipe.name = recipe.name
        self._active_recipe.run_time = timedelta(0)
        self._active_recipe.measurement_time = 0
        self._active_recipe.measurement_time_target = recipe.measuring_time_sec
        run_erd_recipe(recipe, self._erd_setup, self._data_serializer)

    def _finish_recipe(self):
        self._update_active_recipe()
        self._finished_recipes.append(copy.deepcopy(self._active_recipe))
        self._active_recipe = empty_erd_recipe_status


def run_erd_recipe(recipe: ErdRecipe, erd_setup: ErdSetup, erd_data_serializer: ErdDataSerializer):
    start_time = datetime.now()
    erd_setup.move(PositionCoordinates(z=recipe.z_start, theta=recipe.theta))
    erd_setup.wait_for_arrival()
    erd_setup.configure_acquisition(recipe.measuring_time_sec, recipe.name)
    erd_setup.start_acquisition()
    erd_setup.wait_for_acquisition_started()
    z_range = get_z_range(recipe.z_start, recipe.z_end, recipe.z_increment, recipe.z_repeat)
    if len(z_range) == 0:
        raise MillError("Invalid z range")
    wait_time = recipe.measuring_time_sec / len(z_range)
    _log_recipe(recipe, wait_time, z_range)
    for z in z_range:
        erd_setup.move(z)
        erd_setup.wait_for(wait_time)

    erd_setup.wait_for_acquisition_done()
    erd_setup.convert_data_to_ascii()
    erd_data_serializer.save_recipe_result(erd_setup.get_status(get_histogram=True), recipe, start_time)


def _log_recipe(recipe, wait_time, z_range):
    position_list = "("
    position_list += "; ".join([str(position.z) for position in z_range])
    position_list += ")"
    logging.info("Recipe: " + recipe.name + ", wait_time_sec between steps: " + str(wait_time) +
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
