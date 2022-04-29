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
import rbs_random_csv_to_json
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

    def make_job_model_from_csv(self, contents) -> Union[RbsJobModel, ErdJobModel]:
        sections = get_sections(contents)
        settings = {"job_id": sections[0][0]["job_id"], "job_type": sections[0][0]["job_type"]}

        if settings["job_type"] == "erd":
            settings["recipes"] = []
            for section_recipe in sections[1]:
                recipe = section_recipe
                if isnan(recipe["z_repeat"]):
                    recipe["z_repeat"] = 1
                settings["recipes"].append(recipe)
            return ErdJobModel.parse_obj(settings)

        elif settings["job_type"] == "rbs":
            settings["detectors"] = sections[1]
            settings["recipes"] = []

            for section_recipe in sections[2]:
                recipe = section_recipe
                recipe["start_position"] = RbsPosition.parse_obj(recipe)
                if recipe["type"] == RecipeType.random:
                    recipe["vary_coordinate"] = VaryCoordinate(name="phi", start=0, end=30, increment=2).dict()
                settings["recipes"].append(recipe)

            return RbsJobModel.parse_obj(settings)

    def make_rbs_job_model_from_csv(self, contents):
        top_section, detectors_section, recipes_section = rbs_random_csv_to_json.get_sections(contents)
        settings = rbs_random_csv_to_json.parse_top_settings(top_section)
        settings["detectors"] = rbs_random_csv_to_json.parse_list_settings(detectors_section)
        settings["recipes"] = rbs_random_csv_to_json.parse_recipes(recipes_section)
        self._rbs_setup.verify_caen_boards(settings["detectors"])
        return RbsJobModel.parse_obj(settings)

    def make_erd_job(self, job_model: ErdJobModel):
        return ErdJob(job_model, self._erd_setup, self._erd_data_serializer)

    def make_erd_job_model_from_csv(self, contents):
        return erd_csv_to_json.parse_rqm(contents)


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



class RbsJobFactory:
    def __init__(self, setup: RbsSetup, data_serializer: RbsDataSerializer):
        self._setup = setup
        self._data_serializer = data_serializer

    def make_job(self, job_model: RbsJobModel):
        return RbsJob(job_model, self._setup, self._data_serializer)

    def make_job_model_from_csv(self, contents):
        top_section, detectors_section, recipes_section = rbs_random_csv_to_json.get_sections(contents)
        settings = rbs_random_csv_to_json.parse_top_settings(top_section)
        settings["detectors"] = rbs_random_csv_to_json.parse_list_settings(detectors_section)
        settings["recipes"] = rbs_random_csv_to_json.parse_recipes(recipes_section)
        self._setup.verify_caen_boards(settings["detectors"])
        return RbsJobModel.parse_obj(settings)


class ErdJobFactory:
    def __init__(self, setup: ErdSetup, data_serializer: ErdDataSerializer):
        self._setup = setup
        self._data_serializer = data_serializer


