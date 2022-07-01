import logging
import traceback
from typing import Union

from hive.erd_entities import ErdJobModel
from hive.job_factory import JobFactory
from hive.job_runner import JobRunner
from hive.rbs_entities import RbsJobModel
from fastapi import UploadFile, Response, File, status


def build_job_routes(http_server, job_runner: JobRunner, job_factory: JobFactory):
    @http_server.post("/api/job/erd", tags=["JOBS"], summary="Schedule an ERD experiment")
    async def run_rbs(job: ErdJobModel):
        job = job_factory.make_erd_job(job)
        job_runner.add_job_to_queue(job)

    @http_server.post("/api/job/rbs", tags=["JOBS"], summary="Schedule an RBS experiment")
    async def run_rbs(job: RbsJobModel):
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
    async def parse_job_csv(response: Response, file: UploadFile = File(...)):
        try:
            file_bytes = await file.read()
            contents = file_bytes.decode('utf-8')
            return job_factory.make_job_model_from_csv(contents)
        except Exception as e:
            logging.error(traceback.format_exc())
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return str(e)