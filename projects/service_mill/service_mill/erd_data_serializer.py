import logging
import traceback
from datetime import datetime
from pathlib import Path
from shutil import copy2
import copy
from typing import Dict

from threading import Lock

from hive.hardware_control.data_serializer import DataSerializer
from erd_entities import ErdJobModel, ErdRecipe
from hive.hardware_control.erd_entities import ErdData
from logbook_db import LogBookDb


def _try_copy(source, destination):
    logging.info("copying {source} to {destination}".format(source=source, destination=destination))
    try:
        Path.mkdir(destination.parent, exist_ok=True)
        copy2(source, destination)
    except:
        logging.error(traceback.format_exc())


class ErdDataSerializer:
    _data_store: DataSerializer
    _db: LogBookDb
    _time_loaded: datetime
    _job: ErdJobModel

    def __init__(self, data_store: DataSerializer, log_book_db: LogBookDb):
        self._data_store = data_store
        self._lock = Lock()
        self._abort = False
        self._db = log_book_db

    def abort(self):
        with self._lock:
            self._abort = True

    def resume(self):
        with self._lock:
            self._abort = False

    def aborted(self):
        with self._lock:
            return copy.deepcopy(self._abort)

    def prepare_job(self, job: ErdJobModel):
        self._job = job
        self._data_store.set_base_folder(job.job_id)
        self._db.job_start(job)
        self._time_loaded = datetime.now()

    def finalize_job(self, job_model: ErdJobModel, job_result: Dict):
        trends = self._db.get_trends(str(self._time_loaded), str(datetime.now()), "erd")
        self._data_store.write_csv_panda_to_disk("erd_trends.csv", trends)
        trends = self._db.get_trends(str(self._time_loaded), str(datetime.now()), "any")
        self._data_store.write_csv_panda_to_disk("any_trends.csv", trends)
        self._data_store.write_json_to_disk("active_rqm.json", job_result)
        self._data_store.write_csv_panda_to_disk("service_log.csv", self._db.get_job_summary())
        self._db.job_end(job_model)
        self.resume()

    def save_recipe_result(self, erd_data: ErdData, recipe: ErdRecipe):
        if self.aborted():
            return
        self._db.erd_recipe_finish(self._job, recipe, self._time_loaded)
        self._data_store.write_text_to_disk(recipe.file_stem + ".flt", erd_data.histogram)
        self._data_store.write_text_to_disk(recipe.file_stem + ".meta",
                                            _serialize_meta(erd_data, recipe, self._job, self._time_loaded))


def _serialize_meta(erd_data: ErdData, recipe: ErdRecipe, job_model: ErdJobModel, start_time):
    header = """ % Comments
 % Title                 := {title}
 % Section := <raw_data>
 *
 * Recipe name           := {recipe_name}
 * DATE/Time             := {date}
 * MEASURING TIME[sec]   := {measure_time_sec}
 * Job id                := {job_id}
 *
 * ENERGY[MeV]           := {beam_energy} MeV
 * Beam type             := {beam_type}
 * Sample Tilt Degrees   := {sample_tilt_degrees}
 *
 * Sample ID             := {sample_id}
 * Sample Z              := {sample_z}
 * Sample Theta          := {sample_theta}
 * Z Start               := {z_start}
 * Z End                 := {z_end}
 * Z Increment           := {z_increment}
 * Z Repeat              := {z_repeat}
 *
 * Start time            := {start_time}
 * End time              := {end_time}
 *
 * Avg Terminal Voltage  := {average_terminal_voltage}
 *
 % Section :=  </raw_data>
 % End comments""".format(
        title=recipe.file_stem,
        recipe_name=recipe.file_stem,
        date=datetime.utcnow().strftime("%Y.%m.%d__%H:%M__%S.%f")[:-3],
        measure_time_sec=erd_data.measuring_time_sec,
        beam_energy=job_model.beam_energy_MeV,
        beam_type=job_model.beam_type,
        sample_tilt_degrees=job_model.sample_tilt_degrees,
        sample_id=recipe.sample_id,
        sample_z=erd_data.mdrive_z["motor_position"],
        sample_theta=erd_data.mdrive_theta["motor_position"],
        z_start=recipe.z_start,
        z_end=recipe.z_end,
        z_increment=recipe.z_increment,
        z_repeat=recipe.z_repeat,
        start_time=start_time,
        end_time=datetime.now(),
        average_terminal_voltage=0,
        job_id=job_model.job_id,
    )
    return header
