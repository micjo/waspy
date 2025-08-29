#!/bin/bash

export DB_FILE="imec.db"
export DASHBOARD_FILE="/tmp/daybook.toml"
export REMOTE_PATH="/mnt/winbe_wasp/daybook/"
source ../../venv/bin/activate
uvicorn --factory src.db.main:main --log-level warning --host="0.0.0.0" --port=8001  --reload
