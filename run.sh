#!/bin/bash
export config_file="./lab_config.toml"
export faker=false
export env_state="prod"

source venv/bin/activate
uvicorn --reload --factory hive:create_app --root-path /hive --log-level warning
