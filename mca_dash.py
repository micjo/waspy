from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
import config

from app.rbs_experiment.router import router as rbs_router
from app.hardware_controllers.router import router as hw_router
from app.trends.router import app_dash

from fastapi.middleware.wsgi import WSGIMiddleware



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(rbs_router)
app.include_router(hw_router)

@app.get("/", response_class=HTMLResponse, tags=["WebUI"])
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "config": config.daemons.dict()})

@app.get("/favicon.ico")
def favicon():
    return FileResponse('static/favicon.png')

app.mount("/dash", WSGIMiddleware(app_dash.server))
