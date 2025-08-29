#!/bin/bash
export config_file="/mnt/winbe_wasp/mill_config/lab_config.toml"
export faker=false
export env_state="prod"
export logbook_url="http://172.16.3.203:8001"

source ../../venv/bin/activate
uvicorn --factory src.mill.main:create_app --log-level warning --host="0.0.0.0" --port=8000
