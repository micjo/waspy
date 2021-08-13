#!/bin/bash
source venv/bin/activate
#uvicorn mca_dash:app --reload --log-level=warning
uvicorn mca_dash:app --host=169.254.150.200 --log-level=warning
