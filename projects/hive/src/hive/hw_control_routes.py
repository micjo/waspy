from typing import Dict, List

import requests
from fastapi import status, Response
from pydantic import create_model
from pydantic.generics import GenericModel

from waspy.hardware_control import http_helper as http
from hive.entities import AnyHardware
from waspy.hardware_control.hw_action import get_caen_histogram, pack, get_packed_histogram
from hive.config import HiveConfig
from waspy.hardware_control.rbs_entities import CaenDetector
from starlette.requests import Request


def build_api_endpoints(http_router, any_hardware: AnyHardware):
    for key, daemon in any_hardware.__root__.items():
        build_get_redirect(http_router, daemon.proxy, daemon.url, ["ANY API"])
        build_post_redirect(http_router, daemon.proxy, daemon.url, ["ANY API"])
        if daemon.type == 'caen':
            build_histogram_redirect(http_router, daemon.proxy, daemon.url, ["ANY API"])
            build_packed_histogram(http_router, daemon.proxy, daemon.url, ["ANY API"])
        if daemon.type == 'mpa3':
            build_mpa3_histogram_redirect(http_router, daemon.proxy, daemon.url, ["ANY API"])


def build_conf_endpoint(http_router, hive_config: HiveConfig):
    @http_router.get("/api/hive_config")
    async def api_get_hive_config():
        return hive_config


def build_histogram_redirect(some_router, from_url, to_url, tags):
    @some_router.get(from_url + "/histogram/{board_id}/{channel}", tags=tags)
    async def histogram(response: Response, board_id: str, channel: int):
        url = to_url + "/histogram/" + board_id + "/" + str(channel)
        response.status_code, resp = http.get_text_with_response_code(url)
        return resp


def histogram(response: Response, to_url, board: str, channel: int, start: int, end: int, width: int):
    if width > end - start:
        response.status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        return {}
    detector = CaenDetector(board=board, channel=channel, identifier="", bins_min=start, bins_max=end,
                            bins_width=width)
    resp_code, packed_data = get_packed_histogram(to_url, detector)
    response.status_code = resp_code
    return packed_data


def build_packed_histogram(some_router, from_url, to_url, tags):
    @some_router.get(from_url + "/histogram/{board}/{channel}/pack/{start}-{end}-{width}", tags=tags)
    async def get_any_histogram(response: Response, board: str, channel: int, start: int, end: int, width: int):
        return histogram(response, to_url, board, channel, start, end, width)


def build_detector_endpoints(some_router, from_url, to_url, detectors: List[CaenDetector], tags):
    for detector in detectors:
        @some_router.get(from_url + "/detector/" + detector.identifier, tags=tags)
        async def get_histogram(request: Request, response: Response):
            path = str(request.url.path)
            last_part = path.split("/")[-1]
            
            active_detector = next(some_detector for some_detector in detectors 
                    if some_detector.identifier == last_part)

            return histogram(response, to_url, active_detector.board, active_detector.channel, 
                    active_detector.bins_min, active_detector.bins_max, active_detector.bins_width)

        @some_router.get(from_url + "/detector/" + detector.identifier + "_compressed", tags=tags)
        async def get_histogram(request: Request, response: Response):
            path = str(request.url.path)
            last_part = path.split("/")[-1]

            active_detector = next(some_detector for some_detector in detectors
                                   if some_detector.identifier == last_part)

            return histogram(response, to_url, active_detector.board, active_detector.channel,
                             active_detector.bins_min, active_detector.bins_max, 1024)


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


def build_mpa3_histogram_redirect(some_router, from_url, to_url, tags):
    @some_router.get(from_url + "/histogram", tags=tags)
    async def histogram(response: Response):
        print(to_url)
        url = to_url + "/histogram"
        response.status_code, resp = http.get_text_with_response_code(url)
        return resp
