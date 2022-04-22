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


def drop_nan(data: Dict) -> List[Dict]:
    dropped = []
    for setting in data:
        clean_dict = {k: v for k, v in setting.items() if pd.notnull(v)}
        dropped.append(clean_dict)
    return dropped


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


def parse_recipes(recipe_section: str) -> [Dict]:
    '''Defaults can happen here'''
    recipe_settings = parse_list_settings(recipe_section)

    for setting in recipe_settings:
        if "type" not in setting:
            raise AttributeError("type object 'recipe', has no attribute 'type'")
        elif setting["type"] == rbs.RecipeType.random:
            convert_coordinates_to_position("start_position", setting)
            setting["vary_coordinate"] = rbs.VaryCoordinate(name="phi", start=0, end=30, increment=2).dict()
        else:
            raise AttributeError("type object 'type' is incorrect")

    return recipe_settings
