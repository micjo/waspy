import traceback

from fastapi import APIRouter, UploadFile, File, Response
from starlette import status

from app.rbs_experiment.entities import RbsRqm, PauseModel, RbsConfig
import app.rbs_experiment.random_csv_to_json as csv_convert
import logging

from app.rbs_experiment.recipe_list_runner import RecipeListRunner
from app.rbs_experiment.rqm_dispatcher import RqmDispatcher

router = APIRouter()

# -> RecipeListRunner
# @router.get("/api/rbs/hw_config", tags=["RBS API"])
# async def get_hw_config():
#     hw_conf = cfg.hw_config.dict()
#     for key in hw_conf.keys():
#         hw_conf[key]["proxy"] = "/api/" + key
#     hw_conf["rbs"] = {"proxy": "/api/rbs/"}
#     return hw_conf

# @router.get("/api/rbs/schedule", tags=["RBS API"])
# async def get_schedule():
#     path = cfg.input_dir.watch
#     files = [file.name for file in sorted(path.iterdir()) if file.is_file()]
#     return files
#
#

# @router.get("/api/rbs/state", tags=["RBS API"])
# async def get_rbs_experiment():
#     rbs_state = scanner.get_state()
#     return rbs_state



# @router.post("/api/rbs/abort", tags=["RBS API"])
# async def rbs_experiment_abort():
#     scanner.abort()
#     return ""


@router.post("/api/rbs/dry_run", tags=["RBS API"], summary="Verify an RBS experiment")
async def dry_run_rbs(rbs_experiment: RbsRqm):
    return {"Verification": "Passed"}


# @router.post("/api/rbs/pause_dir_scan", tags=["RBS API"],
#              summary="Start/stop scanning the configured directory for experiments to execute")
# async def pause_rbs_dir_scan(request: PauseModel):
#     scanner.pause_dir_scan(request.pause_dir_scan)
#
#

def build_api_endpoints(rqm_dispatcher: RqmDispatcher, recipe_list_runner: RecipeListRunner):
    @router.post("/api/rbs/run", tags=["RBS API"], summary="Run an rbs experiment")
    async def run_rbs(response: Response, job: RbsRqm):
        rqm_dispatcher.add_rqm_to_queue(job)

    @router.get("/api/rbs/state", tags=["RBS API"], summary="Get the state of the active rqm")
    async def get_rqm_state(response: Response):
        print(recipe_list_runner.get_status())
        return recipe_list_runner.get_status()

    @router.get("/api/rbs/abort", tags=["RBS API"], summary="Abort the running rqm")
    async def abort(response: Response):
        rqm_dispatcher.abort()




# @router.post("/api/rbs/rqm_csv", tags=["RBS API"])
# async def parse_rqm_csv(response: Response, file: UploadFile = File(...)):
#     try:
#         file_bytes = await file.read()
#         contents = file_bytes.decode('utf-8')
#         top_section, detectors_section, recipes_section = csv_convert.get_sections(contents)
#         settings = csv_convert.parse_top_settings(top_section)
#         settings["detectors"] = csv_convert.parse_list_settings(detectors_section)
#         settings["recipes"] = csv_convert.parse_recipes(recipes_section)
#         RbsRqm.validate_recipes(settings)
#         rbs_rqm = RbsRqm.parse_obj(settings)
#         await verify_caen_boards(settings["detectors"])
#         return rbs_rqm
#     except Exception as e:
#         logging.error(traceback.format_exc())
#         response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
#         return str(e)
