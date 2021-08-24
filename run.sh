#!/bin/bash
export config_file="./home_config.toml"
export faker=true
export env_state="dev"
export ip="localhost"

source venv/bin/activate
uvicorn --reload --factory hive:create_app