import queue
from fastapi import APIRouter

from app.erd.entities import ErdRqm
from app.erd.erd_runner import ErdRunner

router = APIRouter()


def build_api_endpoints(erd_runner: ErdRunner):
    @router.post("/api/erd/run", tags=["ERD API"], summary="Run an ERD experiment")
    async def run_erd(job: ErdRqm):
        try:
            erd_runner.rqms.put(job, timeout=2)
        except queue.Full:
            return {"Queue is full"}
