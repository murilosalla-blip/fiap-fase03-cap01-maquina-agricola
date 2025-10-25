param(
  [string]$VenvPath = ".\.venv"
)

# Ativa venv se existir
if (Test-Path "$VenvPath/Scripts/Activate.ps1") {
  & "$VenvPath/Scripts/Activate.ps1"
}

# Instala/atualiza dependências (idempotente)
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Executa a EDA
python src/ml/eda.py
