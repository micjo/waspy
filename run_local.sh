#!/bin/bash
export config_file="./home_config.toml"
export faker=false
export env_state="dev"
export trend_store="/tmp/trends/"

source venv/bin/activate
uvicorn --reload --factory hive:create_app --log-level warning --host="localhost" --port=8000
#uvicorn --factory hive:create_app --log-level warning --host="localhost" --port=8000
