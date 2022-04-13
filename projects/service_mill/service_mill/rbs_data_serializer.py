import io
from datetime import datetime
import copy
from threading import Lock
from typing import List, Dict, Union
import numpy as np
import pandas as pd
import json

from data_serializer import DataSerializer
from logbook_db import LogBookDb
from rbs_entities import DoublePath, RbsData, CaenDetectorModel, RbsJobModel, RbsRqmRandom, RbsRqmChanneling
from matplotlib import pyplot as plt
import matplotlib

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

    def save_recipe_result(self, job_id:str,  recipe: Union[RbsRqmRandom, RbsRqmChanneling]):
        self._db.rbs_recipe_finish(job_id, recipe)

    def prepare_yield_step(self, sub_folder: str):
        self._data_store.set_sub_folder(sub_folder)

    def finalize_yield_step(self):
        self._data_store.set_sub_folder("")

    def _flush_plot(self, fig, file_stem):
        if self.aborted():
            return
        plt.subplots_adjust(hspace=0.5)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        self._data_store.write_bytes_to_disk(file_stem + ".png", buf)
        plt.close(fig)
        plt.clf()

    def plot_histograms(self, rbs_data: RbsData, file_stem: str):
        if self.aborted():
            return
        data = rbs_data.histograms
        fig, axs = plt.subplots(len(data))
        fig.suptitle(file_stem)

        for index, ax in enumerate(axs):
            ax.plot(data[index], label=rbs_data.detectors[index].identifier)
            ax.grid(which='major')
            ax.grid(which='minor', linestyle=":")
            ax.minorticks_on()
            ax.legend()
            ax.set_xlabel("energy level")
            ax.set_ylabel("yield")
        self._flush_plot(fig, file_stem)

    def plot_compare(self, detectors: List[CaenDetectorModel], fixed_data: List[List[int]],
                     random_data: List[List[int]], file_stem):
        if self.aborted():
            return

        nr_of_histograms = len(fixed_data)
        fixed_labels = [detector.identifier + "_fixed" for detector in detectors]
        random_labels = [detector.identifier + "_random" for detector in detectors]
        fig, axs = plt.subplots(nr_of_histograms)

        for index, ax in enumerate(axs):
            ax.plot(fixed_data[index], label=fixed_labels[index])
            ax.plot(random_data[index], label=random_labels[index])
            ax.grid(which='major')
            ax.grid(which='minor', linestyle=":")
            ax.minorticks_on()
            ax.legend()
            ax.set_xlabel("energy level")
            ax.set_ylabel("yield")
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
        for index, detector in enumerate(rbs_data.detectors):
            header = _serialize_histogram_header(rbs_data, detector.identifier, file_stem, sample_id)
            formatted_data = _format_caen_histogram(rbs_data.histograms[index])
            full_data = header + "\n" + formatted_data

            self._data_store.write_text_to_disk(file_stem + "_" + detector.identifier + ".txt", full_data)


def _serialize_histogram_header(rbs_data: RbsData, detector_id: str, file_stem: str, sample_id: str):
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
 * ENERGY[MeV]           := 1.5 MeV
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
        title=file_stem + "_" + detector_id,
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
        det_name=detector_id
    )
    return header


def _format_caen_histogram(data: List[int]):
    index = 0
    data_string = ""
    for energy_level in data:
        data_string += str(index) + ", " + str(energy_level) + "\n"
        index += 1
    return data_string
