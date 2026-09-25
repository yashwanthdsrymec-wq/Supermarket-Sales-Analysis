@echo off
cd /d "%~dp0"
if not exist venv\Scripts\python.exe (
    echo Creating virtual environment...
    python -m venv venv
)
echo Installing required packages...
venv\Scripts\python.exe -m pip install -r requirements.txt
echo Starting Supermarket Sales Analysis...
venv\Scripts\python.exe -m streamlit run app.py
pause
