import asyncio
import os
import traceback
from typing import List

from app.rbs_experiment.entities import PauseModel
from app.setup import config
from fastapi import APIRouter, Response, status
from fastapi import File, UploadFile
from fastapi.templating import Jinja2Templates
import app.rbs_experiment.entities as rbs
import app.rbs_experiment.random_csv_to_json as csv_convert
import app.rbs_experiment.folder_scanner as folder_scanner
import logging
import tomli
import app.hardware_controllers.http_helper as http

templates = Jinja2Templates(directory="templates")

scanner = folder_scanner.FolderScanner()
router = APIRouter()


@router.on_event('startup')
async def router_startup():
    asyncio.create_task(scanner.run_main())


@router.get("/api/rbs/hw_config", tags=["RBS API"])
async def get_hw_config():
    with open("./config.toml", "rb") as f:
        return tomli.load(f)


@router.get("/api/rbs/schedule", tags=["RBS API"])
async def get_schedule():
    path = config.input_dir.watch
    files = [file.name for file in sorted(path.iterdir()) if file.is_file()]
    return files


@router.get("/api/rbs/state", tags=["RBS API"])
async def get_rbs_experiment():
    rbs_state = scanner.get_state()
    return rbs_state


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
async def run_rbs(response: Response, job: rbs.RbsRqm):
    await pause_rbs_dir_scan(PauseModel(pause_dir_scan=True))
    file_path = config.input_dir.watch / job.rqm_number
    with open(file_path, "w") as f:
        f.write(job.json())
        f.flush()
    await pause_rbs_dir_scan(PauseModel(pause_dir_scan=False))


async def verify_caen_boards(detectors: List[rbs.CaenDetectorModel]):
    for detector in detectors:
        caen_data = await http.get_json(config.daemons.caen_rbs.url)
        if "board_" + str(detector['board']) not in caen_data:
            raise Exception("The specified board in the detector list does not exist")




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
        await verify_caen_boards(settings["detectors"])
        return rbs_rqm
    except Exception as e:
        logging.error(traceback.format_exc())
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return str(e)
