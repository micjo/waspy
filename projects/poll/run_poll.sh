#!/bin/bash

source ../../venv/bin/activate

export CONFIG_FILE="config_fake.toml"
export LOG_TO="logbook"

python src/trend/main.py

