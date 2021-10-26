from typing import Dict

import requests
from fastapi import APIRouter, status, Response
from pydantic import create_model
from pydantic.generics import GenericModel

from app.hardware_controllers.entities import HwControllerConfig
import app.http_routes.async_http_helper as http
from app.hardware_controllers.hw_action import get_caen_histogram, pack
from app.setup.config import HiveConfig

router = APIRouter()


def _build_get_api(key, url):
    @router.get("/api/" + key, tags=["Daemon API"])
    async def api_key_get(response: Response):  # type: ignore
        try:
            response.status_code, resp = await http.get_json_with_response_code(url)
        except Exception as e:
            response.status_code = status.HTTP_404_NOT_FOUND
            resp = str(e)
        return resp


def _build_histogram_api(key, base_url):
    @router.get("/api/" + key + "/histogram/{board}-{channel}", tags=["Daemon API"])
    async def histogram(response: Response, board: int, channel: int):
        url = base_url + "/histogram/" + str(board) + "-" + str(channel)
        response.status_code, resp = await http.get_text_with_response_code(url)
        return resp


def _build_packed_histogram_api(key, base_url):
    @router.get("/api/" + key + "/histogram/{board}-{channel}/pack-{start}-{end}-{width}", tags=["Daemon API"])
    async def histogram(response: Response, board: int, channel: int, start: int, end: int, width: int):
        if width > 2048:
            response.status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
            return {}
        resp_code, data = get_caen_histogram(base_url, board, channel)
        packed_data = pack(data, start, end, width)
        response.status_code = resp_code
        return packed_data


def _make_hw_schema(class_name, url):
    values = {}

    class BaseSchema(GenericModel):
        __root__: Dict

        class Config:
            try:
                schema_extra = requests.get(url + "/caps").json()
            except:
                pass

    return create_model(class_name, **values, __base__=BaseSchema)


def _convert_snakecase_to_camelcase(text):
    return ''.join(word.title() for word in text.split('_'))


def _build_post_api(key, url):
    hw_schema = _make_hw_schema(_convert_snakecase_to_camelcase(key), url)

    @router.post("/api/" + key, tags=["Daemon API"])
    async def api_key_post(response: Response, hardware_command: hw_schema):  # type: ignore
        code, body = await http.post_dictionary(url, hardware_command.__root__)
        response.status_code = code
        return body


def build_api_endpoints(daemon_config: HwControllerConfig):
    for key, daemon in daemon_config.controllers.items():
        _build_get_api(key, daemon.url)
        _build_post_api(key, daemon.url)
        if daemon.type == "caen":
            _build_histogram_api(key, daemon.url)
            _build_packed_histogram_api(key, daemon.url)


def build_conf_endpoint(hive_config: HiveConfig):
    @router.get("/api/hive_config")
    async def api_get_hive_config():
        return hive_config


