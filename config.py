from pydantic.generics import BaseModel
from enum import Enum

class DaemonType(str, Enum):
    aml= 'aml'
    motrona= 'motrona'
    caen= 'caen'

class DaemonUrls(BaseModel):
    motrona_rbs: str
    aml_x_y: str
    aml_det_theta: str
    aml_phi_zeta: str
    caen_charles_evans: str

class AmlConfig(BaseModel):
    type: DaemonType
    title: str
    first_name: str
    second_name: str
    first_load: int
    second_load: int
    class Config:
        use_enum_values = True

class SimpleConfig(BaseModel):
    type: DaemonType
    title: str
    class Config:
        use_enum_values = True

class DaemonConfig(BaseModel):
    aml_x_y: AmlConfig
    aml_phi_zeta: AmlConfig
    aml_det_theta: AmlConfig
    motrona_rbs: SimpleConfig
    caen_charles_evans: SimpleConfig
    class Config:
        use_enum_values = True

def makeDaemonConfig(json_data) -> DaemonConfig:
    return DaemonConfig.parse_raw(json_data)

def makeDaemonUrls(json_data) -> DaemonUrls:
    return DaemonUrls.parse_raw(json_data)

home_urls = makeDaemonUrls('''{
    "motrona_rbs": "http://127.0.0.1:22200/api/latest",
    "aml_x_y": "http://127.0.0.1:22100/api/latest",
    "aml_det_theta": "http://127.0.0.1:22100/api/latest",
    "aml_phi_zeta": "http://127.0.0.1:22100/api/latest",
    "caen_charles_evans": "http://127.0.0.1:22300/api/latest"
    }''')

lab_urls = makeDaemonUrls('''{
    "motrona_rbs": "http://127.0.0.1:23000/api/latest",
    "aml_x_y": "http://127.0.0.1:22000/api/latest",
    "aml_det_theta": "http://127.0.0.1:22001/api/latest",
    "aml_phi_zeta": "http://127.0.0.1:22002/api/latest",
    "caen_charles_evans": "http://169.254.13.109:22123/api/latest"
    }''')

urls = home_urls

daemons = makeDaemonConfig('''{
    "aml_x_y" : {"type":"aml", "title": "AML X Y", "first_name":"X", "second_name":"Y", "first_load":72.50, "second_load":61.7},
    "aml_phi_zeta" : {"type":"aml", "title": "AML Phi Zeta", "first_name":"Phi", "second_name":"Zeta", "first_load":0.00, "second_load":-1.00},
    "aml_det_theta" : {"type":"aml", "title": "AML Det Theta", "first_name":"Detector", "second_name":"Theta", "first_load":170.00, "second_load":-180.50},
    "motrona_rbs" : {"type":"motrona", "title" : "Motrona RBS"},
    "caen_charles_evans" : {"type":"caen", "title":"CAEN Charles Evans" }
    }''')

watch_dir = "/tmp/watch/"
