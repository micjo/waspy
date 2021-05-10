#!/bin/bash

export FLASK_APP=mca_dash.py
export FLASK_ENV=development
python -m flask run --host=0.0.0.0

