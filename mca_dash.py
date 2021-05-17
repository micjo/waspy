from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
import config

from app.rbs_experiment.router import rbs_router as make_rbs_router
rbs_router = make_rbs_router(config.direct_urls, config.hardware_config)

from app.hardware_controllers.router import hw_router as make_hw_router
hw_router = make_hw_router(config.direct_urls, config.hardware_config)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(rbs_router)
app.include_router(hw_router)

@app.get("/", response_class=HTMLResponse, tags=["WebUI"])
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "config": config.hardware_config})

@app.get("/favicon.ico")
def favicon():
    return FileResponse('static/favicon.png')
