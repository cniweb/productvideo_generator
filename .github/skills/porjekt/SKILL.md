---
name: Project
description: Guide for work with this porject
---

## 1) Python-Pipeline pflegen
- Arbeite primär in `productvideo_generator.py` und halte den 4-Schritt-Flow stabil:
  1. Trends (`research_trends`)
  2. Sales-Skript (`generate_sales_script`)
  3. Veo-Video (`generate_video_with_veo`)
  4. Metadaten (`generate_metadata`)
- Behalte Dateiausgaben unter `VIDEO_OUTPUT_DIR` bei (`*_script.txt`, `*.mp4`, `*_meta.json`).

## 2) Gemini/Veo-Integration
- Nutze `.env`/Umgebungsvariablen, keine hartkodierten Keys.
- Relevante Variablen: `GEMINI_API_KEY`, `CHANNEL_NAME`, `CHANNEL_DESCRIPTION`, `VIDEO_OUTPUT_DIR`.
- Optional: `VIDEO_MODEL`, `VIDEO_MAX_SECONDS`, `VIDEO_ASPECT_RATIO`, `VIDEO_RESOLUTION`.
- Kein ffmpeg, keine externe TTS-/Audio-Mischung: Audio/Video/Musik kommen aus Veo.

## 3) Prompt- und Content-Qualität
- User-facing Inhalte standardmäßig auf Deutsch.
- Skriptstil: Sales/Conversion (Hook, Problem/Solution, Benefits, CTA).
- Erlaube kurze visuelle Hinweise in Klammern im Skript für bessere Veo-Steuerung.
- Fokus auf Produkt-/Sales-Videos (kein Podcast-Flow).

## 4) Trends & Resilienz
- Trend-Fokus DACH (aktuell `geo='DE'` im Code).
- Bei Trend-Fehlern/Fremd-API-Problemen Fallback-Verhalten beibehalten (nicht gesamte Pipeline abbrechen).
- Veo-Modell-Fallback-Logik nur ergänzen, wenn sie robust bleibt.

## 5) Qualitätssicherung (lokal + CI)
- Lint: `python -m ruff check productvideo_generator.py`
- Compile: `python -m compileall productvideo_generator.py`
- Tests: `python -m pytest -q`
- Einzeltest: `python -m pytest -q tests/test_productvideo_generator.py::test_generate_sales_script_writes_file`
- Optional Komplettlauf: `./ci.sh`
