param([string]$VenvPath = ".\.venv")
if (Test-Path "$VenvPath/Scripts/Activate.ps1") { & "$VenvPath/Scripts/Activate.ps1" }
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
