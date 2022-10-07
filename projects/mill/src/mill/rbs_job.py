import copy
import logging
from datetime import datetime, timedelta
from typing import List, Union, Dict

from pydantic import BaseModel

from mill.logbook_db import LogBookDb
from waspy.iba.rbs_data_serializer import plot_energy_yields
from waspy.iba.rbs_entities import RecipeType, RbsRandom, RbsChanneling, AysJournal, RbsJournal, get_positions_as_float
from mill.rbs_entities import RbsJobModel
from mill.job import Job

from waspy.iba.file_writer import FileWriter
from waspy.iba.rbs_recipes import run_random, run_channeling, save_channeling_graphs_to_disk, save_rbs_graph_to_disk, \
    save_fit_result_to_disk, serialize_energy_yields
from waspy.iba.rbs_setup import RbsSetup


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
    _rbs_setup: RbsSetup
    _job_model: RbsJobModel
    _active_recipe_status: RbsRecipeStatus
    _finished_recipes: List[RbsRecipeStatus]
    _running: bool
    _db: LogBookDb
    _file_writer: FileWriter
    _time_loaded: datetime
    _beam_params: Dict
    _ays_index: int

    def __init__(self, job_model: RbsJobModel, rbs_setup: RbsSetup,
                 file_writer: FileWriter, db: LogBookDb):
        self._rbs_setup = rbs_setup
        self._job_model = job_model
        self._run_time = timedelta(0)
        self._active_recipe_status = copy.deepcopy(empty_rbs_recipe_status)
        self._finished_recipes = []
        self._db = db
        self._file_writer = file_writer
        self._running = False
        self._ays_index = 0

    def setup(self):
        self._file_writer.set_base_folder(self._job_model.name)
        self._db.job_start(self._job_model)
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
        self._file_writer.write_json_to_disk("active_rqm.json", self.serialize())
        self._db.job_finish(self._job_model)
        self._rbs_setup.finish()

    def terminate(self, message: str) -> None:
        self._db.job_terminate(self._job_model.name, message)

    def serialize(self):
        self._update_active_recipe()
        finished_recipes = [recipe.dict() for recipe in self._finished_recipes]
        status = {"job": self._job_model.dict(), "active_recipe": self._active_recipe_status.dict(),
                  "finished_recipes": finished_recipes}
        return status

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

    def _ays_report_cb(self, ays_result: AysJournal):
        yield_coordinate_range = self._recipe.yield_coordinate_ranges[self._ays_index]
        coordinate_ranging = yield_coordinate_range.name
        positions = get_positions_as_float(yield_coordinate_range)
        name = f'{self._recipe.name}_{self._ays_index}_{coordinate_ranging}'

        self._file_writer.cd_folder(name)
        for index, rbs_journal in enumerate(ays_result.rbs_journals):
            self._save_rbs_recipe_result(rbs_journal, f'{index:02}_{name}_{positions[index]}')

        text = serialize_energy_yields(ays_result.fit)
        self._file_writer.write_text_to_disk(f'_{name}_yields.txt', text)
        if ays_result.fit.success:
            fig = plot_energy_yields(self._recipe.name, ays_result.fit)
            self._file_writer.write_matplotlib_fig_to_disk(f'_{self._recipe.name}_{self._ays_index}_{coordinate_ranging}.png', fig)
        else:
            self._file_writer.write_text_to_disk(f'_{self._recipe.name}_FAILURE.txt', "Fitting failed")
        self._ays_index += 1
        self._file_writer.cd_folder_up()
        # TODO: Fix
        # self._db.recipe_finish(ays_result.dict())

    def _run_random_recipe(self, recipe: RbsRandom):
        journal = run_random(recipe, self._rbs_setup)
        self._save_rbs_recipe_result(journal, recipe.name)
        # TODO: fix
        # self._db.recipe_finish(result.json())

    def _run_channeling_recipe(self, recipe: RbsChanneling):
        self._ays_index = 0
        result = run_channeling(recipe, self._rbs_setup, self._ays_report_cb)
        self._save_rbs_recipe_result(result.fixed, recipe.name + "_fixed")
        self._save_rbs_recipe_result(result.random, recipe.name + "_random")
        save_channeling_graphs_to_disk(self._file_writer, result, recipe.name)
        # TODO: fix
        # self._db.recipe_finish(result.json())

    def _run_recipe(self, recipe: RbsRandom | RbsChanneling):
        self._recipe = recipe
        self._rbs_setup.charge_offset = 0
        self._active_recipe_status.start_time = datetime.now()
        self._active_recipe_status.name = recipe.name
        self._active_recipe_status.accumulated_charge_target = _get_total_counts(recipe)
        self._running = True
        self._beam_params = self._db.get_last_beam_parameters()
        if recipe.type == RecipeType.RANDOM:
            self._run_random_recipe(recipe)
        if recipe.type == RecipeType.CHANNELING:
            self._run_channeling_recipe(recipe)
        self._running = False

    def _save_rbs_recipe_result(self, journal: RbsJournal, file_stem):
        for [detector, histogram] in journal.histograms.items():
            title = f'{file_stem}_{detector}.txt'
            header = _serialize_histogram_header(journal, detector, self._recipe, self._beam_params)
            data = format_caen_histogram(histogram)
            self._file_writer.write_text_to_disk(title, f'{header}\n{data}')
        save_rbs_graph_to_disk(self._file_writer, journal, file_stem)

    def _finish_recipe(self):
        self._update_active_recipe()
        self._finished_recipes.append(copy.deepcopy(self._active_recipe_status))
        self._active_recipe_status = copy.deepcopy(empty_rbs_recipe_status)

    def abort(self):
        logging.info("Abort: need to implement")


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


def format_caen_histogram(data: List[int]) -> str:
    index = 0
    data_string = ""
    for energy_level in data:
        data_string += f'{index}, {energy_level}\n'
        index += 1
    return data_string


def _serialize_histogram_header(journal: RbsJournal, detector_name, recipe, extra):
    now = datetime.utcnow().strftime("%Y.%m.%d__%H:%M__%S.%f")[:-3]

    header = f""" % Comments
 % Title                 := {recipe.name + "_" + detector_name}
 % Section := <raw_data>
 *
 * Filename no extension := {recipe.name}
 * DATE/Time             := {now}
 * MEASURING TIME[sec]   := {journal.measuring_time_msec}
 * ndpts                 := {1024}
 *
 * ANAL.IONS(Z)          := 4.002600
 * ANAL.IONS(symb)       := He+
 * ENERGY[MeV]           := {extra.get("beam_energy_MeV", "")} MeV
 * Charge[nC]            := {journal.accumulated_charge}
 *
 * Sample ID             := {recipe.sample}
 * Sample X              := {journal.x}
 * Sample Y              := {journal.y}
 * Sample Zeta           := {journal.zeta}
 * Sample Theta          := {journal.theta}
 * Sample Phi            := {journal.phi}
 * Sample Det            := {journal.det}
 *
 * Detector name         := {detector_name}
 * Detector ZETA         := 0.0
 * Detector Omega[mSr]   := 0.42
 * Detector offset[keV]  := 33.14020
 * Detector gain[keV/ch] := 1.972060
 * Detector FWHM[keV]    := 18.0
 *
 % Section :=  </raw_data>
 % End comments"""
    return header
