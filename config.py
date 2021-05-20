from pydantic.generics import BaseModel
from enum import Enum

class DaemonType(str, Enum):
    aml= 'aml'
    motrona= 'motrona'
    caen= 'caen'

class AmlConfig(BaseModel):
    type: DaemonType
    title: str
    first_name: str
    second_name: str
    first_load: int
    second_load: int
    url: str
    class Config:
        use_enum_values = True

class SimpleConfig(BaseModel):
    type: DaemonType
    title: str
    url: str
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

daemons_local = makeDaemonConfig('''{
    "aml_x_y" : {"type":"aml", "title": "AML X Y", "first_name":"X", "second_name":"Y", "first_load":72.50, "second_load":61.7, "url": "http://127.0.0.1:22100/api/latest"},
    "aml_det_theta" : {"type":"aml", "title": "AML Det Theta", "first_name":"Detector", "second_name":"Theta", "first_load":170.00, "second_load":-180.50, "url":"http://127.0.0.1:22100/api/latest"},
    "aml_phi_zeta" : {"type":"aml", "title": "AML Phi Zeta", "first_name":"Phi", "second_name":"Zeta", "first_load":0.00, "second_load":-1.00, "url":"http://127.0.0.1:22100/api/latest"},
    "motrona_rbs" : {"type":"motrona", "title" : "Motrona RBS", "url":"http://127.0.0.1:22200/api/latest"},
    "caen_charles_evans" : {"type":"caen", "title":"CAEN Charles Evans", "url":"http://127.0.0.1:22300/api/latest" }
    }''')

daemons_lab = makeDaemonConfig('''{
    "aml_x_y" : {"type":"aml", "title": "AML X Y", "first_name":"X", "second_name":"Y", "first_load":72.50, "second_load":61.7, "url": "http://127.0.0.1:22000/api/latest"},
    "aml_det_theta" : {"type":"aml", "title": "AML Det Theta", "first_name":"Detector", "second_name":"Theta", "first_load":170.00, "second_load":-180.50, "url":"http://127.0.0.1:22001/api/latest"},
    "aml_phi_zeta" : {"type":"aml", "title": "AML Phi Zeta", "first_name":"Phi", "second_name":"Zeta", "first_load":0.00, "second_load":-1.00, "url":"http://127.0.0.1:22002/api/latest"},
    "motrona_rbs" : {"type":"motrona", "title" : "Motrona RBS", "url":"http://127.0.0.1:23000/api/latest"},
    "caen_charles_evans" : {"type":"caen", "title":"CAEN Charles Evans", "url":"http://169.254.13.109:22123/api/latest" }
    }''')

daemons = daemons_local

watch_dir = "/tmp/watch/"
