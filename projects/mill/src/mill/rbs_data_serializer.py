from datetime import datetime
import copy
from threading import Lock
from typing import List, Dict
import numpy as np

from waspy.iba.file_writer import FileWriter
from mill.logbook_db import LogBookDb
from mill.rbs_entities import RbsJobModel
from waspy.iba.rbs_entities import RbsData
from matplotlib import pyplot as plt
import matplotlib

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

        # params = self._db.get_last_beam_parameters()
        #
        # plt.title(file_stem)
        # for histogram_data in rbs_data.histograms:
        #     header = _serialize_histogram_header(rbs_data, histogram_data.title, file_stem, sample_id, params)
        #     formatted_data = format_caen_histogram(histogram_data.data)
        #     full_data = header + "\n" + formatted_data
        #
        #     self._data_store.write_text_to_disk(file_stem + "_" + histogram_data.title + ".txt", full_data)




