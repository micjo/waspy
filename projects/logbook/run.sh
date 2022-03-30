#!/bin/bash

source venv/bin/activate
uvicorn --factory logbook:create_app --root-path /hive --log-level warning --host="0.0.0.0"
