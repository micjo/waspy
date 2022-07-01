import logging
import time
from collections import deque
from threading import Thread, Lock
from typing import List, Dict

from hive.job import Job, EmptyJob, empty_job


class JobRunner(Thread):
    _scheduled_jobs: List[Job]
    _done_jobs: deque[Job]
    _failed_jobs: deque[Job]
    _active_job: Job
    _abort: bool
    _lock: Lock
    _run_status: str

    def __init__(self):
        Thread.__init__(self)
        self._scheduled_jobs = []
        self._abort = False
        self._done_jobs = deque(maxlen=5)
        self._failed_jobs = deque(maxlen=5)
        self._active_job = EmptyJob()
        self._run_status = "Idle"
        self._lock = Lock()

    def abort_active(self) -> None:
        with self._lock:
            self._active_job.abort()

    def abort_schedule(self) -> None:
        with self._lock:
            self._scheduled_jobs = []

    def get_state(self) -> Dict:
        with self._lock:
            scheuled_jobs = _get_rqm_list_status(self._scheduled_jobs)
            past_jobs = _get_rqm_list_status(list(self._done_jobs))
            failed_jobs = _get_rqm_list_status(list(self._failed_jobs))
            active_job = self._active_job.get_status()
        state = {"run_status": self._run_status, "schedule": scheuled_jobs, "active_job": active_job, "done": past_jobs,
                 "failed": failed_jobs}
        return state

    def add_job_to_queue(self, rqm: Job):
        logging.info("adding job to queue")
        with self._lock:
            self._scheduled_jobs.append(rqm)

    def run(self):
        while True:
            time.sleep(1)
            rqm = self._pop_rqm()
            self._set_active_rqm(rqm)
            if not rqm.empty():
                rqm.execute()
                if rqm.completed():
                    self._done_jobs.appendleft(rqm)
                else:
                    self._failed_jobs.appendleft(rqm)

    def _set_active_rqm(self, rqm):
        with self._lock:
            self._active_job = rqm
            self._run_status = "Idle" if rqm.empty() else "Running"

    def _pop_rqm(self) -> Job:
        with self._lock:
            if self._scheduled_jobs:
                return self._scheduled_jobs.pop(0)
            else:
                return empty_job


def _get_rqm_list_status(rqm_list: List[Job]) -> List[Dict]:
    rqm_status = [rqm.get_status() for rqm in rqm_list]
    return rqm_status
