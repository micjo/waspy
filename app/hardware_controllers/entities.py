from typing import List, Union, Dict, Optional

from pydantic.generics import BaseModel
from enum import Enum


class HwControllerType(str, Enum):
    aml = 'aml'
    motrona = 'motrona'
    caen = 'caen'
    mdrive = 'mdrive'
    mpa3 = 'mpa3'


class SimpleConfig(BaseModel):
    type: HwControllerType
    title: str
    url: str
    proxy: Optional[str]
    trend: Optional[Dict]

    class Config:
        use_enum_values = True


class MdriveConfig(SimpleConfig):
    load: float
    proxy: Optional[str]


class AmlConfig(SimpleConfig):
    names: List[str]
    loads: List[float]


class AnyHardware(BaseModel):
    __root__: Dict[str, Union[AmlConfig, SimpleConfig]]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class AnyConfig(BaseModel):
    hardware: AnyHardware
