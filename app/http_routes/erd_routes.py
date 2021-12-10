import logging
import queue
import traceback

from fastapi import APIRouter, UploadFile, Response, File, status

from app.erd.entities import ErdRqm, ErdHardware
from app.erd.erd_runner import ErdRunner
from app.http_routes.hw_control_routes import build_get_redirect, build_post_redirect, build_mpa3_histogram_redirect
import app.erd.erd_csv_to_json as csv_convert

router = APIRouter()


def build_api_endpoints(erd_runner: ErdRunner, erd_hardware: ErdHardware):
    @router.post("/api/erd/run", tags=["ERD API"], summary="Run an ERD experiment")
    async def run_erd(job: ErdRqm):
        erd_runner.add_rqm_to_queue(job)

    for key, daemon in erd_hardware.dict().items():
        build_get_redirect(router, daemon['proxy'], daemon['url'], ["ERD API"])
        build_post_redirect(router, daemon['proxy'], daemon['url'], ["ERD API"])
        if daemon['type'] == 'mpa3':
            build_mpa3_histogram_redirect(router, daemon['proxy'], daemon['url'], ["ERD API"])

    @router.get("/api/erd/state", tags=["RBS API"], summary="Get the state of the active rqm")
    async def get_rqm_state():
        return erd_runner.get_state()

    @router.post("/api/erd/abort", tags=["RBS API"], summary="Abort the running rqm")
    async def abort():
        erd_runner.abort()

    @router.post("/api/erd/rqm_csv", tags=["ERD API"])
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
