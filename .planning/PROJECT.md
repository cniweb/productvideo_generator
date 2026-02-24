# Produkt Video Generator

## What This Is

Ein CLI-Tool in Python, das aus einem Produkt-Input automatisch ein verkaufsstarkes Video erstellt.
Es erzeugt in einem Durchlauf Skript, Video und Metadaten, damit manuelle Arbeit entfällt.

## Core Value

Ein einziger CLI-Aufruf erzeugt schnell ein vollständiges Produkt-Video (Skript, Video, Metadaten).

## Requirements

### Validated

- ✓ Produkt-Input wird als Thema verarbeitet — existing
- ✓ Sales-Script wird automatisch erstellt — existing
- ✓ Video wird automatisch generiert und gespeichert — existing
- ✓ Metadaten werden erzeugt und gespeichert — existing

### Active

- [ ] Ein einziger CLI-Lauf erzeugt Skript, Video und Metadaten ohne manuelle Zwischenschritte
- [ ] Skript folgt konsistentem Sales-Framework (Hook, Solution, Benefits, CTA)
- [ ] Trend-Recherche liefert DACH-relevante Themen (DE) mit robusten Fallbacks

### Out of Scope

- Web-UI — CLI-Workflow ist ausreichend
- Batch-Verarbeitung vieler Produkte — Fokus auf Single-Produkt-Run

## Context

- Bestehender Python-Workflow in `productvideo_generator.py` mit linearem Pipeline-Flow
- Ausgabe-Dateien werden in `VIDEO_OUTPUT_DIR` geschrieben
- Ziel ist schnelle, konsistente Erstellung von Produktvideos

## Constraints

- **Tech stack**: Python 3.10+ — bestehender Code und CI basieren darauf
- **Audio/Video**: Keine externen TTS/Mixing-Tools — Veo übernimmt Audio/Musik/Video
- **Config**: Secrets aus `.env` — nichts hardcoden

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| CLI-first statt Web-UI | Schnellster, einfachster Workflow für Einzelperson | — Pending |
| DACH-Fokus bei Trends | Relevanz für Zielmarkt erhöhen | — Pending |

---
*Last updated: 2026-02-24 after initialization*
