from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Response, status

from app.setup import config
from app.hardware_controllers.entities import get_schema_type, get_page_type
from app.hardware_controllers import http_helper as http

templates = Jinja2Templates(directory="templates")

router = APIRouter()


def build_get_api(key, daemon):
    @router.get("/api/" + key, tags=["Daemon API"])
    async def api_key_get(response: Response):  # type: ignore
        try:
            response.status_code, resp = await http.get_json_with_response_code(daemon.url)
        except Exception as e:
            response.status_code = status.HTTP_404_NOT_FOUND
            resp = str(e)
        return resp


def build_histogram_api(key, daemon):
    @router.get("/api/" + key + "/histogram/{board}-{channel}", tags=["Daemon API"])
    async def histogram(response: Response, board: int, channel: int):
        url = daemon.url + "/histogram/" + str(board) + "-" + str(channel)
        response.status_code, resp = await http.get_text_with_response_code(url)
        return resp


def build_post_api(key, daemon):
    hardware_schema = get_schema_type(daemon.type)

    @router.post("/api/" + key, tags=["Daemon API"])
    async def api_key_post(response: Response, hardware_command: hardware_schema):  # type: ignore
        code, body = await http.post_dictionary(daemon.url, hardware_command.__root__)
        response.status_code = code
        return body


def build_webui(key, daemon):
    @router.get("/hw/" + key, response_class=HTMLResponse, summary="WebUI for hardware", description="WebUI",
                tags=["WebUI"])
    async def hw(request: Request):
        page_type = get_page_type(daemon.type)
        return templates.TemplateResponse(page_type,
                                          {"request": request, "config": config.daemons.dict(), "prefix": key})


for any_key, any_daemon in config.daemons:
    if any_daemon.type == "caen":
        build_histogram_api(any_key, any_daemon)
    build_get_api(any_key, any_daemon)
    build_post_api(any_key, any_daemon)
    build_webui(any_key, any_daemon)
