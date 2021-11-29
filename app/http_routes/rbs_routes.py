from fastapi import APIRouter, UploadFile, File, Response
from starlette import status

from app.rbs.entities import RbsRqm, PauseModel, RbsConfig
from app.rbs.rqm_dispatcher import RqmDispatcher
import app.rbs.rbs_setup as rbs_lib
import logging
import traceback
import app.rbs.random_csv_to_json as csv_convert

router = APIRouter()

@router.post("/api/rbs/dry_run", tags=["RBS API"], summary="Verify an RBS experiment")
async def dry_run_rbs(rbs_experiment: RbsRqm):
    return {"Verification": "Passed"}


def build_api_endpoints(rqm_dispatcher: RqmDispatcher, rbs: rbs_lib.RbsSetup):
    @router.post("/api/rbs/run", tags=["RBS API"], summary="Run an rbs experiment")
    async def run_rbs(job: RbsRqm):
        rqm_dispatcher.add_rqm_to_queue(job)

    @router.get("/api/rbs/state", tags=["RBS API"], summary="Get the state of the active rqm")
    async def get_rqm_state():
        return rqm_dispatcher.get_state()

    @router.post("/api/rbs/abort", tags=["RBS API"], summary="Abort the running rqm")
    async def abort():
        rqm_dispatcher.abort()

    @router.get("/api/rbs/hw_config", tags=["RBS API"])
    async def get_hw_config():
        return rbs.hw

    @router.post("/api/rbs/rqm_csv", tags=["RBS API"])
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
            rbs.verify_caen_boards(settings["detectors"])
            return rbs_rqm
        except Exception as e:
            logging.error(traceback.format_exc())
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return str(e)
