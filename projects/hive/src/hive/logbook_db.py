import json
from datetime import datetime
from typing import Union, Dict

import pandas as pd
import requests
from hive.rbs_entities import RbsJobModel, RbsChanneling, RbsStepwise, RbsSingleStep, RbsStepwiseLeast, RecipeType
from hive.erd_entities import ErdJobModel, ErdRecipe


class LogBookDb:
    _logbook_url: str
    _time_loaded: datetime

    def __init__(self, logbook_url):
        self._logbook_url = logbook_url

    def job_start(self, job: Union[RbsJobModel, ErdJobModel]):
        self._time_loaded = datetime.now()
        requests.post(self._logbook_url + "/log_started_job?name=" + job.name)

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

    def get_trends(self, start: datetime, end: datetime, starts_with: str):
        start_str = str(start)
        end_str = str(end)
        url = self._logbook_url + f"/get_trend_starts_with?start={start_str}&end={end_str}&starts_with={starts_with}&step=1"
        response = requests.get(url).json()
        df = pd.DataFrame.from_dict(response)
        df['time'] = pd.to_datetime(df['epoch'], unit='s')
        return df.to_dict(orient='list')
