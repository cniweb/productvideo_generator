#!/bin/bash
# Führt Linting, Syntax-Check und Tests für productvideo_generator im venv aus.
set -euo pipefail

python_bin="python3"
ruff_version="0.6.8"

if ! $python_bin -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'; then
    echo "Python 3.10 oder neuer erforderlich."
    exit 1
fi

# Virtuelle Umgebung sicherstellen
if [[ ! -d .venv ]]; then
    $python_bin -m venv .venv
fi
source .venv/bin/activate
python_bin=".venv/bin/python"

# Optional: Setup erneut nutzen, falls Umgebungs- und FFmpeg-Checks gewünscht sind (benötigt .env)
if [[ "${1:-}" == "--setup" ]]; then
    ./setup.sh
fi

$python_bin -m pip install --upgrade pip
$python_bin -m pip install -r requirements-dev.txt
$python_bin -m pip install ruff=="$ruff_version"

# Linting
$python_bin -m ruff check --fix productvideo_generator.py tests/
$python_bin -m ruff check productvideo_generator.py tests/

# Markdown-Linting
shopt -s globstar
$python_bin -m pymarkdown -c .pymarkdown.toml scan .

# Import-Prüfung
$python_bin - <<'PY'
import importlib
deps = [
    'google.genai',
    'pytrends',
    'dotenv',
    'pytest',
    'pytest_cov',
]
for dep in deps:
    try:
        importlib.import_module(dep)
    except Exception as exc:
        raise SystemExit(f"Import failed for {dep}: {exc}")
PY

# Syntax-Prüfung
$python_bin -m compileall productvideo_generator.py

# Tests
$python_bin -m pytest -q --cov=productvideo_generator --cov-report=term-missing --cov-fail-under=40 --junitxml=test-results.xml

echo "All checks passed."
