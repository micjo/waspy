import requests
from pydantic.generics import GenericModel
from typing import Dict
from app.setup.config import daemons

def get_page_type(hardware_type):
    if (hardware_type == "aml"): return "max_aml.jinja2"
    if (hardware_type == "caen"): return "max_caen.jinja2"
    if (hardware_type == "motrona"): return "max_motrona.jinja2"
    return ""

class MotronaSchema(GenericModel):
    __root__: Dict
    class Config:
        try: schema_extra = requests.get(daemons.motrona_rbs.url + "/caps").json()
        except: pass

class CaenSchema(GenericModel):
    __root__: Dict
    class Config:
        try: schema_extra = requests.get(daemons.caen_charles_evans.url + "/caps").json()
        except: pass

class AmlSchema(GenericModel):
    __root__: Dict
    class Config:
        try: schema_extra = requests.get(daemons.aml_x_y.url + "/caps").json()
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

