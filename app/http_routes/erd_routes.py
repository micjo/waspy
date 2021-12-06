import queue
from fastapi import APIRouter

from app.erd.entities import ErdRqm, ErdHardware
from app.erd.erd_runner import ErdRunner
from app.http_routes.hw_control_routes import build_get_redirect, build_post_redirect

router = APIRouter()


def build_api_endpoints(erd_runner: ErdRunner, erd_hardware: ErdHardware):
    @router.post("/api/erd/run", tags=["ERD API"], summary="Run an ERD experiment")
    async def run_erd(job: ErdRqm):
        try:
            erd_runner.rqms.put(job, timeout=2)
        except queue.Full:
            return {"Queue is full"}

    for key, daemon in erd_hardware.dict().items():
        build_get_redirect(daemon['proxy'], daemon['url'], router, ["ERD API"])
        build_post_redirect(daemon['proxy'], daemon['url'], router, ["ERD API"])



