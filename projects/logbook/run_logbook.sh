#!/bin/bash

export DB_FILE="imec.db"
source ../../venv/bin/activate
uvicorn --factory src.logbook.main:main --root-path /logbook --log-level warning --host="0.0.0.0" --port=8001 
