#!/bin/bash

source venv/bin/activate
uvicorn --factory src.logbook.main:main --log-level warning --host="0.0.0.0" --port=8001 
