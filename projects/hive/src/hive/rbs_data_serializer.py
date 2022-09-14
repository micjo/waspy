from datetime import datetime
import copy
from threading import Lock
from typing import List, Dict, Union
import numpy as np

from hive.erd_entities import ErdJobModel
from waspy.hardware_control.file_writer import FileWriter
from waspy.hardware_control.hw_action import format_caen_histogram
from hive.logbook_db import LogBookDb
from hive.rbs_entities import RbsJobModel, RbsStepwise, RbsChanneling, RbsStepwiseLeast, RbsSingleStep
from waspy.hardware_control.rbs_entities import CaenDetector, HistogramData, RbsHistogramGraphData, \
    RbsHistogramGraphDataSet, RbsData
from matplotlib import pyplot as plt
import matplotlib
from waspy.hardware_control.plot import plot_rbs_histograms, plot_compare_rbs_histograms

matplotlib.use('Agg')


class RbsDataSerializer:
    _data_store: FileWriter
    _db: LogBookDb
    _time_loaded: datetime

    def __init__(self, data_serializer: FileWriter, db: LogBookDb):
        self._data_store = data_serializer
        self._lock = Lock()
        self._abort = False
        self._db = db

    def abort(self):
        with self._lock:
            self._abort = True

    def resume(self):
        with self._lock:
            self._abort = False

    def aborted(self):
        with self._lock:
            return copy.deepcopy(self._abort)

    def prepare_job(self, job: RbsJobModel):
        self._data_store.set_base_folder(job.name)
        self._db.job_start(job)
        self._time_loaded = datetime.now()

    def terminate_job(self, job_name: str, reason: str):
        self._db.job_terminate(job_name, reason)

    def finalize_job(self, job_model: RbsJobModel, job_result: Dict):
        trends = self._db.get_trends(self._time_loaded, datetime.now(), "rbs")
        self._data_store.write_csv_panda_to_disk("rbs_trends.csv", trends)
        trends = self._db.get_trends(self._time_loaded, datetime.now(), "any")
        self._data_store.write_csv_panda_to_disk("any_trends.csv", trends)
        self._data_store.write_json_to_disk("active_rqm.json", job_result)
        self._db.job_finish(job_model)
        self.resume()

    def stepwise_finish(self, recipe: RbsStepwise, start_time: datetime):
        finished_recipe = _make_finished_vary_recipe(recipe, start_time)
        self._db.recipe_finish(finished_recipe)

    def single_step_finish(self, recipe: RbsSingleStep, start_time: datetime):
        finished_recipe = _make_finished_basic_recipe(recipe, start_time)
        self._db.recipe_finish(finished_recipe)

    def stepwise_least_finish(self, recipe: RbsStepwiseLeast, angles: List[float], energy_yields: List[int],
                              position: float, start_time: datetime):
        finished_recipe = _make_finished_vary_recipe(recipe, start_time)
        finished_recipe["yield_positions"] = list(zip(angles, energy_yields))
        finished_recipe["least_yield_position"] = position
        self._db.recipe_finish(finished_recipe)

    def stepwise_least_terminate(self, recipe: RbsStepwiseLeast, angles: List[float], energy_yields: List[int],
                                 reason: str, start_time: datetime):
        terminated_recipe = _make_finished_vary_recipe(recipe, start_time)
        terminated_recipe["yield_positions"] = np.column_pack((angles, energy_yields))
        self._db.recipe_terminate(terminated_recipe, reason)

    def cd_folder(self, sub_folder: str):
        self._data_store.cd_folder(sub_folder)

    def cd_folder_up(self):
        self._data_store.cd_folder_up()

    def clear_sub_folder(self):
        self._data_store.clear_sub_folder()

    def fitting_fail(self, file_stem, extra: str):
        self._data_store.write_text_to_disk(file_stem + "_FAILURE.txt",
                                            "Fitting the angular yields failed: \n" + extra)

    def _flush_plot(self, fig, file_stem):
        if self.aborted():
            return
        self._data_store.write_matplotlib_fig_to_disk(file_stem + ".png", fig)

    def plot_histograms(self, rbs_data: RbsData, file_stem: str):
        if self.aborted():
            return

        rbs_histogram_graph_data = RbsHistogramGraphData(graph_title=file_stem, histograms=rbs_data.histograms)
        fig = plot_rbs_histograms(rbs_histogram_graph_data)
        self._flush_plot(fig, file_stem)

    def plot_compare(self, fixed_data: List[HistogramData], random_data: List[HistogramData], file_stem):
        if self.aborted():
            return

        histograms = []

        for (random, fixed) in zip(random_data, fixed_data):
            random.title += "_random"
            fixed.title += "_fixed"
            histograms.append([random, fixed])

        rbs_histogram_graph_data_set = RbsHistogramGraphDataSet(graph_title=file_stem,
                                                                histograms=histograms,
                                                                x_label="energy level",
                                                                y_label="yield")

        fig = plot_compare_rbs_histograms(rbs_histogram_graph_data_set)
        self._flush_plot(fig, file_stem)

    def plot_energy_yields(self, file_stem,
                           angles: List[float], yields: List[int], smooth_angles: List[float],
                           smooth_yields: List[float]):
        if self.aborted():
            return
        fig, ax = plt.subplots()
        ax.scatter(angles, yields, marker="+", color="red", label="Data Points")
        ax.axhline(np.amin(yields), label="Minimum", linestyle=":")
        ax.plot(smooth_angles, smooth_yields, color="green", label="Fit")
        ax.legend(loc=0)
        plt.xlabel("degrees").set_fontsize(15)
        plt.ylabel("yield").set_fontsize(15)
        plt.title(file_stem)
        plt.grid()
        self._flush_plot(fig, file_stem + "_yields")

    def store_yields(self, file_stem, angle_values, energy_yields):
        if self.aborted():
            return

        content = ""
        for index, angle in enumerate(angle_values):
            content += "{angle}, {energy_yield}\n".format(angle=angle, energy_yield=energy_yields[index])
        self._data_store.write_text_to_disk(file_stem + "_yields.txt", content)

    def save_histograms(self, rbs_data: RbsData, file_stem, sample_id):
        if self.aborted():
            return

        params = self._db.get_last_beam_parameters()

        plt.title(file_stem)
        for histogram_data in rbs_data.histograms:
            header = _serialize_histogram_header(rbs_data, histogram_data.title, file_stem, sample_id, params)
            formatted_data = format_caen_histogram(histogram_data.data)
            full_data = header + "\n" + formatted_data

            self._data_store.write_text_to_disk(file_stem + "_" + histogram_data.title + ".txt", full_data)


def _make_finished_basic_recipe(recipe: RbsStepwiseLeast | RbsStepwise | RbsSingleStep, start_time: datetime):
    return {"start_time": str(start_time), "end_time": str(datetime.now()), "name": recipe.name,
            "type": recipe.type.value, "sample": recipe.sample}


def _make_finished_vary_recipe(recipe: RbsStepwiseLeast | RbsStepwise, start_time: datetime):
    finished_recipe = _make_finished_basic_recipe(recipe, start_time)
    finished_recipe["vary_axis"] = recipe.vary_coordinate.name
    finished_recipe["start"] = recipe.vary_coordinate.start
    finished_recipe["end"] = recipe.vary_coordinate.end
    finished_recipe["step"] = recipe.vary_coordinate.increment
    return finished_recipe


def _serialize_histogram_header(rbs_data: RbsData, data_title: str, file_stem: str, sample_id: str, params: dict):
    now = datetime.utcnow().strftime("%Y.%m.%d__%H:%M__%S.%f")[:-3]

    header = f""" % Comments
 % Title                 := {file_stem + "_" + data_title}
 % Section := <raw_data>
 *
 * Filename no extension := {file_stem}
 * DATE/Time             := {now}
 * MEASURING TIME[sec]   := {rbs_data.measuring_time_msec}
 * ndpts                 := {1024}
 *
 * ANAL.IONS(Z)          := 4.002600
 * ANAL.IONS(symb)       := He+
 * ENERGY[MeV]           := {params.get("beam_energy_MeV","")} MeV
 * Charge[nC]            := {rbs_data.accumulated_charge}
 *
 * Sample ID             := {sample_id}
 * Sample X              := {rbs_data.aml_x_y["motor_1_position"]}
 * Sample Y              := {rbs_data.aml_x_y["motor_2_position"]}
 * Sample Zeta           := {rbs_data.aml_phi_zeta["motor_1_position"]}
 * Sample Theta          := {rbs_data.aml_phi_zeta["motor_2_position"]}
 * Sample Phi            := {rbs_data.aml_det_theta["motor_1_position"]}
 * Sample Det            := {rbs_data.aml_det_theta["motor_2_position"]}
 *
 * Detector name         := {data_title}
 * Detector ZETA         := 0.0
 * Detector Omega[mSr]   := 0.42
 * Detector offset[keV]  := 33.14020
 * Detector gain[keV/ch] := 1.972060
 * Detector FWHM[keV]    := 18.0
 *
 % Section :=  </raw_data>
 % End comments"""
    return header
