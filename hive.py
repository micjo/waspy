from app.erd.erd_runner import ErdRunner
from app.erd.erd_setup import ErdSetup
from app.rbs.data_serializer import RbsDataSerializer
from app.rbs.recipe_list_runner import RecipeListRunner
from app.rbs.rqm_dispatcher import RqmDispatcher
from app.setup.config import GlobalConfig, make_hive_config
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.http_routes import hw_control_routes, rbs_routes, systemd_routes, erd_routes
import app.rbs.rbs_setup as rbs_lib
from fastapi.middleware.cors import CORSMiddleware
import logging


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

    hw_control_routes.build_api_endpoints(hive_config.hw_config)
    hw_control_routes.build_conf_endpoint(hive_config)
    app.include_router(hw_control_routes.router)

    rbs_setup = rbs_lib.RbsSetup(hive_config.rbs_config.hardware)
    rbs_data_serializer = RbsDataSerializer(hive_config.rbs_config.data_dir)
    recipe_list_scanner = RecipeListRunner(rbs_setup, rbs_data_serializer)
    rqm_dispatcher = RqmDispatcher(recipe_list_scanner, rbs_data_serializer, rbs_setup)
    rqm_dispatcher.daemon = True
    rqm_dispatcher.start()
    rbs_routes.build_api_endpoints(rqm_dispatcher, rbs_setup)
    app.include_router(rbs_routes.router)

    erd_setup = ErdSetup(hive_config.erd_config.hardware)
    erd_runner = ErdRunner(erd_setup)
    erd_runner.daemon = True
    erd_runner.start()
    erd_routes.build_api_endpoints(erd_runner)
    app.include_router(erd_routes.router)

    app.include_router(systemd_routes.router)

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
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/favicon.ico")
    def favicon():
        return FileResponse('static/favicon.png')

    return app
