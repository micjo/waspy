#!/bin/bash
export config_file="./lab_config.toml"
export faker=false
export env_state="prod"
export logbook_url="http://127.0.0.1:8001"

source ../../venv/bin/activate
uvicorn --factory src.mill.main:create_app --root-path /mill --log-level warning --host="0.0.0.0" --port=8000
