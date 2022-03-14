#!/bin/bash
export config_file="./lab_config.toml"
export faker=false
export env_state="prod"
export trend_store="/root/trends/"

source venv/bin/activate
uvicorn --factory hive:create_app --root-path /hive --log-level warning --host="0.0.0.0"
