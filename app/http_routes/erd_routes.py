import logging
import queue
import traceback

from fastapi import APIRouter, UploadFile, Response, File, status

from app.erd.entities import ErdRqm, ErdHardware
from app.erd.erd_runner import ErdRunner
from app.http_routes.hw_control_routes import build_get_redirect, build_post_redirect
import app.erd.erd_csv_to_json as csv_convert

router = APIRouter()


def build_api_endpoints(erd_runner: ErdRunner, erd_hardware: ErdHardware):
    @router.post("/api/erd/run", tags=["ERD API"], summary="Run an ERD experiment")
    async def run_erd(job: ErdRqm):
        try:
            erd_runner.rqms.put(job, timeout=2)
        except queue.Full:
            return {"Queue is full"}

    for key, daemon in erd_hardware.dict().items():
        build_get_redirect(router, daemon['proxy'], daemon['url'], ["ERD API"])
        build_post_redirect(router, daemon['proxy'], daemon['url'], ["ERD API"])

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
