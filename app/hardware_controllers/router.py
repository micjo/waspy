from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Response, status

import config
import aiohttp
from app.hardware_controllers.entities import get_schema_type, get_page_type

templates = Jinja2Templates(directory="templates")
session = aiohttp.ClientSession()

router = APIRouter()

def build_get_api(key, daemon):
    @router.get("/api/" + key, tags=["Daemon API"])
    async def api_key_get(response: Response): #type: ignore
        try:
            getSession = await session.get(daemon.url)
            response.status_code = getSession.status
            resp = await getSession.json()
        except Exception as e:
            response.status_code = status.HTTP_400_BAD_REQUEST
            resp = str(e)
        return resp

def build_histogram_api(key, daemon):
    @router.get("/api/" + key + "/histogram/{board}-{channel}", tags=["Daemon API"])
    async def histogram(response: Response, board: int, channel: int):
        try:
            bc = str(board) + "-" + str(channel)
            getHistogramSession = await session.get(daemon.url + "/histogram/" + bc)
            response.status_code = getHistogramSession.status
            resp = await getHistogramSession.text()
        except Exception as e:
            response.status_code = status.HTTP_400_BAD_REQUEST
            resp = str(e)
        return resp

def build_post_api(key, daemon):
    HardwareSchema = get_schema_type(daemon.type)
    @router.post("/api/" + key, tags=["Daemon API"])
    async def api_key_post(response:Response, hardware_command:HardwareSchema): # type: ignore
        try:
            postSession = await session.post(daemon.url, json=hardware_command.__root__)
            response.status_code = postSession.status
            resp = await postSession.text()
        except Exception as e:
            response.status_code = status.HTTP_400_BAD_REQUEST
            resp = str(e)
        return resp

def build_webui(key, daemon):
    @router.get("/hw/" + key, response_class=HTMLResponse, summary="WebUI for hardware",description="WebUI", tags=["WebUI"])
    async def hw(request:Request):
        page_type = get_page_type(daemon.type)
        return templates.TemplateResponse(page_type, {"request": request, "config": config.daemons.dict(), "prefix": key})

for key, daemon in config.daemons:
    if daemon.type == "caen":
        build_histogram_api(key, daemon)
    build_get_api(key, daemon)
    build_post_api(key, daemon)
    build_webui(key, daemon)



