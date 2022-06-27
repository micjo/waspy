#!/bin/bash
export config_file="./vdg_lab_config.toml"
export faker=false
export env_state="prod"
export logbook_url="http://127.0.0.1:8001"

source venv/bin/activate
uvicorn --factory hive:create_app --root-path /hive --log-level warning --host="0.0.0.0" --port=8000 --app-dir hive
