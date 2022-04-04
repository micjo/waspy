from typing import Union
import requests, logging
from app.rbs.entities import RbsJobModel, RbsRqmChanneling, RbsRqmRandom


class LogBookDb:
    _logbook_rowid: int
    _logbook_url: str

    def __init__(self, logbook_url):
        self._logbook_rowid = 0
        self._logbook_url = logbook_url

    def rbs_start(self, job: RbsJobModel):
        response = requests.post(self._logbook_url + "/log_rbs_start?rbs_name=" + job.rqm_number)
        self._logbook_rowid = int(response.text)

    def rbs_recipe_finish(self, job_id: str, recipe: Union[RbsRqmChanneling, RbsRqmRandom]):
        requests.post(self._logbook_url +
                      "/log_rbs_recipe_finish?"
                      "row_id=" + str(self._logbook_rowid) +
                      "&rbs=" + job_id +
                      "&recipe_name=" + recipe.file_stem)

    def rbs_end(self, job: RbsJobModel):
        response = requests.post(self._logbook_url + "/log_rbs_end?rbs_name=" + job.rqm_number)
