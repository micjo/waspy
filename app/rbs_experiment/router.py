from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
import asyncio
import app.rbs_experiment.rbs_runner as rbs_runner
import app.rbs_experiment.entities as rbs
from app.setup import config
from app.rbs_experiment.entities import PauseModel

templates = Jinja2Templates(directory="templates")

runner = rbs_runner.RbsRunner()
router = APIRouter()


@router.on_event('startup')
async def router_startup():
    asyncio.create_task(runner.run_main())


@router.get("/rbs_hw", response_class=HTMLResponse, tags=["WebUI"])
async def rbs_hw(request: Request):
    return templates.TemplateResponse("rbs_hw.jinja2", {"request": request, "config": config.daemons.dict()})


@router.get("/api/rbs/state", tags=["RBS API"])
async def get_rbs_experiment():
    return runner.get_state()


@router.post("/api/rbs/abort", tags=["RBS API"])
async def rbs_experiment_abort():
    runner.abort()
    return ""


@router.post("/api/rbs/dry_run", tags=["RBS API"], summary="Verify an RBS experiment")
async def post_rbs_experiment(rbs_experiment: rbs.RbsRqm):
    return {"Verification": "Passed"}


@router.post("/api/rbs_channeling/run", tags=["RBS API"], summary="Verify an RBS experiment")
async def post_rbs_experiment(task_list: rbs.RbsRqm):
    return {"Verification": "Passed"}


@router.post("/api/rbs/pause_dir_scan", tags=["RBS API"],
             summary="Start/stop scanning the configured directory for experiments to execute")
async def pause_rbs_dir_scan(request: PauseModel):
    runner.pause_dir_scan(request.pause_dir_scan)
