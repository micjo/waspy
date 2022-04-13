#!/bin/bash
export config_file="./home_config.toml"
export faker=true
export env_state="dev"
export trend_store="/tmp/trends/"
export logbook_url="http://127.0.0.1:8001"

source venv/bin/activate
#uvicorn --reload --factory hive:create_app --log-level warning --host="localhost" --port=8000
uvicorn --factory service_mill:create_app --app-dir service_mill --log-level warning --host="localhost" --port=8000 --reload
