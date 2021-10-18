import asyncio

from app.setup.config import cfg, env_conf
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.http_routes import hw_control_routes, rbs_routes
from fastapi.middleware.cors import CORSMiddleware
from app.rbs_experiment.task_runner import scanner
import socket


def create_app():
    if env_conf.ENV_STATE == "dev":
        origins = ['http://localhost:3000']
    else:
        origins = ['http://localhost']
    app = FastAPI(docs_url=None, redoc_url=None)
    app.mount("/static", StaticFiles(directory="static"), name="static")

    hw_control_routes.build_api_endpoints(cfg.daemonConfig)
    app.include_router(hw_control_routes.router)

    asyncio.create_task(scanner.run_main())
    app.include_router(rbs_routes.router)

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
