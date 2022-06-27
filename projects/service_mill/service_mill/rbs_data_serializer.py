import io
from datetime import datetime
import copy
from threading import Lock
from typing import List, Dict, Union
import numpy as np

from hive.hardware_control.data_serializer import DataSerializer
from hive.hardware_control.hw_action import format_caen_histogram
from logbook_db import LogBookDb
from rbs_entities import RbsJobModel, RbsRqmRandom, RbsRqmChanneling
from hive.hardware_control.rbs_entities import CaenDetector, HistogramData, RbsHistogramGraphData, \
    RbsHistogramGraphDataSet, RbsData
from matplotlib import pyplot as plt
import matplotlib
from hive.hardware_control.plot import plot_rbs_histograms, plot_compare_rbs_histograms

matplotlib.use('Agg')


class RbsDataSerializer:
    _data_store: DataSerializer
    _db: LogBookDb
    _time_loaded: datetime

    def __init__(self, data_serializer: DataSerializer, db: LogBookDb):
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
        self._data_store.set_base_folder(job.job_id)
        self._db.job_start(job)
        self._time_loaded = datetime.now()

    def finalize_job(self, job_model: RbsJobModel, job_result: Dict):
        trends = self._db.get_trends(str(self._time_loaded), str(datetime.now()), "rbs")
        self._data_store.write_csv_panda_to_disk("rbs_trends.csv", trends)
        trends = self._db.get_trends(str(self._time_loaded), str(datetime.now()), "any")
        self._data_store.write_csv_panda_to_disk("any_trends.csv", trends)
        self._data_store.write_json_to_disk("active_rqm.json", job_result)
        self._db.job_end(job_model)
        self.resume()

    def save_recipe_result(self, job_id: str, recipe: Union[RbsRqmRandom, RbsRqmChanneling]):
        self._db.rbs_recipe_finish(job_id, recipe)

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

        plt.title(file_stem)
        for histogram_data in rbs_data.histograms:
            header = _serialize_histogram_header(rbs_data, histogram_data.title, file_stem, sample_id)
            formatted_data = format_caen_histogram(histogram_data.data)
            full_data = header + "\n" + formatted_data

            self._data_store.write_text_to_disk(file_stem + "_" + histogram_data.title + ".txt", full_data)


def _serialize_histogram_header(rbs_data: RbsData, data_title: str, file_stem: str, sample_id: str):
    header = """ % Comments
 % Title                 := {title}
 % Section := <raw_data>
 *
 * Filename no extension := {filename}
 * DATE/Time             := {date}
 * MEASURING TIME[sec]   := {measure_time_sec}
 * ndpts                 := {ndpts}
 *
 * ANAL.IONS(Z)          := 4.002600
 * ANAL.IONS(symb)       := He+
 * ENERGY[MeV]           := 1.523 MeV
 * Charge[nC]            := {charge}
 *
 * Sample ID             := {sample_id}
 * Sample X              := {sample_x}
 * Sample Y              := {sample_y}
 * Sample Zeta           := {sample_zeta}
 * Sample Theta          := {sample_theta}
 * Sample Phi            := {sample_phi}
 * Sample Det            := {sample_det}
 *
 * Detector name         := {det_name}
 * Detector ZETA         := 0.0
 * Detector Omega[mSr]   := 0.42
 * Detector offset[keV]  := 33.14020
 * Detector gain[keV/ch] := 1.972060
 * Detector FWHM[keV]    := 18.0
 *
 % Section :=  </raw_data>
 % End comments""".format(
        title=file_stem + "_" + data_title,
        filename=file_stem,
        date=datetime.utcnow().strftime("%Y.%m.%d__%H:%M__%S.%f")[:-3],
        measure_time_sec=rbs_data.measuring_time_msec,
        ndpts=1024,
        charge=rbs_data.accumulated_charge,
        sample_id=sample_id,
        sample_x=rbs_data.aml_x_y["motor_1_position"],
        sample_y=rbs_data.aml_x_y["motor_2_position"],
        sample_phi=rbs_data.aml_phi_zeta["motor_1_position"],
        sample_zeta=rbs_data.aml_phi_zeta["motor_2_position"],
        sample_det=rbs_data.aml_det_theta["motor_1_position"],
        sample_theta=rbs_data.aml_det_theta["motor_2_position"],
        det_name=data_title
    )
    return header
