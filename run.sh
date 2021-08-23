#!/bin/bash
export config_file="./home_config.toml"
source venv/bin/activate
uvicorn --reload --factory hive:create_app