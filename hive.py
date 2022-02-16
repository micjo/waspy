import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse

import app.rbs.rbs_setup as rbs_lib
from app.erd.data_serializer import ErdDataSerializer
from app.erd.erd_runner import ErdRunner
from app.erd.erd_setup import ErdSetup
from app.http_routes import hw_control_routes, rbs_routes, systemd_routes, erd_routes
from app.http_routes.systemd_routes import build_systemd_endpoints
from app.http_routes.trend_routes import build_trend_routes
from app.rbs.data_serializer import RbsDataSerializer
from app.rbs.rbs_runner import RbsRunner
from app.rbs.recipe_list_runner import RecipeListRunner
from app.rqm.rqm_runner import RqmRunner
from app.setup.config import GlobalConfig, make_hive_config
from app.trends.trend import Trend


def create_app():
    env_conf = GlobalConfig()
    logging.info("Loaded config: " + env_conf.json())
    hive_config = make_hive_config(env_conf.CONFIG_FILE)

    if env_conf.ENV_STATE == "dev":
        origins = ['http://localhost:3000']
    else:
        origins = ['http://localhost']
    app = FastAPI(docs_url=None, redoc_url=None)
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # hw_control_routes.build_api_endpoints(hive_config.rbs_config.hardware.dict())
    hw_control_routes.build_conf_endpoint(hive_config)
    hw_control_routes.build_api_endpoints(hive_config.any.hardware)
    app.include_router(hw_control_routes.router)

    rqm_runner = RqmRunner()
    rbs_setup = rbs_lib.RbsSetup(hive_config.rbs.hardware)
    rbs_data_serializer = RbsDataSerializer(hive_config.rbs.data_dir)
    recipe_list_scanner = RecipeListRunner(rbs_setup, rbs_data_serializer)
    # rqm_dispatcher = RbsRunner(recipe_list_scanner, rbs_data_serializer, rbs_setup)
    # rqm_dispatcher.daemon = True
    # rqm_dispatcher.start()
    rbs_routes.build_api_endpoints(rqm_runner, rbs_data_serializer, rbs_setup, hive_config.rbs.hardware)
    app.include_router(rbs_routes.router)

    rqm_runner.daemon= True
    rqm_runner.start()

    erd_setup = ErdSetup(hive_config.erd.hardware)
    erd_data_serializer = ErdDataSerializer(hive_config.erd.data_dir)
    # erd_runner = ErdRunner(erd_setup, erd_data_serializer)
    # erd_runner.daemon = True
    # erd_runner.start()
    # erd_routes.build_api_endpoints(erd_runner, hive_config.erd.hardware)
    # app.include_router(erd_routes.router)

    trend = Trend(hive_config)
    trend.daemon = True
    trend.start()
    build_trend_routes(app, trend)

    app.include_router(systemd_routes.router)
    build_systemd_endpoints(app, hive_config)


    app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                       allow_methods=['*'], allow_headers=['*'])

    @app.get("/", include_in_schema=False)
    async def custom_swagger_ui_html():
        text = get_swagger_ui_html(
            openapi_url="openapi.json",
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="static/swagger-ui-bundle.js",
            swagger_css_url="static/swagger-ui.css",
        )
        html = text.body
        # This is a somewhat nasty hack to disable syntax highlighting on the output. Syntax hightlighting makes rendering large
        # datasets extremely slow. Your browser will hang. Disabling it fixes it. A pull request is open for this, but
        # not integrated yet at this point (https://github.com/tiangolo/fastapi/pull/2568)
        html = html.replace(b"SwaggerUIBundle({", b"SwaggerUIBundle({syntaxHighlight:false,")
        return HTMLResponse(html)

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/favicon.ico")
    def favicon():
        return FileResponse('static/favicon.png')

    return app
