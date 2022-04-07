import logging

import pandas as pd
from io import StringIO
from typing import Dict, List
from erd_entities import ErdJobModel


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


def parse_rqm_number(top_section: str) -> Dict:
    df = pd.read_csv(StringIO(top_section))
    job_id = str(df["job_id"][0])
    top_settings = {"job_id": job_id}
    return top_settings


def parse_recipes(list_section: str) -> List[Dict]:
    df = pd.read_csv(StringIO(list_section), dtype=object)
    return drop_nan(df.to_dict('records'))


def parse_rqm(csv_text: str) -> ErdJobModel:
    logging.info("parse_rqm")
    [rqm_section, recipes_section] = get_sections(csv_text)
    erd_rqm_json = parse_rqm_number(rqm_section)
    erd_rqm_json["recipes"] = parse_recipes(recipes_section)
    return ErdJobModel.parse_obj(erd_rqm_json)
