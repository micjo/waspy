#!/bin/bash

export DB_FILE="imec.db"
source ../../venv/bin/activate
uvicorn --factory src.db.main:main --log-level warning --host="0.0.0.0" --port=8001  --reload
