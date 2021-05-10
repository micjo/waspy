#!/bin/bash

set FLASK_APP=mca_dash.py
set FLASK_ENV=development
python -m flask run --host=0.0.0.0

