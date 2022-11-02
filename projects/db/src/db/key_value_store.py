import json
from typing import List, Dict


def set_active_template(template: List):
    with open("template_tmp.txt", "w") as file:
        for value in template:
            file.write(f'{value}\n')

    with open("filled.txt", "w") as filled_template:
        filled_template.write("")


def fill_in_template(template: Dict):
    filled = {}
    with open("template_tmp.txt", "r") as template_file:
        for key in template_file.readlines():
            key = key.strip()
            filled[key] = template.get(key, "")

    with open("filled.txt", "w") as filled_template:
        json.dump(filled, filled_template, indent=4)


def get_filled_data():
    try:
        with open("filled.txt", "r") as filled_template:
            data = json.load(filled_template)
    except json.decoder.JSONDecodeError:
        data = {}

    return data







