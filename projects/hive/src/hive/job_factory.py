from io import StringIO
from typing import Union, Dict, List

import pandas as pd

from hive.erd_data_serializer import ErdDataSerializer
from hive.erd_entities import ErdJobModel
from hive.erd_job import ErdJob
from waspy.hardware_control.erd_setup import ErdSetup
from hive.rbs_data_serializer import RbsDataSerializer
from hive.rbs_entities import RbsJobModel, VaryCoordinate
from hive.rbs_job import RbsJob
from waspy.hardware_control.rbs_entities import PositionCoordinates
from waspy.hardware_control.rbs_setup import RbsSetup


class JobFactory:
    def __init__(self, rbs_setup: RbsSetup, rbs_data_serializer: RbsDataSerializer, erd_setup: ErdSetup,
                 erd_data_serializer: ErdDataSerializer):
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

        if settings["job_type"] == "erd":
            recipes_section = sections[1]
            print(recipes_section)
            settings["recipes"] = parse_erd_recipes(recipes_section)
            return ErdJobModel.parse_obj(settings)

        elif settings["job_type"] == "rbs":
            recipes_section = sections[1]
            settings["recipes"] = parse_rbs_recipes(recipes_section, self._rbs_setup)
            return RbsJobModel.parse_obj(settings)


def convert_csv_to_dict(csv) -> Dict:
    dataframe = pd.read_csv(StringIO(csv))
    dataframe = dataframe.dropna(how='all', axis='columns')
    data = dataframe.to_dict('records')
    return data


def get_sections(csv_text: str) -> List:
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


def drop_nan(data: Dict) -> Dict:
    return {k: v for k, v in data.items() if pd.notnull(v)}


def parse_erd_recipes(recipes_section):
    recipes = []
    for recipe in recipes_section:
        recipes.append(drop_nan(recipe))
    return recipes


def parse_rbs_recipes(recipes_section, rbs_setup: RbsSetup):
    recipes = []

    for input_recipe in recipes_section:
        if input_recipe["type"] == "rbs_random":
            recipes.append(parse_random_recipe(input_recipe))
        elif input_recipe["type"] == "rbs_channeling":
            recipe = parse_channeling_recipe(input_recipe)
            rbs_setup.get_detector(recipe["yield_optimize_detector_identifier"])
            recipes.append(recipe)
    return recipes


def parse_random_recipe(recipe_section: Dict) -> Dict:
    setting = drop_nan(recipe_section)
    convert_coordinates_to_position("start_position", setting)
    setting["vary_coordinate"] = VaryCoordinate(name="phi", start=0, end=30, increment=2).dict()
    return setting


def parse_channeling_recipe(recipe_section: Dict) -> Dict:
    setting = drop_nan(recipe_section)
    convert_coordinates_to_position("start_position", setting)
    setting["random_vary_coordinate"] = VaryCoordinate(name="phi", start=0, end=30, increment=2).dict()
    setting["random_fixed_charge_total"] = setting['charge_total']
    setting.pop("charge_total")
    setting["yield_vary_coordinates"] = [
        {"name": "zeta", "start": -2, "end": 2, "increment": 0.2},
        {"name": "theta", "start": -2, "end": 2, "increment": 0.2},
        {"name": "zeta", "start": -2, "end": 2, "increment": 0.2},
        {"name": "theta", "start": -2, "end": 2, "increment": 0.2},
    ]
    setting["yield_charge_total"] = setting["ays_charge"]
    setting.pop("ays_charge")
    setting["yield_optimize_detector_identifier"] = setting["ays_detector_identifier"]
    setting.pop("ays_detector_identifier")
    setting["random_vary_coordinate"] = {"name": "phi", "start": 0, "end": 30, "increment": 2}
    setting["yield_integration_window"] = {}
    setting["yield_integration_window"]["start"] = setting["ays_window_start"]
    setting.pop("ays_window_start")
    setting["yield_integration_window"]["end"] = setting["ays_window_end"]
    setting.pop("ays_window_end")
    return setting


def convert_coordinates_to_position(position_key, setting):
    setting[position_key] = PositionCoordinates.parse_obj(setting).dict()
    setting.pop("x", None)
    setting.pop("y", None)
    setting.pop("phi", None)
    setting.pop("zeta", None)
    setting.pop("det", None)
    setting.pop("theta", None)
