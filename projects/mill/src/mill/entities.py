from enum import Enum
from typing import Union, Dict, Optional, List

from pydantic.generics import BaseModel
from waspy.iba.rbs_entities import Detector


class DriverType(str, Enum):
    aml = 'aml'
    motrona_dx350 = 'motrona_dx350'
    caen = 'caen'
    mdrive = 'mdrive'
    mpa3 = 'mpa3'
    motrona_ax350 = 'motrona_ax350'
    mirion_g64 = 'mirion_g64'
    keithley = 'keithley'


class SimpleConfig(BaseModel):
    type: DriverType
    title: Optional[str]
    url: str
    proxy: Optional[str]

    class Config:
        use_enum_values = True


class AmlConfig(SimpleConfig):
    names: List[str]


class CaenConfig(SimpleConfig):
    detectors: List[Detector]


class AnyDriverGroup(BaseModel):
    __root__: Dict[str, Union[SimpleConfig, AmlConfig, CaenConfig]]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class AnyDriverConfig(BaseModel):
    drivers: AnyDriverGroup
