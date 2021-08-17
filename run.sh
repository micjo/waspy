#!/bin/bash
source venv/bin/activate
#uvicorn mca_dash:app --reload --log-level=warning
uvicorn mca_dash:app --host=127.0.0.1 --log-level=warning
