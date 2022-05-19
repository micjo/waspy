import logging
import traceback
from typing import Union

from erd_entities import ErdJobModel
from job_factory import JobFactory
from job_runner import JobRunner
from rbs_entities import RbsJobModel
from fastapi import UploadFile, Response, File, status


def build_job_routes(http_server, job_runner: JobRunner, job_factory: JobFactory):
    @http_server.post("/api/job/schedule", tags=["JOBS"], summary="Run an RBS or ERD experiment")
    async def run_rbs(job: Union[ErdJobModel, RbsJobModel]):
        if type(job) == ErdJobModel:
            job = job_factory.make_erd_job(job)
        elif type(job) == RbsJobModel:
            job = job_factory.make_rbs_job(job)
        job_runner.add_job_to_queue(job)

    @http_server.get("/api/job/state", tags=["JOBS"], summary="Get the state of the job(s)")
    async def get_job_status():
        return job_runner.get_state()

    @http_server.post("/api/job/abort_active", tags=["JOBS"], summary="Abort the running job")
    async def abort_active():
        job_runner.abort_active()

    @http_server.post("/api/job/abort_schedule", tags=["JOBS"], summary="Abort the scheduled jobs")
    async def abort_schedule():
        job_runner.abort_schedule()

    @http_server.post("/api/job/csv_conversion", tags=["JOBS"])
    async def parse_erd_csv(response: Response, file: UploadFile = File(...)):
        try:
            file_bytes = await file.read()
            contents = file_bytes.decode('utf-8')
            return job_factory.make_job_model_from_csv(contents)
        except Exception as e:
            logging.error(traceback.format_exc())
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return str(e)

    @http_server.post("/api/job/rbs_csv_conversion", tags=["JOBS"])
    async def parse_rbs_csv(response: Response, file: UploadFile = File(...)):
        try:
            file_bytes = await file.read()
            contents = file_bytes.decode('utf-8')
            return job_factory.make_rbs_job_model_from_csv(contents)
        except Exception as e:
            logging.error(traceback.format_exc())
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return str(e)
