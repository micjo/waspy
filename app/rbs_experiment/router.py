from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
import asyncio
import app.rbs_experiment.rbs_experiment as rbs
import config
from app.rbs_experiment.entities import RbsSchema

templates = Jinja2Templates(directory="templates")

runner = rbs.RbsExperiment()
router = APIRouter()

@router.on_event('startup')
async def router_startup():
    asyncio.create_task(runner.run_main())

@router.get("/rbs_hw", response_class=HTMLResponse, tags=["WebUI"])
async def rbs_hw(request: Request):
    return templates.TemplateResponse("rbs_hw.html", {"request":request, "config": config.daemons.dict()})

@router.get("/api/exp/rbs", tags=["RBS API"])
async def get_rbs_experiment():
    return runner.status

@router.post("/api/exp/rbs_dry_run", tags=["RBS API"], summary="Verify an RBS experiment")
async def post_rbs_experiment(rbs_experiment: RbsSchema):   # type : ignore
    return {"Verification" : "Passed", "experiment": rbs_experiment}


