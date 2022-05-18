import json
from datetime import datetime
from typing import Union

import pandas as pd
import requests
from rbs_entities import RbsJobModel, RbsRqmChanneling, RbsRqmRandom
from erd_entities import ErdJobModel, ErdRecipe


class LogBookDb:
    _logbook_rowid: int
    _logbook_url: str

    def __init__(self, logbook_url):
        self._logbook_rowid = 0
        self._logbook_url = logbook_url

    def job_start(self, job: Union[RbsJobModel, ErdJobModel]):
        response = requests.post(self._logbook_url + "/log_job_start?"
                                                     "job_type=" + job.type +
                                 "&job_id=" + job.job_id)
        self._logbook_rowid = int(response.text)

    def rbs_recipe_finish(self, job_id: str, recipe: Union[RbsRqmChanneling, RbsRqmRandom]):
        requests.post(self._logbook_url +
                      "/log_recipe_finish?"
                      "row_id=" + str(self._logbook_rowid) +
                      "&job_type=rbs" +
                      "&job_id=" + job_id +
                      "&recipe_id=" + recipe.file_stem)

    def erd_recipe_finish(self, job_model: ErdJobModel, recipe: ErdRecipe, time_loaded: datetime):
        recipe_result = recipe.dict()
        recipe_result["job_id"] = job_model.job_id
        recipe_result["beam_type"] = job_model.beam_type
        recipe_result["beam_energy_MeV"] = job_model.beam_energy_MeV
        recipe_result["sample_tilt_degrees"] = job_model.sample_tilt_degrees
        recipe_result["start_time"] = str(time_loaded)
        recipe_result["end_time"] = str(datetime.now())
        recipe_result["avg_terminal_voltage"] = 0.0
        recipe_result["type"] = "erd"
        print("--------------")
        print(json.dumps(recipe_result))

        url = self._logbook_url + "/log_erd_recipe_finish?row_id={}".format(self._logbook_rowid)

        response = requests.post(url, json=recipe_result, timeout=10)

    def get_job_summary(self):
        return requests.get(self._logbook_url + "/get_erd_service_log?row_id={}".format(self._logbook_rowid)).json()

    def job_end(self, job: Union[RbsJobModel, ErdJobModel]):
        requests.post(self._logbook_url + "/log_job_end?"
                                          "job_type=" + job.type +
                      "&job_id=" + job.job_id)

    def get_trends(self, start: str, end: str, starts_with: str):
        url = self._logbook_url + f"/get_trend_starts_with?start={start}&end={end}&starts_with={starts_with}&step=1"
        response = requests.get(url).json()
        df = pd.DataFrame.from_dict(response)
        df['time'] = pd.to_datetime(df['epoch'], unit='s')
        return df.to_dict(orient='list')
