#!/bin/bash

source ../../venv/bin/activate
uvicorn --factory src.ruthelde.main:main --log-level warning --host="0.0.0.0" --port=8002
