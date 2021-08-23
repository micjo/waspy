import traceback

from fastapi import APIRouter, UploadFile, File, Response
from starlette import status

from app.setup.config import cfg
import app.rbs_experiment.folder_scanner as folder_scanner
from app.rbs_experiment.entities import RbsRqm, PauseModel
import app.rbs_experiment.random_csv_to_json as csv_convert
import logging


scanner = folder_scanner.FolderScanner()
router = APIRouter()


@router.get("/new/api/rbs/hw_config", tags=["RBS API"])
async def get_hw_config():
    return cfg.daemons.dict()


@router.get("/new/api/rbs/schedule", tags=["RBS API"])
async def get_schedule():
    path = cfg.input_dir.watch
    files = [file.name for file in sorted(path.iterdir()) if file.is_file()]
    return files


@router.get("/new/api/rbs/state", tags=["RBS API"])
async def get_rbs_experiment():
    rbs_state = scanner.get_state()
    return rbs_state


@router.post("/new/api/rbs/abort", tags=["RBS API"])
async def rbs_experiment_abort():
    scanner.abort()
    return ""


@router.post("/new/api/rbs/dry_run", tags=["RBS API"], summary="Verify an RBS experiment")
async def dry_run_rbs(rbs_experiment: RbsRqm):
    return {"Verification": "Passed"}


@router.post("/new/api/rbs/pause_dir_scan", tags=["RBS API"],
             summary="Start/stop scanning the configured directory for experiments to execute")
async def pause_rbs_dir_scan(request: PauseModel):
    scanner.pause_dir_scan(request.pause_dir_scan)


@router.post("/new/api/rbs/run", tags=["RBS API"], summary="Run an rbs experiment")
async def run_rbs(response: Response, job: RbsRqm):
    await pause_rbs_dir_scan(PauseModel(pause_dir_scan=True))
    file_path = cfg.input_dir.watch / job.rqm_number
    with open(file_path, "w") as f:
        f.write(job.json())
        f.flush()
    await pause_rbs_dir_scan(PauseModel(pause_dir_scan=False))


@router.post("/new/api/rbs/rqm_csv", tags=["RBS API"])
async def parse_rqm_csv(response: Response, file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        contents = file_bytes.decode('utf-8')
        top_section, detectors_section, recipes_section = csv_convert.get_sections(contents)
        settings = csv_convert.parse_top_settings(top_section)
        settings["detectors"] = csv_convert.parse_list_settings(detectors_section)
        settings["recipes"] = csv_convert.parse_recipes(recipes_section)
        RbsRqm.validate_recipes(settings)
        rbs_rqm = RbsRqm.parse_obj(settings)
        # await verify_caen_boards(settings["detectors"])
        return rbs_rqm
    except Exception as e:
        logging.error(traceback.format_exc())
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return str(e)
