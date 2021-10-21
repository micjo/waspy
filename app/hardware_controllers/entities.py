from typing import List, Union, Dict

from pydantic.generics import BaseModel
from enum import Enum


class HwControllerType(str, Enum):
    aml = 'aml'
    motrona = 'motrona'
    caen = 'caen'
    mdrive = 'mdrive'


class AmlConfig(BaseModel):
    type: HwControllerType
    title: str
    url: str
    names: List[str]
    loads: List[float]

    class Config:
        use_enum_values = True


class SimpleConfig(BaseModel):
    type: HwControllerType
    title: str
    url: str

    class Config:
        use_enum_values = True


class HwControllerConfig(BaseModel):
    controllers: Dict[str, Union[AmlConfig, SimpleConfig]]
