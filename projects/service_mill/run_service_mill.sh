#!/bin/bash
export config_file="./lab_config.toml"
export faker=false
export env_state="prod"
export logbook_url="http://127.0.0.1:8001"

source venv/bin/activate
uvicorn --factory service_mill:create_app --root-path /service_mill --log-level warning --host="0.0.0.0" --port=8000 --app-dir service_mill
