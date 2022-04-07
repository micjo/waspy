import logging
import traceback

from fastapi import UploadFile, Response, File, status
from erd_entities import ErdJobModel
from hw_control_routes import build_get_redirect, build_post_redirect, build_mpa3_histogram_redirect
from job_factory import ErdJobFactory
from job_runner import JobRunner


def build_api_endpoints(http_server, job_dispatcher: JobRunner, job_factory: ErdJobFactory):
    @http_server.post("/api/erd/run", tags=["ERD API"], summary="Run an ERD experiment")
    async def run_erd(job: ErdJobModel):
        erd_job = job_factory.make_job(job)
        job_dispatcher.add_rqm_to_queue(erd_job)

    @http_server.get("/api/erd/state", tags=["ERD API"], summary="Get the state of the active rqm")
    async def get_rqm_state():
        return job_dispatcher.get_state()

    @http_server.post("/api/erd/abort_active", tags=["RBS API"], summary="Abort the running rqm")
    async def abort_active():
        job_dispatcher.abort_active()

    @http_server.post("/api/erd/abort_schedule", tags=["RBS API"], summary="Abort the scheduled rqms")
    async def abort_schedule():
        job_dispatcher.abort_schedule()

    @http_server.post("/api/erd/rqm_csv", tags=["ERD API"])
    async def parse_rqm_csv(response: Response, file: UploadFile = File(...)):
        try:
            file_bytes = await file.read()
            contents = file_bytes.decode('utf-8')
            return job_factory.make_job_model_from_csv(contents)
        except Exception as e:
            logging.error(traceback.format_exc())
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return str(e)


def build_hw_endpoints(http_server, erd_hardware):
    for key, daemon in erd_hardware.dict().items():
        build_get_redirect(http_server, daemon['proxy'], daemon['url'], ["ERD API"])
        build_post_redirect(http_server, daemon['proxy'], daemon['url'], ["ERD API"])
        if daemon['type'] == 'mpa3':
            build_mpa3_histogram_redirect(http_server, daemon['proxy'], daemon['url'], ["ERD API"])
