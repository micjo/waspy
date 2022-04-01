import logging
import queue
import traceback
from typing import List

from fastapi import APIRouter, UploadFile, Response, File, status

from app.erd.data_serializer import ErdDataSerializer
from app.erd.entities import ErdJobModel, ErdHardware
from app.erd.erd_setup import ErdSetup
from app.http_routes.hw_control_routes import build_get_redirect, build_post_redirect, build_mpa3_histogram_redirect
import app.erd.erd_csv_to_json as csv_convert
from app.rqm.erd_job import ErdJob
from app.rqm.job_runner import JobRunner
from app.trends.trend import Trend


def build_api_endpoints(http_server, rqm_runner: JobRunner, data_serializer: ErdDataSerializer, erd_setup: ErdSetup,
                        erd_hardware: ErdHardware, trends: List[Trend]):
    @http_server.post("/api/erd/run", tags=["ERD API"], summary="Run an ERD experiment")
    async def run_erd(job: ErdJobModel):
        erd_action = ErdJob(job, erd_setup, data_serializer, trends)
        rqm_runner.add_rqm_to_queue(erd_action)

    @http_server.get("/api/erd/state", tags=["ERD API"], summary="Get the state of the active rqm")
    async def get_rqm_state():
        return rqm_runner.get_state()

    @http_server.post("/api/erd/abort_active", tags=["RBS API"], summary="Abort the running rqm")
    async def abort_active():
        rqm_runner.abort_active()

    @http_server.post("/api/erd/abort_schedule", tags=["RBS API"], summary="Abort the scheduled rqms")
    async def abort_schedule():
        rqm_runner.abort_schedule()

    @http_server.post("/api/erd/rqm_csv", tags=["ERD API"])
    async def parse_rqm_csv(response: Response, file: UploadFile = File(...)):
        try:
            file_bytes = await file.read()
            contents = file_bytes.decode('utf-8')
            erd_json = csv_convert.parse_rqm(contents)
            return erd_json
        except Exception as e:
            logging.error(traceback.format_exc())
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return str(e)

    for key, daemon in erd_hardware.dict().items():
        build_get_redirect(http_server, daemon['proxy'], daemon['url'], ["ERD API"])
        build_post_redirect(http_server, daemon['proxy'], daemon['url'], ["ERD API"])
        if daemon['type'] == 'mpa3':
            build_mpa3_histogram_redirect(http_server, daemon['proxy'], daemon['url'], ["ERD API"])
