#!/bin/bash

source venv/bin/activate

export CONFIG_FILE="config.toml"
export LOG_TO="logbook"

python trend/run_trend.py

