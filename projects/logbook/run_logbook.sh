#!/bin/bash

source venv/bin/activate
uvicorn --factory logbook:main --log-level warning --host="0.0.0.0" --port=8001 --app-dir=logbook
