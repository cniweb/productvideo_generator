# Beitragen zu productvideo_generator

Vielen Dank für deinen Beitrag.

## Voraussetzungen

- Python 3.10+
- Ein gültiger `GEMINI_API_KEY` mit Zugriff auf Gemini/Veo-Modelle
- Eine konfigurierte `.env`-Datei im Repository-Root

Erforderliche `.env`-Variablen:

- `GEMINI_API_KEY`
- `CHANNEL_NAME`
- `CHANNEL_DESCRIPTION`
- `VIDEO_OUTPUT_DIR`

Optionale Video-Einstellungen:

- `VIDEO_MODEL`
- `VIDEO_MAX_SECONDS`
- `VIDEO_ASPECT_RATIO`
- `VIDEO_RESOLUTION`

## Lokales Setup

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Oder nutze:

```bash
./setup.sh
```

## Lokal ausführen

```bash
./run.sh "Smarte Kaffeemaschine"
```

Ohne explizites Thema:

```bash
./run.sh
```

## Lint, Kompilieren und Tests

Nutze dieselben Checks wie in CI:

```bash
python -m ruff check productvideo_generator.py
python -m mdformat --check **/*.md
python -m compileall productvideo_generator.py
python -m pytest -q
```

Einen einzelnen Test ausführen:

```bash
python -m pytest -q tests/test_productvideo_generator.py::test_generate_sales_script_writes_file
```

Oder den kombinierten lokalen Ablauf:

```bash
./ci.sh
```

## Repository-spezifische Konventionen

- Nutzerseitiger Text bleibt auf Deutsch (Skripte, Titel, Beschreibungen).
- Skriptstil bleibt sales-/conversion-orientiert (Hook, Solution, Benefits, CTA).
- Visuelle Hinweise in Klammern im generierten Skript verwenden, wenn es für Veo-Prompts hilft.
- Kein ffmpeg oder externes TTS/Mixing hinzufügen: Video, Audio und Musik werden via Veo generiert.
- Trendverhalten bleibt DACH-fokussiert (aktuell `geo='DE'` für Trend-Abfrage).
- Konfiguration bleibt `.env`-getrieben und Secrets werden nie hardcodiert.
- Bevorzuge robuste Fallbacks bei externen API-Problemen, besonders bei Trends und Modell-Verfügbarkeit.

## Pull-Request-Checkliste

Vor dem Öffnen eines PRs:

1. Lint + Tests lokal ausführen.
1. Änderungen minimal und auf das Thema begrenzen.
1. Doku aktualisieren, wenn Verhalten, Kommandos oder Konfiguration angepasst wurden.
1. Eine klare Zusammenfassung geben, was geändert wurde und wie es validiert wurde.
