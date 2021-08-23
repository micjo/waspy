from app.setup.config import cfg

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.http_routes import hw_control_routes, rbs_routes
from fastapi.middleware.cors import CORSMiddleware
from app.rbs_experiment.folder_scanner import scanner



def create_app():
    # app = FastAPI(docs_url=None, redoc_url=None, servers=[
    #     {"url": "http://169.254.150.200/hive"},
    #     {"url": "http://localhost/hive", "description": "Local Proxy environment"},
    #     {"url": "http://localhost:8000/", "description": "Local Direct environment"}
    # ])
    app = FastAPI(docs_url=None, redoc_url=None)
    app.mount("/static", StaticFiles(directory="static"), name="static")

    hw_control_routes.build_api_endpoints(cfg.daemons)
    app.include_router(hw_control_routes.router)

    scanner.run_main()
    app.include_router(rbs_routes.router)
    origins = [
        'http://localhost',
        'http://localhost:8000',
        'http://169.254.150.200',
    ]
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
