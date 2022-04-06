from typing import Union
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

    def erd_recipe_finish(self, job_id: str, recipe: ErdRecipe):
        requests.post(self._logbook_url +
                      "/log_recipe_finish?"
                      "row_id=" + str(self._logbook_rowid) +
                      "&job_type=erd" +
                      "&job_id=" + job_id +
                      "&recipe_id=" + recipe.file_stem)

    def job_end(self, job: Union[RbsJobModel, ErdJobModel]):
        requests.post(self._logbook_url + "/log_job_end?"
                                          "job_type=" + job.type +
                      "&job_id=" + job.job_id)

    def get_trends(self, start: str, end: str, starts_with: str):
        url = self._logbook_url + f"/get_trend_starts_with?start={start}&end={end}&starts_with={starts_with}&step=1"
        return requests.get(url).json()
