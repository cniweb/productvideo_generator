# Config-, QA- und Fehlerverträge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Config-Injektion, maschinenlesbare Fehler und Retry-Metriken in den zentralen Generatorpfaden wirksam machen.

**Architecture:** Die bestehenden globalen Variablen bleiben als Kompatibilitätsschicht. Generator-Methoden bevorzugen injizierte Configwerte; Manifestfehler werden beim Main-Wrapper klassifiziert. Retry-Zähler werden lokal an den vorhandenen Schleifen erhöht.

**Tech Stack:** Python, dataclasses, JSON, pytest.

## Global Constraints

- Bestehende CLI- und Output-Semantik bleibt kompatibel.
- Keine Secrets oder Promptinhalte im Manifest.
- Keine Live-API-Aufrufe in Tests.

### Task 1: Productvideo Config-Nutzung

**Files:**
- Modify: `productvideo_generator.py`
- Test: `tests/test_productvideo_generator.py`

- [ ] Kanal-/Promptwerte aus `self.config` lesen.
- [ ] Output-/Modellwerte aus `self.config` lesen.
- [ ] Test mit abweichender injizierter Config ergänzen.

### Task 2: Podcast Config-Nutzung

**Files:**
- Modify: `podcast_generator.py`
- Test: `tests/test_env_and_cli.py`, Pipeline-Tests

- [ ] Podcastname, Pfade und Modellwerte in zentralen Methoden aus `self.config` lesen.
- [ ] Resume-/Manifestpfade kompatibel halten.
- [ ] Test mit isolierter Config ergänzen.

### Task 3: Strukturierte Manifestfehler

**Files:**
- Modify: beide Hauptmodule
- Test: Manifesttests

- [ ] Fehler als `type`, `message`, `retryable` speichern.
- [ ] QA-, Config- und GenerationError korrekt klassifizieren.
- [ ] Secret-freie Serialisierung testen.

### Task 4: Retry-Zähler

- [ ] Productvideo-Content-Retries und Fallbacks zählen.
- [ ] Podcast-HTTP-, Gemini- und TTS-Retries zählen.
- [ ] Manifesttests für Zähler ergänzen.

### Task 5: Verifikation und PR

- [ ] Tests, Ruff, Compile, Markdown, Shell und CI ausführen.
- [ ] PRs nach grünen Matrixläufen mergen.
- [ ] Branches lokal/remote bereinigen.
