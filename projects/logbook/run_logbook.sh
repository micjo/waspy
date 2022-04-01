#!/bin/bash

source venv/bin/activate
uvicorn --factory logbook:main --log-level warning --host="0.0.0.0" --reload --port=8001
