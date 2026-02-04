#!/bin/bash
# Setup-Skript für productvideo_generator

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}--- Product Video Generator Setup ---${NC}"

# .env Check
if [ ! -f ".env" ]; then
    echo -e "${RED}Fehler: .env fehlt.${NC}"
    echo "Bitte 'cp .env.example .env' ausführen und konfigurieren."
    exit 1
fi

# Python Check
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Fehler: Python 3 fehlt.${NC}"
    exit 1
fi

# Venv erstellen falls nötig
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/Scripts/activate

# Dependencies
echo -e "${GREEN}Installiere Python Abhängigkeiten...${NC}"
pip install -r requirements.txt

echo -e "\n${GREEN}--- Installation abgeschlossen! ---${NC}"
echo "Starte mit: ./run.sh \"Dein Produkt\""
