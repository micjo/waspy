import config
import requests
from pydantic.generics import GenericModel
from typing import Dict

def get_page_type(hardware_type):
    if (hardware_type == "aml"): return "max_aml.html"
    if (hardware_type == "caen"): return "max_caen.html"
    if (hardware_type == "motrona"): return "max_motrona.html"
    return ""

class MotronaSchema(GenericModel):
    __root__: Dict
    class Config:
        try: schema_extra = requests.get(config.direct_urls.motrona_rbs + "/caps").json()
        except: pass

class CaenSchema(GenericModel):
    __root__: Dict
    class Config:
        try: schema_extra = requests.get(config.direct_urls.caen_charles_evans + "/caps").json()
        except: pass

class AmlSchema(GenericModel):
    __root__: Dict
    class Config:
        try: schema_extra = requests.get(config.direct_urls.aml_x_y + "/caps").json()
        except: pass

class NoSchema(GenericModel):
    __root__: Dict

def get_schema_type(hardware_type):
    Schema = NoSchema
    if hardware_type == "aml":
        Schema = AmlSchema
    if hardware_type == "motrona":
        Schema = MotronaSchema
    if hardware_type == "caen":
        Schema = CaenSchema

    return Schema

