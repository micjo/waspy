import numpy as np
import pandas as pd
from io import StringIO
from typing import Dict, List

import hive.hardware_control.rbs_entities
import rbs_entities as rbs


def get_sections(csv_text: str):
    section_text = ""
    sections = []
    for line in csv_text.splitlines(keepends=True):
        if not line.startswith(",,"):
            section_text += line
        else:
            sections.append(section_text)
            section_text = ""
    sections.append(section_text)
    return sections


def drop_nan(data: Dict) -> Dict:
    return {k: v for k, v in data.items() if pd.notnull(v)}


def parse_top_settings(top_section: str) -> Dict:
    df = pd.read_csv(StringIO(top_section))
    job_id = str(df["job_id"][0])
    #TODO: better filename checkking (underscores are allowed , ...)
    top_settings = {"job_id": job_id}
    return top_settings


def parse_list_settings(list_section: str) -> List[Dict]:
    df = pd.read_csv(StringIO(list_section), dtype=object)
    return drop_nan(df.to_dict('records'))


def convert_coordinates_to_position(position_key, setting):
    setting[position_key] = hive.hardware_control.rbs_entities.PositionCoordinates.parse_obj(setting).dict()
    setting.pop("x", None)
    setting.pop("y", None)
    setting.pop("phi", None)
    setting.pop("zeta", None)
    setting.pop("det", None)
    setting.pop("theta", None)


def parse_rbs_recipes(recipes_section):
    recipes = []

    for input_recipe in recipes_section:
        if input_recipe["type"] == "random":
            recipes.append(parse_random_recipe(input_recipe))
        elif input_recipe["type"] == "channeling":
            recipes.append(parse_channeling_recipe(input_recipe))
    return recipes


def parse_random_recipe(recipe_section: Dict) -> Dict:
    setting = drop_nan(recipe_section)
    convert_coordinates_to_position("start_position", setting)
    setting["vary_coordinate"] = rbs.VaryCoordinate(name="phi", start=0, end=30, increment=2).dict()
    return setting


def parse_channeling_recipe(recipe_section: Dict) -> Dict:
    setting = drop_nan(recipe_section)
    convert_coordinates_to_position("start_position", setting)
    setting["random_vary_coordinate"] = rbs.VaryCoordinate(name="phi", start=0, end=30, increment=2).dict()
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
    setting["yield_optimize_detector_index"] = setting["ays_detector_index"]
    setting.pop("ays_detector_index")
    setting["random_vary_coordinate"] = {"name": "phi", "start": 0, "end": 30, "increment": 2}
    setting["yield_integration_window"] = {}
    setting["yield_integration_window"]["start"] = setting["ays_window_start"]
    setting.pop("ays_window_start")
    setting["yield_integration_window"]["end"] = setting["ays_window_end"]
    setting.pop("ays_window_end")
    return setting






