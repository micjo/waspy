import requests, json
import asyncio
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Request, Response, status
from pydantic.generics import GenericModel, create_model, BaseModel
from enum import Enum
from typing import Dict, List, Set

import config
import aiohttp

templates = Jinja2Templates(directory="templates")

session = aiohttp.ClientSession()

def get_page_type(hardwareType):
    if (hardwareType == "aml"): return "max_aml.html"
    if (hardwareType == "caen"): return "max_caen.html"
    if (hardwareType == "motrona"): return "max_motrona.html"
    return ""

class MotronaSchema(GenericModel):
    __root__: Dict
    class Config:
        try: schema_extra = requests.get(config.direct_urls["motrona_rbs"] + "/caps").json()
        except: pass

class CaenSchema(GenericModel):
    __root__: Dict
    class Config:
        try: schema_extra = requests.get(config.direct_urls["caen_charles_evans"] + "/caps").json()
        except: pass

class AmlSchema(GenericModel):
    __root__: Dict
    class Config:
        try: schema_extra = requests.get(config.direct_urls["aml_x_y"] + "/caps").json()
        except: pass

class NoSchema(GenericModel):
    __root__: Dict


def hw_router(direct_url_config, hardware_config):
    router = APIRouter()

    for key in hardware_config:
        Schema = NoSchema
        if hardware_config[key]["type"] == "aml":
            Schema = AmlSchema
        if hardware_config[key]["type"] == "motrona":
            Schema = MotronaSchema
        if hardware_config[key]["type"] == "caen":
            Schema = CaenSchema

            @router.get("/api/" + key + "/histogram/{board}-{channel}", tags=["WebUI"])
            async def histogram(request: Request, response: Response, board: int, channel: int):
                hw_request = request.url.path.split("/")[2]
                try:
                    bc = str(board) + "-" + str(channel)
                    getHistogramSession = await session.get(direct_url_config[hw_request] + "/histogram/" + bc)
                    response.status_code = getHistogramSession.status
                    resp = await getHistogramSession.text()
                except Exception as e:
                    response.status_code = status.HTTP_400_BAD_REQUEST
                    resp = str(e)
                return resp


        @router.get("/api/" + key, tags=["hardware api"])
        async def api_key_get(request: Request, response: Response):
            hw_request = request.url.path.split("/")[2]
            try:
                getSession = await session.get(direct_url_config[hw_request])
                response.status_code = getSession.status
                resp = await getSession.json()
            except Exception as e:
                response.status_code = status.HTTP_400_BAD_REQUEST
                resp = str(e)
            return resp

        @router.post("/api/" + key, tags=["hardware api"])
        async def api_key_post(request:Request, response:Response, hardware_command:Schema):
            hw_request = request.url.path.split("/")[2]
            try:
                postSession = await session.post(direct_url_config[hw_request], json=hardware_command.__root__)
                response.status_code = postSession.status
                resp = await postSession.text()
            except Exception as e:
                response.status_code = status.HTTP_400_BAD_REQUEST
                resp = str(e)
            return resp

        @router.get("/hw/" + key, response_class=HTMLResponse, summary="WebUI for hardware",description="WebUI", tags=["WebUI"])
        async def hw(request:Request):
            hw_request = request.url.path.split("/")[2]
            hardware = hardware_config[hw_request]
            page_type = get_page_type(hardware["type"])
            return templates.TemplateResponse(page_type, {"request": request, "prefix": hw_request, "config": hardware})
    return router
