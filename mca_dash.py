from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.rbs_experiment.router import router as rbs_router
from app.hardware_controllers.router import router as hw_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/site", StaticFiles(directory="static", html=True), name="site")
app.include_router(rbs_router)
app.include_router(hw_router)
origins = [
    'http://localhost:3000',
    'http://localhost:8080',
]
app.add_middleware(CORSMiddleware, allow_origins= origins, allow_credentials=True,
                   allow_methods=['*'], allow_headers=['*'])


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


@app.get("/favicon.ico")
def favicon():
    return FileResponse('static/favicon.png')
