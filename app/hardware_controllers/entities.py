from typing import List, Union, Dict, Optional

from pydantic.generics import BaseModel
from enum import Enum


class HwControllerType(str, Enum):
    aml = 'aml'
    motrona = 'motrona'
    caen = 'caen'
    mdrive = 'mdrive'
    mpa3 = 'mpa3'


class MdriveConfig(BaseModel):
    type: HwControllerType
    title: str
    url: str
    load: float
    proxy: Optional[str]
    trend: Optional[Dict]


class AmlConfig(BaseModel):
    type: HwControllerType
    title: str
    url: str
    names: List[str]
    loads: List[float]
    proxy: Optional[str]
    trend: Optional[Dict]

    class Config:
        use_enum_values = True


class SimpleConfig(BaseModel):
    type: HwControllerType
    title: str
    url: str
    proxy: Optional[str]
    trend: Optional[Dict]

    class Config:
        use_enum_values = True


class AnyHardware(BaseModel):
    __root__: Dict[str, Union[AmlConfig, SimpleConfig]]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class AnyConfig(BaseModel):
    hardware: AnyHardware
