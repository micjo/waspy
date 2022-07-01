import json
from datetime import datetime
from typing import Union, Dict

import pandas as pd
import requests
from hive.rbs_entities import RbsJobModel, RbsChanneling, RbsStepwise, RbsSingleStep, RbsStepwiseLeast, RecipeType
from hive.erd_entities import ErdJobModel, ErdRecipe


class LogBookDb:
    _logbook_url: str

    def __init__(self, logbook_url):
        self._logbook_url = logbook_url

    def job_start(self, job: Union[RbsJobModel, ErdJobModel]):
        response = requests.post(self._logbook_url + "/log_started_job?name=" + job.name)
        print(response.text)

    def job_terminate(self, name: str, reason: str):
        requests.post(self._logbook_url + "/log_terminated_job?name=" + name + "&reason=" + reason)

    def job_finish(self, job: RbsJobModel | ErdJobModel):
        requests.post(self._logbook_url + "/log_finished_job?name=" + job.name)

    def recipe_terminate(self, recipe: Dict, reason: str):
        print(recipe)
        requests.post(self._logbook_url + "/log_terminated_recipe?reason=" + reason, json=recipe)

    def recipe_finish(self, recipe: Dict):
        print(recipe)
        requests.post(self._logbook_url + "/log_finished_recipe", json=recipe)

    # def erd_recipe_finish(self, job_model: ErdJobModel, recipe: ErdRecipe, time_loaded: datetime):
    #     recipe_result = recipe.dict()
    #     recipe_result["job_id"] = job_model.job_id
    #     recipe_result["beam_type"] = job_model.beam_type
    #     recipe_result["beam_energy_MeV"] = job_model.beam_energy_MeV
    #     recipe_result["sample_tilt_degrees"] = job_model.sample_tilt_degrees
    #     recipe_result["start_time"] = str(time_loaded)
    #     recipe_result["end_time"] = str(datetime.now())
    #     recipe_result["avg_terminal_voltage"] = 0.0
    #     recipe_result["type"] = "erd"
    #     print("--------------")
    #     print(json.dumps(recipe_result))
    #
    #
    # def get_job_summary(self):
    #     return requests.get(self._logbook_url + "/get_erd_service_log?row_id={}".format(self._logbook_rowid)).json()

    def get_trends(self, start: str, end: str, starts_with: str):
        url = self._logbook_url + f"/get_trend_starts_with?start={start}&end={end}&starts_with={starts_with}&step=1"
        response = requests.get(url).json()
        df = pd.DataFrame.from_dict(response)
        df['time'] = pd.to_datetime(df['epoch'], unit='s')
        return df.to_dict(orient='list')
