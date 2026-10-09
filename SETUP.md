# ESS Python Starter — Local Setup

Requires **Python 3.12 or newer** (`python --version`).

## Create a virtual environment
python -m venv .venv

## Activate
- Windows PowerShell: `.\.venv\Scripts\Activate.ps1`
- macOS / Linux: `source .venv/bin/activate`

## Install development dependencies
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

## Enable pre-commit hooks (ruff, gitleaks, mypy)
pre-commit install

## Verify (the same checks CI runs)
ruff check .
ruff format --check .
mypy src
pytest
pip-audit --skip-editable
python tools/ess_guard.py check

## Start the API
cp .env.example .env
uvicorn ess_app.main:app --reload
