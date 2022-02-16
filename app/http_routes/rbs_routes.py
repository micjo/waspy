from fastapi import APIRouter, UploadFile, File, Response, status

from app.http_routes.hw_control_routes import build_get_redirect, build_post_redirect, build_histogram_redirect, \
    build_packed_histogram
from app.rbs.data_serializer import RbsDataSerializer
from app.rbs.entities import RbsRqm, PauseModel, RbsConfig, RbsHardware
from app.rbs.rbs_runner import RbsRunner
from app.rqm.rbs_action_plan import RbsAction
import app.rbs.rbs_setup as rbs_lib
import logging
import traceback
import app.rbs.random_csv_to_json as csv_convert
from app.rqm.rqm_runner import RqmRunner

router = APIRouter()


@router.post("/api/rbs/dry_run", tags=["RBS API"], summary="Verify an RBS experiment")
async def dry_run_rbs(rbs_experiment: RbsRqm):
    return {"Verification": "Passed"}


def build_api_endpoints(rqm_dispatcher: RqmRunner, data_serializer: RbsDataSerializer, rbs: rbs_lib.RbsSetup,
                        rbs_hardware: RbsHardware):
    @router.post("/api/rbs/run", tags=["RBS API"], summary="Run an rbs experiment")
    async def run_rbs(job: RbsRqm):
        rqm_action = RbsAction(job, rbs, data_serializer)
        rqm_dispatcher.add_rqm_to_queue(rqm_action)

    @router.get("/api/rbs/state", tags=["RBS API"], summary="Get the state of the active rqm")
    async def get_rqm_state():
        state = rqm_dispatcher.get_state()
        return state

    @router.post("/api/rbs/abort_active", tags=["RBS API"], summary="Abort the running rqm")
    async def abort_active():
        rqm_dispatcher.abort_active()

    @router.post("/api/rbs/abort_schedule", tags=["RBS API"], summary="Abort the scheduled rqms")
    async def abort_schedule():
        rqm_dispatcher.abort_schedule()

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

    for key, daemon in rbs_hardware.dict().items():
        build_get_redirect(router, daemon['proxy'], daemon['url'], ["RBS API"])
        build_post_redirect(router, daemon['proxy'], daemon['url'], ["RBS API"])
        if daemon['type'] == 'caen':
            build_histogram_redirect(router, daemon['proxy'], daemon['url'], ["RBS API"])
            build_packed_histogram(router, daemon['proxy'], daemon['url'], ["RBS API"])
