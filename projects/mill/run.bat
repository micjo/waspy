call venv/Scripts/activate.bat
python -m uvicorn mca_dash:app --reload --host=0.0.0.0 --port=5000 --no-use-colors