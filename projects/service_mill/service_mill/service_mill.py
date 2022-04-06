import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import rbs_setup as rbs_lib
from data_serializer import DataSerializer
from erd_data_serializer import ErdDataSerializer
from erd_setup import ErdSetup
import rbs_routes
import hw_control_routes
import erd_routes
from job_factory import RbsJobFactory, ErdJobFactory
from systemd_routes import build_systemd_endpoints
from logbook_db import LogBookDb
from rbs_data_serializer import RbsDataSerializer
from job_runner import JobRunner
from config import GlobalConfig, make_hive_config, HiveConfig


def create_app():
    env_conf = GlobalConfig()
    logging.info("Loaded config: " + env_conf.json())
    hive_config = make_hive_config(env_conf.CONFIG_FILE)

    if env_conf.ENV_STATE == "dev":
        origins = ['http://localhost:3000']
    else:
        origins = ['http://localhost']
    app = FastAPI(docs_url=None, redoc_url=None, swagger_ui_parameters={"syntaxHighlight": False})
    app.mount("/static", StaticFiles(directory="static"), name="static")

    hw_control_routes.build_conf_endpoint(app, hive_config)
    hw_control_routes.build_api_endpoints(app, hive_config.any.hardware)

    logbook_db = LogBookDb(env_conf.LOGBOOK_URL)

    build_rqm_listener(app, hive_config, logbook_db)
    build_systemd_endpoints(app, hive_config)

    app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                       allow_methods=['*'], allow_headers=['*'])

    @app.get("/", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url="openapi.json",
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="static/swagger-ui-bundle.js",
            swagger_css_url="static/swagger-ui.css",
            swagger_ui_parameters={"syntaxHighlight": False}
        )
    #
    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/favicon.ico")
    def favicon():
        return FileResponse('static/favicon.png')

    return app


def build_rqm_listener(router, hive_config: HiveConfig, logbook_db: LogBookDb):
    rqm_runner = JobRunner()

    rbs_setup = rbs_lib.RbsSetup(hive_config.rbs.hardware)
    rbs_data_serializer = RbsDataSerializer(DataSerializer(hive_config.rbs.data_dir), logbook_db)
    rbs_factory = RbsJobFactory(rbs_setup, rbs_data_serializer)
    rbs_routes.build_job_endpoints(router, rqm_runner, rbs_factory)
    rbs_routes.build_hw_endpoints(router, hive_config.rbs.hardware)

    erd_setup = ErdSetup(hive_config.erd.hardware)
    erd_data_serializer = ErdDataSerializer(DataSerializer(hive_config.erd.data_dir), logbook_db)
    erd_factory = ErdJobFactory(erd_setup, erd_data_serializer)

    erd_routes.build_api_endpoints(router, rqm_runner, erd_factory)
    erd_routes.build_hw_endpoints(router, hive_config.erd.hardware)

    rqm_runner.daemon = True
    rqm_runner.start()
