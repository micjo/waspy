import random
from typing import Dict

import requests
from fastapi import APIRouter, status, Response
from pydantic import create_model
from pydantic.generics import GenericModel

import app.http_routes.http_helper as http
from app.hardware_controllers.entities import AnyHardware
from app.hardware_controllers.hw_action import get_caen_histogram, pack
from app.setup.config import HiveConfig


def build_histogram_redirect(some_router, from_url, to_url, tags):
    @some_router.get(from_url + "/histogram/{board}-{channel}", tags=tags)
    async def histogram(response: Response, board: int, channel: int):
        url = to_url + "/histogram/" + str(board) + "-" + str(channel)
        response.status_code, resp = http.get_text_with_response_code(url)
        return resp


def build_packed_histogram(some_router, from_url, to_url, tags):
    @some_router.get(from_url + "/histogram/{board}-{channel}/pack-{start}-{end}-{width}", tags=tags)
    async def histogram(response: Response, board: int, channel: int, start: int, end: int, width: int):
        if width > 2048:
            response.status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
            return {}
        resp_code, data = get_caen_histogram(to_url, board, channel)
        packed_data = pack(data, start, end, width)
        response.status_code = resp_code
        return packed_data


def _make_hw_schema(class_name, url):
    values = {}

    class BaseSchema(GenericModel):
        __root__: Dict

        class Config:
            try:
                schema_extra = requests.get(url + "/caps", timeout=5).json()
            except:
                pass

    return create_model(class_name, **values, __base__=BaseSchema)


def _convert_snakecase_to_camelcase(text):
    return ''.join(word.title() for word in text.split('_'))


def build_post_redirect(some_router, from_url, to_url, tags):
    hw_schema = _make_hw_schema(_convert_snakecase_to_camelcase(from_url), to_url)

    @some_router.post(from_url, tags=tags)
    async def api_key_post(response: Response, hardware_command: hw_schema):  # type: ignore
        code, body = http.post_dictionary(to_url, hardware_command.__root__)
        response.status_code = code
        return body


def build_get_redirect(some_router, from_url, to_url, tags):
    @some_router.get(from_url, tags=tags)
    async def api_key_get(response: Response):  # type: ignore
        try:
            response.status_code, resp = http.get_json_with_response_code(to_url)
        except Exception as e:
            response.status_code = status.HTTP_404_NOT_FOUND
            resp = str(e)
        return resp


router = APIRouter()


def build_mpa3_histogram_redirect(some_router, from_url, to_url, tags):
    @some_router.get(from_url + "/histogram", tags=tags)
    async def histogram(response: Response):
        print(to_url)
        url = to_url + "/histogram"
        response.status_code, resp = http.get_text_with_response_code(url)
        return resp


def build_api_endpoints(any_hardware: AnyHardware):
    @router.get("/api/some_number")
    async def get_random_number():
        return random.randint(0,20)

    for key, daemon in any_hardware.__root__.items():
        build_get_redirect(router, daemon.proxy, daemon.url, ["ANY API"])
        build_post_redirect(router, daemon.proxy, daemon.url, ["ANY API"])
        if daemon.type == 'caen':
            build_histogram_redirect(router, daemon.proxy, daemon.url, ["ANY API"])
            build_packed_histogram(router, daemon.proxy, daemon.url, ["ANY API"])
        if daemon.type == 'mpa3':
            build_mpa3_histogram_redirect(router, daemon.proxy, daemon.url, ["ANY API"])


def build_conf_endpoint(hive_config: HiveConfig):
    @router.get("/api/hive_config")
    async def api_get_hive_config():
        return hive_config
