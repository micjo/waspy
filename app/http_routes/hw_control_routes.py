import requests
from fastapi import APIRouter, status, Response
from pydantic import create_model
from app.setup.entities import DaemonConfig
import app.http_routes.http_helper as http
from app.hardware_controllers.hw_control import get_caen_histogram, pack

router = APIRouter()


def _build_get_api(key, daemon):
    @router.get("/api/" + key, tags=["Daemon API"])
    async def api_key_get(response: Response):  # type: ignore
        try:
            response.status_code, resp = await http.get_json_with_response_code(daemon.url)
        except Exception as e:
            response.status_code = status.HTTP_404_NOT_FOUND
            resp = str(e)
        return resp


def _build_histogram_api(key, daemon):
    @router.get("/api/" + key + "/histogram/{board}-{channel}", tags=["Daemon API"])
    async def histogram(response: Response, board: int, channel: int):
        url = daemon.url + "/histogram/" + str(board) + "-" + str(channel)
        response.status_code, resp = await http.get_text_with_response_code(url)
        return resp


def _build_packed_histogram_api(key, daemon):
    @router.get("/api/" + key + "/histogram/{board}-{channel}/pack-{start}-{end}-{width}", tags=["Daemon API"])
    async def histogram(response: Response, board: int, channel: int, start: int, end: int, width: int):
        if width > 2048:
            response.status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
            return {}
        resp_code, data = await get_caen_histogram(daemon.url, board, channel)
        packed_data = pack(data, start, end, width)
        response.status_code = resp_code
        return packed_data


def _make_hw_schema(class_name, daemon):
    values = {}

    class BaseConfig:
        try:
            schema_extra = requests.get(daemon.url + "/caps").json()
        except:
            pass

    return create_model(class_name, **values, __config__=BaseConfig)


def _build_post_api(key, daemon):
    hw_schema = _make_hw_schema(key, daemon)

    @router.post("/api/" + key, tags=["Daemon API"])
    async def api_key_post(response: Response, hardware_command: hw_schema):  # type: ignore
        code, body = await http.post_dictionary(daemon.url, hardware_command.__root__)
        response.status_code = code
        return body


def build_api_endpoints(daemons: DaemonConfig):
    for any_key, any_daemon in daemons:
        _build_get_api(any_key, any_daemon)
        _build_post_api(any_key, any_daemon)



