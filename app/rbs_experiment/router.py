import asyncio
import traceback

from app.rbs_experiment.entities import PauseModel
from app.setup import config
from fastapi import APIRouter, Request, Response, status
from fastapi import File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import app.rbs_experiment.entities as rbs
import app.rbs_experiment.random_csv_to_json as csv_convert
import app.rbs_experiment.folder_scanner as folder_scanner
import logging
import json

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
async def dry_run_rbs(rbs_experiment: rbs.RbsRqm):
    return {"Verification": "Passed"}


@router.post("/api/rbs/pause_dir_scan", tags=["RBS API"],
             summary="Start/stop scanning the configured directory for experiments to execute")
async def pause_rbs_dir_scan(request: PauseModel):
    scanner.pause_dir_scan(request.pause_dir_scan)


@router.post("/api/rbs/run", tags=["RBS API"], summary="Run an rbs experiment")
async def run_rbs(response: Response, file: UploadFile = File(...)):
    await pause_rbs_dir_scan(PauseModel(pause_dir_scan=True))
    file_path = config.input_dir.watch / file.filename
    file_bytes = await file.read()
    with open(file_path, "w") as f:
        f.write(file_bytes.decode("utf-8"))
        f.flush()
    await pause_rbs_dir_scan(PauseModel(pause_dir_scan=False))


@router.post("/api/rbs/rqm_csv", tags=["RBS API"])
async def parse_rqm_csv(response: Response, file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        contents = file_bytes.decode('utf-8')
        top_section, detectors_section, recipes_section = csv_convert.get_sections(contents)
        settings = csv_convert.parse_top_settings(top_section)
        settings["detectors"] = csv_convert.parse_list_settings(detectors_section)
        settings["recipes"] = csv_convert.parse_recipes(recipes_section)
        rbs.RbsRqm.validate_recipes(settings)
        rbs_rqm = rbs.RbsRqm.parse_obj(settings)
        return rbs_rqm
    except Exception as e:
        logging.error(traceback.format_exc())
        print(traceback.format_exc())
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return str(e)
