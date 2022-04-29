
from fastapi import UploadFile, File, Response, status
from hw_control_routes import build_get_redirect, build_post_redirect, build_histogram_redirect, \
    build_packed_histogram
from job_factory import RbsJobFactory
from rbs_entities import RbsJobModel
import logging
import traceback
from job_runner import JobRunner


def build_rbs_job_endpoints(http_server, job_dispatcher: JobRunner, job_factory: RbsJobFactory):
    @http_server.post("/api/rbs/run", tags=["RBS API"], summary="Run an rbs experiment")
    async def run_rbs(job: RbsJobModel):
        rqm_action = job_factory.make_job(job)
        job_dispatcher.add_job_to_queue(rqm_action)

    @http_server.get("/api/rbs/state", tags=["RBS API"], summary="Get the state of the active rqm")
    async def get_rqm_state():
        return job_dispatcher.get_state()

    @http_server.post("/api/rbs/abort_active", tags=["RBS API"], summary="Abort the running rqm")
    async def abort_active():
        job_dispatcher.abort_active()

    @http_server.post("/api/rbs/abort_schedule", tags=["RBS API"], summary="Abort the scheduled rqms")
    async def abort_schedule():
        job_dispatcher.abort_schedule()

    @http_server.post("/api/rbs/rqm_csv", tags=["RBS API"])
    async def parse_rqm_csv(response: Response, file: UploadFile = File(...)):
        try:
            file_bytes = await file.read()
            contents = file_bytes.decode('utf-8')
            return job_factory.make_job_model_from_csv(contents)
        except Exception as e:
            logging.error(traceback.format_exc())
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return str(e)

    @http_server.post("/api/rbs/dry_run", tags=["RBS API"], summary="Verify an RBS experiment")
    async def dry_run_rbs(rbs_experiment: RbsJobModel):
        return {"Verification": "Passed"}


def build_hw_endpoints(http_server, rbs_hardware):
    for key, daemon in rbs_hardware.dict().items():
        build_get_redirect(http_server, daemon['proxy'], daemon['url'], ["RBS API"])
        build_post_redirect(http_server, daemon['proxy'], daemon['url'], ["RBS API"])
        if daemon['type'] == 'caen':
            build_histogram_redirect(http_server, daemon['proxy'], daemon['url'], ["RBS API"])
            build_packed_histogram(http_server, daemon['proxy'], daemon['url'], ["RBS API"])
