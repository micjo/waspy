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
        self._data_store.set_base_folder(job.job_id)
        self._db.job_start(job)
        self._time_loaded = datetime.now()

    def finalize_job(self, job_model: ErdJobModel, job_result: Dict):
        trends = self._db.get_trends(str(self._time_loaded), str(datetime.now()), "erd")
        self._data_store.write_csv_panda_to_disk("erd_trends.csv", trends)
        trends = self._db.get_trends(str(self._time_loaded), str(datetime.now()), "any")
        self._data_store.write_csv_panda_to_disk("any_trends.csv", trends)
        self._data_store.write_json_to_disk("active_rqm.json", job_result)
        self._db.job_end(job_model)
        self.resume()

    def save_recipe_result(self, job_id:str,  recipe: ErdRecipe):
        self._db.erd_recipe_finish(job_id, recipe)

    def save_histogram(self, histogram: str, file_stem):
        if self.aborted():
            return
        self._data_store.write_text_to_disk(file_stem + ".flt", histogram)
