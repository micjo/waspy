import logging
import traceback
from datetime import datetime
from pathlib import Path
from shutil import copy2, move
import os
import copy
from threading import Lock
from typing import List, Dict
import numpy as np
import json


from app.rbs_experiment.entities import DoublePath, RbsData, CaenDetectorModel, RbsRqm
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')

def _try_copy(source, destination):
    logging.info("copying {source} to {destination}".format(source=source, destination=destination))
    try:
        Path.mkdir(destination.parent, exist_ok=True)
        copy2(source, destination)
    except:
        logging.error(traceback.format_exc())


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


class RbsDataSerializer:
    data_dir: DoublePath
    base_folder: Path
    sub_folder: Path

    def __init__(self, data_dir: DoublePath):
        self.data_dir = data_dir
        self.sub_folder = Path("")
        self._make_folders()
        self._lock = Lock()
        self._abort = False

    def abort(self):
        with self._lock:
            self._abort = True

    def resume(self):
        with self._lock:
            self._abort = False

    def aborted(self):
        with self._lock:
            return copy.deepcopy(self._abort)

    def _make_folders(self):
        Path.mkdir(self.data_dir.local, parents=True, exist_ok=True)
        Path.mkdir(self.data_dir.remote, parents=True, exist_ok=True)

    def clear_sub_folder(self):
        self.sub_folder = Path("")



    def set_base_folder(self, base_folder: str):
        self.base_folder = Path(base_folder)
        Path.mkdir(self.data_dir.local / self.base_folder, exist_ok=True)
        Path.mkdir(self.data_dir.remote / self.base_folder, exist_ok=True)
        subdir = "old_" + datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        self.move_files(self.data_dir.local, subdir)
        self.move_files(self.data_dir.remote, subdir)

    def move_files(self, base, subdir):
        files_to_move = [x for x in (base / self.base_folder).iterdir() if not x.stem.startswith("old_")]
        if files_to_move:
            full_subdir = base / self.base_folder / subdir
            logging.info("Existing files found, moving them to: '" + str(full_subdir) + "'.")
            Path.mkdir(full_subdir, exist_ok=True)
            for file in files_to_move:
                move(file, full_subdir)

    def save_rqm(self, rqm: dict):
        file_stem = "active_rqm.txt"
        local = self.data_dir.local / self._get_folder() / file_stem
        remote = self.data_dir.remote /self._get_folder() / file_stem
        with open(local, 'w+') as f:
            f.write("Running RQM:\n")
            f.write(json.dumps(rqm,indent=4))
        _try_copy(local, remote)

    def set_sub_folder(self, sub_folder: str):
        self.sub_folder = Path(sub_folder)
        Path.mkdir(self.data_dir.remote / self.base_folder / self.sub_folder, exist_ok=True)

    def _get_folder(self):
        return self.base_folder / self.sub_folder

    def _flush_plot(self, fig, file_stem):
        if self.aborted():
            return
        plt.subplots_adjust(hspace=0.5)
        histogram_file = file_stem + ".png"
        histogram_path = self.data_dir.local / self._get_folder() / histogram_file
        Path.mkdir(histogram_path.parent, parents=True, exist_ok=True)
        logging.info("Storing histogram plot to path: " + str(histogram_path))
        plt.savefig(histogram_path)
        remote_histogram_path = self.data_dir.remote / self._get_folder() / histogram_file
        _try_copy(histogram_path, remote_histogram_path)
        plt.close(fig)

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

        yield_plot_file = file_stem + "_yields.png"
        yield_plot_path = self.data_dir.local / self._get_folder() / yield_plot_file
        Path.mkdir(yield_plot_path.parent, parents=True, exist_ok=True)
        logging.info("Storing yield plot to path: " + str(yield_plot_path))
        plt.savefig(yield_plot_path)
        plt.clf()

        remote_yield_plot_path = self.data_dir.remote / self._get_folder() / yield_plot_file
        _try_copy(yield_plot_path, remote_yield_plot_path)
        plt.close(fig)

    def store_yields(self, file_stem, angle_values, energy_yields):
        if self.aborted():
            return
        yields_file = file_stem + "_yields.txt"
        yields_path = self.data_dir.local / self._get_folder() / yields_file

        with open(yields_path, 'w+') as f:
            for index, angle in enumerate(angle_values):
                f.write("{angle}, {energy_yield}\n".format(angle=angle, energy_yield=energy_yields[index]))

        remote_yields_path = self.data_dir.remote / self._get_folder() / yields_file
        _try_copy(yields_path, remote_yields_path)

    def save_histograms(self, rbs_data: RbsData, file_stem, sample_id):
        if self.aborted():
            return
        plt.title(file_stem)
        for index, detector in enumerate(rbs_data.detectors):
            header = _serialize_histogram_header(rbs_data, detector.identifier, file_stem, sample_id)
            formatted_data = _format_caen_histogram(rbs_data.histograms[index])
            full_data = header + "\n" + formatted_data
            histogram_file = file_stem + "_" + detector.identifier + ".txt"
            histogram_path = self.data_dir.local / self._get_folder() / histogram_file
            Path.mkdir(histogram_path.parent, parents=True, exist_ok=True)
            logging.info("Storing histogram data to path: " + str(histogram_path))
            with open(histogram_path, 'w+') as f:
                f.write(full_data)

            remote_histogram_path = self.data_dir.remote / self._get_folder() / histogram_file
            _try_copy(histogram_path, remote_histogram_path)
