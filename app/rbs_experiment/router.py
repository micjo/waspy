import asyncio

from app.rbs_experiment.entities import PauseModel
from app.setup import config
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import app.rbs_experiment.entities as rbs
import app.rbs_experiment.folder_scanner as folder_scanner

templates = Jinja2Templates(directory="templates")

scanner = folder_scanner.FolderScanner()
router = APIRouter()


@router.on_event('startup')
async def router_startup():
    asyncio.create_task(scanner.run_main())


@router.get("/rbs_hw", response_class=HTMLResponse, tags=["WebUI"])
async def rbs_hw(request: Request):
    return templates.TemplateResponse("rbs_hw.jinja2", {"request": request, "config": config.daemons.dict()})


@router.get("/api/rbs/state", tags=["RBS API"])
async def get_rbs_experiment():
    return scanner.get_state()


@router.post("/api/rbs/abort", tags=["RBS API"])
async def rbs_experiment_abort():
    scanner.abort()
    return ""


@router.post("/api/rbs/dry_run", tags=["RBS API"], summary="Verify an RBS experiment")
async def post_rbs_experiment(rbs_experiment: rbs.RbsRqm):
    return {"Verification": "Passed"}


@router.post("/api/rbs/pause_dir_scan", tags=["RBS API"],
             summary="Start/stop scanning the configured directory for experiments to execute")
async def pause_rbs_dir_scan(request: PauseModel):
    scanner.pause_dir_scan(request.pause_dir_scan)
