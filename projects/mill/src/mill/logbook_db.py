from datetime import datetime
from typing import Union, Dict

import pandas as pd
from mill.rbs_entities import RbsJobModel
from mill.erd_entities import ErdJobModel
from waspy.drivers.http_helper import post_safe, get_json_safe


class LogBookDb:
    _logbook_url: str
    _time_loaded: datetime

    def __init__(self, logbook_url):
        self._logbook_url = logbook_url

    def job_start(self, job: Union[RbsJobModel, ErdJobModel]):
        self._time_loaded = datetime.now()
        post_safe(self._logbook_url + "/log_started_job?name=" + job.name)

    def job_terminate(self, name: str, reason: str):
        post_safe(self._logbook_url + "/log_terminated_job?name=" + name + "&reason=" + reason)

    def job_finish(self, job: RbsJobModel | ErdJobModel):
        post_safe(self._logbook_url + "/log_finished_job?name=" + job.name)

    def recipe_terminate(self, recipe: Dict, reason: str):
        post_safe(self._logbook_url + "/log_terminated_recipe?reason=" + reason, json=recipe)

    def recipe_finish(self, recipe: Dict):
        post_safe(self._logbook_url + "/log_finished_recipe", json=recipe)

    def get_last_beam_parameters(self):
        return get_json_safe(self._logbook_url + "/get_last_accelerator_parameters", {})

    def get_trends(self, start: datetime, end: datetime, starts_with: str) -> Dict:
        start_str = str(start)
        end_str = str(end)
        url = self._logbook_url + f"/get_trend_starts_with?start={start_str}&end={end_str}&starts_with={starts_with}&step=1"
        response = get_json_safe(url, {})
        if response == {}:
            return {}
        df = pd.DataFrame.from_dict(response)
        df['time'] = pd.to_datetime(df['epoch'], unit='s')
        return df.to_dict(orient='list')
