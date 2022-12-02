import json
from datetime import datetime
from typing import List, Dict
from waspy.iba.file_handler import FileHandler


def update_account_format(file_handler: FileHandler, account: str, format: List):
    file_handler.cd_folder(account)
    file_handler.write_json_to_disk(f'_{account}_format.json', {"format": format})
    file_handler.cd_folder_up()


def post_account_entry(file_handler: FileHandler, account: str, entry: Dict):
    file_handler.cd_folder(account)
    format = file_handler.read_json_from_disk(f'_{account}_format.json')["format"]
    now = datetime.now()
    time_string = now.strftime("%Y.%m.%d_%H.%M.%S")

    formatted_entry = {"epoch": int(now.timestamp()), "datetime":time_string}

    for key in format:
        formatted_entry[key] = entry.get(key, "")

    root_entries = file_handler.read_json_from_disk(f'{account}_entries.json')
    entries = root_entries.get("entries", [])
    entries.append(formatted_entry)
    file_handler.write_json_to_disk(f'{account}_entry.json', {"entries":[entries]})
    file_handler.cd_folder_up()


def get_account_data():
    try:
        with open("filled.txt", "r") as filled_template:
            data = json.load(filled_template)
    except json.decoder.JSONDecodeError:
        data = {}

    return data







