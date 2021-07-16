from fastapi import FastAPI, Request
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from app.setup import config

from app.rbs_experiment.router import router as rbs_router
from app.hardware_controllers.router import router as hw_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(docs_url=None, redoc_url=None)
origins = [
    'http://localhost:3000',
]
app.add_middleware(CORSMiddleware, allow_origins= origins, allow_credentials=True,
                   allow_methods=['*'], allow_headers=['*'])

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.mount("/site", StaticFiles(directory="static", html = True), name="site")

app.include_router(rbs_router)
app.include_router(hw_router)


# @app.get("/", response_class=HTMLResponse, tags=["WebUI"])
# async def dashboard(request: Request):
#     return templates.TemplateResponse("dashboard.jinja2", {"request": request, "config": config.daemons.dict()})


@app.get("/favicon.ico")
def favicon():
    return FileResponse('static/favicon.png')


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )

# app.mount("/dash", WSGIMiddleware(app_dash.server))
