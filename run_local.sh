#!/bin/bash
export config_file="./home_config.toml"
export faker=false
export env_state="dev"

source venv/bin/activate
uvicorn --reload --factory hive:create_app --log-level warning
