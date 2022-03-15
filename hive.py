import logging
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import app.rbs.rbs_setup as rbs_lib
from app.erd.data_serializer import ErdDataSerializer
from app.erd.erd_setup import ErdSetup
from app.hardware_controllers.entities import SimpleConfig
from app.http_routes import hw_control_routes, rbs_routes, erd_routes
from app.http_routes.systemd_routes import build_systemd_endpoints
from app.http_routes.trend_routes import build_trend_routes
from app.rbs.data_serializer import RbsDataSerializer
from app.rqm.job_runner import JobRunner
from app.setup.config import GlobalConfig, make_hive_config, HiveConfig
from app.trends.trend import Trend


def create_app():
    env_conf = GlobalConfig()
    logging.info("Loaded config: " + env_conf.json())
    hive_config = make_hive_config(env_conf.CONFIG_FILE)

    if env_conf.ENV_STATE == "dev":
        origins = ['http://localhost:3000']
    else:
        origins = ['http://localhost']
    app = FastAPI(docs_url=None, redoc_url=None, swagger_ui_parameters={"syntaxHighlight": False})
    app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})
    app.mount("/static", StaticFiles(directory="static"), name="static")

    hw_control_routes.build_conf_endpoint(app, hive_config)
    hw_control_routes.build_api_endpoints(app, hive_config.any.hardware)

    rbs_trender = build_trend(app, "rbs",
                              [SimpleConfig.parse_obj(y) for y in hive_config.rbs.hardware.__dict__.values()])
    erd_trender = build_trend(app, "erd",
                              [SimpleConfig.parse_obj(y) for y in hive_config.erd.hardware.__dict__.values()])
    any_trender = build_trend(app, "any",
                              [SimpleConfig.parse_obj(y) for y in hive_config.any.hardware.__root__.values()])

    build_rqm_listener(app, hive_config, [rbs_trender, any_trender], [erd_trender, any_trender])
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

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/favicon.ico")
    def favicon():
        return FileResponse('static/favicon.png')

    return app


def build_trend(router, name, to_trend: List[SimpleConfig]):
    trender = Trend(name, to_trend)
    trender.daemon = True
    trender.start()
    build_trend_routes(router, trender)
    return trender


def build_trending(router, hive_config: HiveConfig):
    rbs_trend_values = [SimpleConfig.parse_obj(y) for y in hive_config.rbs.hardware.__dict__.values()]
    erd_trend_values = [SimpleConfig.parse_obj(y) for y in hive_config.erd.hardware.__dict__.values()]
    any_trend_values = [SimpleConfig.parse_obj(y) for y in hive_config.any.hardware.__root__.values()]

    rbs_trender = Trend("rbs", rbs_trend_values)
    rbs_trender.daemon = True
    rbs_trender.start()
    build_trend_routes(router, rbs_trender)

    erd_trender = Trend("erd", erd_trend_values)
    erd_trender.daemon = True
    erd_trender.start()
    build_trend_routes(router, erd_trender)

    any_trender = Trend("any", any_trend_values)
    any_trender.daemon = True
    any_trender.start()
    build_trend_routes(router, any_trender)


def build_rqm_listener(router, hive_config: HiveConfig, rbs_trends: List[Trend], erd_trends: List[Trend]):
    rqm_runner = JobRunner()
    rbs_setup = rbs_lib.RbsSetup(hive_config.rbs.hardware)
    rbs_data_serializer = RbsDataSerializer(hive_config.rbs.data_dir)
    rbs_routes.build_api_endpoints(router, rqm_runner, rbs_data_serializer, rbs_setup, hive_config.rbs.hardware,
                                   rbs_trends)

    erd_setup = ErdSetup(hive_config.erd.hardware)
    erd_data_serializer = ErdDataSerializer(hive_config.erd.data_dir)
    erd_routes.build_api_endpoints(router, rqm_runner, erd_data_serializer, erd_setup, hive_config.erd.hardware,
                                   erd_trends)

    rqm_runner.daemon = True
    rqm_runner.start()
