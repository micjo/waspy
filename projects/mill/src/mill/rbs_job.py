import copy
import logging
from datetime import datetime
from typing import List, Union, Dict

from mill.logbook_db import LogBookDb
from waspy.iba.rbs_entities import RecipeType, RbsRandom, RbsChanneling, AysJournal, CoordinateRange
from mill.rbs_entities import RbsJobModel, make_rbs_status
from mill.job import Job

from waspy.iba.file_writer import FileWriter
from waspy.iba.rbs_recipes import run_random, run_channeling, save_rbs_journal, save_channeling_journal
from waspy.iba.rbs_setup import RbsSetup

empty_recipe = RbsRandom(type="rbs_random", sample="", name="", charge_total=0,
                         coordinate_range=CoordinateRange(name="none", start=0, end=0, increment=0))


class RbsJob(Job):
    _rbs_setup: RbsSetup
    _job_model: RbsJobModel
    _finished_recipes: List
    _running: bool
    _db: LogBookDb
    _file_writer: FileWriter
    _time_loaded: datetime
    _ays_index: int
    _active_recipe: RbsRandom | RbsChanneling
    _recipe_start_time: datetime
    _extra_meta: Dict
    _cancelled: bool

    def __init__(self, job_model: RbsJobModel, rbs_setup: RbsSetup,
                 file_writer: FileWriter, db: LogBookDb):
        self._rbs_setup = rbs_setup
        self._job_model = job_model
        self._active_recipe = copy.deepcopy(empty_recipe)
        self._finished_recipes = []
        self._db = db
        self._file_writer = file_writer
        self._running = False
        self._ays_index = 0
        self._recipe_start_time = datetime.now()
        self._cancelled = False

    def setup(self):
        self._file_writer.set_base_folder(self._job_model.name)
        self._db.job_start(self._job_model)
        self._rbs_setup.resume()
        self._rbs_setup.clear_charge_offset()

    def exec(self):
        """ Can raise: AbortedError, HardwareError"""
        self._time_loaded = datetime.now()
        for recipe in self._job_model.recipes:
            self._run_recipe(recipe)
            self._finish_recipe()

    def teardown(self):
        trends = self._db.get_trends(self._time_loaded, datetime.now(), "rbs")
        self._file_writer.write_csv_panda_to_disk("rbs_trends.csv", trends)
        trends = self._db.get_trends(self._time_loaded, datetime.now(), "any")
        self._file_writer.write_csv_panda_to_disk("any_trends.csv", trends)
        self._file_writer.write_json_to_disk("job.json", self.serialize())
        self._db.job_finish(self._job_model)
        self._rbs_setup.finish()

    def terminate(self, message: str) -> None:
        self._db.job_terminate(self._job_model.name, message)

    def serialize(self):
        active_recipe_status = make_rbs_status(self._active_recipe, self.get_recipe_progress(), self._recipe_start_time)
        status = {"job": self._job_model.dict(), "active_recipe": active_recipe_status.dict(),
                  "finished_recipes": self._finished_recipes}
        return status

    def get_recipe_progress(self):
        target_charge = _get_total_counts(self._active_recipe)
        actual_charge = self._rbs_setup.get_total_clipped_charge()
        progress = actual_charge / target_charge * 100 if self._running else 0
        return f'{progress:02}'

    def _ays_report_cb(self, ays_result: AysJournal):
        if not ays_result.fit.success:
            logging.error("Fit failure:" + str(ays_result))
            self.cancel()

    def _run_random_recipe(self, recipe: RbsRandom):
        journal = run_random(recipe, self._rbs_setup)
        save_rbs_journal(self._file_writer, recipe, journal, self._extra_params)
        # TODO: log finish in db

    def _run_channeling_recipe(self, recipe: RbsChanneling):
        self._ays_index = 0
        journal = run_channeling(recipe, self._rbs_setup, self._ays_report_cb)
        save_channeling_journal(self._file_writer, recipe, journal, self._extra_params)
        # TODO: log finish in db

    def _run_recipe(self, recipe: RbsRandom | RbsChanneling):
        self._active_recipe = recipe
        self._rbs_setup.clear_charge_offset()
        self._recipe_start_time = datetime.now()
        self._running = True
        self._extra_params = self._db.get_last_beam_parameters()
        if recipe.type == RecipeType.RANDOM:
            self._run_random_recipe(recipe)
        if recipe.type == RecipeType.CHANNELING:
            self._run_channeling_recipe(recipe)
        self._running = False

    def _finish_recipe(self):
        finished_recipe_status = make_rbs_status(self._active_recipe, 100, self._recipe_start_time)
        self._finished_recipes.append(finished_recipe_status.dict())
        self._active_recipe = copy.deepcopy(empty_recipe)

    def cancel(self):
        logging.info("[RBS] Recipe" + str(self._active_recipe) + "cancelled")
        self._rbs_setup.cancel()
        self._cancelled = True


def _get_total_counts_stepwise(recipe: RbsRandom):
    return recipe.charge_total


def _get_total_counts_channeling(recipe: RbsChanneling):
    yield_optimize_total_charge = recipe.yield_charge_total * len(recipe.yield_coordinate_ranges)
    compare_total_charge = 2 * recipe.compare_charge_total
    return yield_optimize_total_charge + compare_total_charge


def _get_total_counts(recipe: Union[RbsRandom, RbsChanneling]):
    if recipe.type == RecipeType.CHANNELING:
        return _get_total_counts_channeling(recipe)
    if recipe.type == RecipeType.RANDOM:
        return _get_total_counts_stepwise(recipe)
