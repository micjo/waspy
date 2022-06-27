from io import StringIO
from math import isnan
from typing import Union, Dict, List

import pandas as pd

from erd_data_serializer import ErdDataSerializer
from erd_entities import ErdJobModel
from erd_job import ErdJob
from hive.hardware_control.erd_setup import ErdSetup
from hive.hardware_control.rbs_entities import PositionCoordinates as RbsPosition
from hive.hardware_control.erd_entities import PositionCoordinates as ErdPosition
from rbs_data_serializer import RbsDataSerializer
from rbs_entities import RbsJobModel, RecipeType, VaryCoordinate
from rbs_job import RbsJob
import rbs_csv_to_json
import erd_csv_to_json
from hive.hardware_control.rbs_setup import RbsSetup
import csv


class JobFactory:
    def __init__(self, rbs_setup: RbsSetup, rbs_data_serializer: RbsDataSerializer, erd_setup: ErdSetup,
                 erd_data_serializer:ErdDataSerializer):
        self._rbs_setup = rbs_setup
        self._rbs_data_serializer = rbs_data_serializer
        self._erd_setup = erd_setup
        self._erd_data_serializer = erd_data_serializer

    def make_rbs_job(self, job_model: RbsJobModel):
        return RbsJob(job_model, self._rbs_setup, self._rbs_data_serializer)

    def make_erd_job(self, job_model: ErdJobModel):
        return ErdJob(job_model, self._erd_setup, self._erd_data_serializer)

    def make_job_model_from_csv(self, contents) -> Union[RbsJobModel, ErdJobModel]:
        sections = get_sections(contents)
        top_section = sections[0][0]
        settings = top_section
        print(top_section)

        if settings["job_type"] == "erd":
            recipes_section = sections[1]
            settings["recipes"] = erd_csv_to_json.parse_recipes(recipes_section)
            return ErdJobModel.parse_obj(settings)

        elif settings["job_type"] == "rbs":
            # settings["detectors"] = sections[1]
            # self._rbs_setup.verify_caen_boards(settings["detectors"])

            recipes_section = sections[1]
            settings["recipes"] = rbs_csv_to_json.parse_rbs_recipes(recipes_section)
            return RbsJobModel.parse_obj(settings)


def convert_csv_to_dict(csv) -> Dict:
    dataframe = pd.read_csv(StringIO(csv))
    dataframe = dataframe.dropna(how='all', axis='columns')
    data = dataframe.to_dict('records')
    return data


def get_sections(csv_text: str)-> List:
    section_text = ""
    sections = []
    for line in csv_text.splitlines(keepends=True):
        if not line.startswith(",,"):
            section_text += line
        else:
            sections.append(convert_csv_to_dict(section_text))
            section_text = ""

    sections.append(convert_csv_to_dict(section_text))


    return sections
