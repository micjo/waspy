import logging
import time
from threading import Thread, Lock
from typing import List, Dict

from mill.job import Job, EmptyJob, empty_job, execute


class JobRunner(Thread):
    _scheduled_jobs: List[Job]
    _active_job: Job
    _abort: bool
    _lock: Lock
    _run_status: str

    def __init__(self):
        Thread.__init__(self)
        self._scheduled_jobs = []
        self._abort = False
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
            scheduled_jobs = _get_job_list_status(self._scheduled_jobs)
            active_job = self._active_job.serialize()
        state = {"run_status": self._run_status, "schedule": scheduled_jobs, "active_job": active_job}
        return state

    def add_job_to_queue(self, job: Job):
        logging.info("adding job to queue")
        with self._lock:
            self._scheduled_jobs.append(job)

    def run(self):
        while True:
            time.sleep(1)
            job = self._pop_job()
            self._set_active_job(job)
            if job != empty_job:
                execute(job)

    def _set_active_job(self, job: Job):
        with self._lock:
            self._active_job = job
            self._run_status = "Idle" if job == empty_job else "Running"

    def _pop_job(self) -> Job:
        with self._lock:
            if self._scheduled_jobs:
                return self._scheduled_jobs.pop(0)
            else:
                return empty_job


def _get_job_list_status(job_list: List[Job]) -> List[Dict]:
    job_status = [job.serialize() for job in job_list]
    return job_status
