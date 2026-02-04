#!/bin/bash
# Startskript für den Product Video Generator

# Farben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

TOPIC="$1"
SCRIPT_FILE="productvideo_generator.py"
ENV_FILE=".env"
PYTHON_BIN="python3"

# 1. ENV CHECK
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${RED}Fehler: $ENV_FILE fehlt.${NC}"
    echo "Bitte kopiere .env.example zu .env und trage deinen Key ein."
    exit 1
fi

# 2. VIRTUAL ENVIRONMENT
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Erstelle virtuelles Environment (.venv)...${NC}"
    $PYTHON_BIN -m venv .venv
fi

# Aktivieren
source .venv/Scripts/activate

# 3. ABHÄNGIGKEITEN (Quick Check)
# Wir führen setup.sh aus, wenn es noch nie gelaufen ist (oder manuell aufrufen)
if ! pip freeze | grep -q "google-genai"; then
    echo -e "${YELLOW}Installiere Abhängigkeiten...${NC}"
    pip install -q -r requirements.txt
fi

# 4. STARTEN
echo -e "\n${GREEN}🚀 Starte Video Generator...${NC}"

if [ -z "$TOPIC" ]; then
    # Interaktiver Modus, wenn kein Argument übergeben wurde
    python "$SCRIPT_FILE"
else
    # Argument direkt übergeben (via Pipe damit input() es frisst)
    echo "$TOPIC" | python "$SCRIPT_FILE"
fi

deactivate
