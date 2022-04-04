from typing import List

from fastapi import APIRouter, UploadFile, File, Response, status

from app.http_routes.hw_control_routes import build_get_redirect, build_post_redirect, build_histogram_redirect, \
    build_packed_histogram
from app.job.logbook_post import LogBookDb
from app.rbs.data_serializer import RbsDataSerializer
from app.rbs.entities import RbsJobModel, RbsHardware
from app.job.rbs_job import RbsJob
from app.rbs.rbs_setup import RbsSetup
import logging
import traceback
import app.rbs.random_csv_to_json as csv_convert
from app.job.job_runner import JobRunner
from app.trends.trend import Trend


# TODO: Refactoring ( should use a factory for jobs to reduce the number of parameters to this function)
def build_api_endpoints(http_server, rqm_dispatcher: JobRunner, data_serializer: RbsDataSerializer, rbs_setup: RbsSetup,
                        rbs_hardware: RbsHardware, logbook_db: LogBookDb, trends: List[Trend]):
    @http_server.post("/api/rbs/run", tags=["RBS API"], summary="Run an rbs experiment")
    async def run_rbs(job: RbsJobModel):
        rqm_action = RbsJob(job, rbs_setup, data_serializer, logbook_db, trends)
        rqm_dispatcher.add_rqm_to_queue(rqm_action)

    @http_server.get("/api/rbs/state", tags=["RBS API"], summary="Get the state of the active rqm")
    async def get_rqm_state():
        return rqm_dispatcher.get_state()

    @http_server.post("/api/rbs/abort_active", tags=["RBS API"], summary="Abort the running rqm")
    async def abort_active():
        rqm_dispatcher.abort_active()

    @http_server.post("/api/rbs/abort_schedule", tags=["RBS API"], summary="Abort the scheduled rqms")
    async def abort_schedule():
        rqm_dispatcher.abort_schedule()

    @http_server.post("/api/rbs/rqm_csv", tags=["RBS API"])
    async def parse_rqm_csv(response: Response, file: UploadFile = File(...)):
        try:
            file_bytes = await file.read()
            contents = file_bytes.decode('utf-8')
            top_section, detectors_section, recipes_section = csv_convert.get_sections(contents)
            settings = csv_convert.parse_top_settings(top_section)
            settings["detectors"] = csv_convert.parse_list_settings(detectors_section)
            settings["recipes"] = csv_convert.parse_recipes(recipes_section)
            RbsJobModel.validate_recipes(settings)
            rbs_rqm = RbsJobModel.parse_obj(settings)
            rbs_setup.verify_caen_boards(settings["detectors"])
            return rbs_rqm
        except Exception as e:
            logging.error(traceback.format_exc())
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return str(e)

    @http_server.post("/api/rbs/dry_run", tags=["RBS API"], summary="Verify an RBS experiment")
    async def dry_run_rbs(rbs_experiment: RbsJobModel):
        return {"Verification": "Passed"}

    for key, daemon in rbs_hardware.dict().items():
        build_get_redirect(http_server, daemon['proxy'], daemon['url'], ["RBS API"])
        build_post_redirect(http_server, daemon['proxy'], daemon['url'], ["RBS API"])
        if daemon['type'] == 'caen':
            build_histogram_redirect(http_server, daemon['proxy'], daemon['url'], ["RBS API"])
            build_packed_histogram(http_server, daemon['proxy'], daemon['url'], ["RBS API"])
