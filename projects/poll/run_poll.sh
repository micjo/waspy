#!/bin/bash

source ../../venv/bin/activate

export CONFIG_FILE="config.toml"
export LOG_TO="logbook"
export LOGBOOK_URL="http://172.16.3.203:8001"
python src/poll/main.py

