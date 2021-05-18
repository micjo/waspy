from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Response, status

import config
import aiohttp
from app.hardware_controllers.entities import get_schema_type, get_page_type

templates = Jinja2Templates(directory="templates")
session = aiohttp.ClientSession()

router = APIRouter()

for key, daemon in config.daemons:

    if daemon.type == "caen":
        @router.get("/api/" + key + "/histogram/{board}-{channel}", tags=["Daemon API"])
        async def histogram(request: Request, response: Response, board: int, channel: int):
            hardware_id = request.url.path.split("/")[2]
            try:
                bc = str(board) + "-" + str(channel)
                url = config.direct_urls.dict()[hardware_id]
                getHistogramSession = await session.get(url + "/histogram/" + bc)
                response.status_code = getHistogramSession.status
                resp = await getHistogramSession.text()
            except Exception as e:
                response.status_code = status.HTTP_400_BAD_REQUEST
                resp = str(e)
            return resp

    @router.get("/api/" + key, tags=["Daemon API"])
    async def api_key_get(request: Request, response: Response):
        hardware_id = request.url.path.split("/")[2]
        try:
            url = config.direct_urls.dict()[hardware_id]
            getSession = await session.get(url)
            response.status_code = getSession.status
            resp = await getSession.json()
        except Exception as e:
            response.status_code = status.HTTP_400_BAD_REQUEST
            resp = str(e)
        return resp

    HardwareSchema = get_schema_type(daemon.type)
    @router.post("/api/" + key, tags=["Daemon API"])
    async def api_key_post(request:Request, response:Response, hardware_command:HardwareSchema): # type: ignore
        hardware_id = request.url.path.split("/")[2]
        try:
            url = config.direct_urls.dict()[hardware_id]
            postSession = await session.post(url[hardware_id], json=hardware_command.__root__)
            response.status_code = postSession.status
            resp = await postSession.text()
        except Exception as e:
            response.status_code = status.HTTP_400_BAD_REQUEST
            resp = str(e)
        return resp

    @router.get("/hw/" + key, response_class=HTMLResponse, summary="WebUI for hardware",description="WebUI", tags=["WebUI"])
    async def hw(request:Request):
        hardware_id = request.url.path.split("/")[2]
        active_daemon = config.daemons.dict()[hardware_id]
        print(active_daemon)
        page_type = get_page_type(active_daemon["type"])
        return templates.TemplateResponse(page_type, {"request": request, "prefix": hardware_id, "config": active_daemon})
