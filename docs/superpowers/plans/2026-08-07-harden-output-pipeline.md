# Output-Pipeline härten Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Externe Hänger, Fallbackfehler und unvollständige Medienartefakte deterministisch behandeln.

**Architecture:** Productvideo erhält Timeout-/Polling- und Fallback-Verbesserungen im bestehenden Modul. Gemeinsame Manifest-/QA-Helfer bleiben zunächst projektintern, damit die Repositories unabhängig bleiben.

**Tech Stack:** Python, pytest, ffprobe, atomic filesystem replacement, bestehende Gemini-/Veo-API.

## Global Constraints

- Keine unbegrenzten API-Wartezeiten.
- Keine Live-API-Aufrufe in Tests.
- CLI- und Output-Namenskonventionen bleiben kompatibel.
- Fehlgeschlagene Läufe erhalten Status `failed`.

### Task 1: Veo-Polling und Fallbacks

**Files:**
- Modify: `productvideo_generator.py`
- Test: `tests/test_productvideo_generator.py`

- [ ] Polling-Timeout und maximale Polling-Versuche als Konstanten definieren.
- [ ] Timeoutfehler als `GenerationError` melden.
- [ ] Fallbackfehler nach ausgeschöpften Modellen weiterreichen.
- [ ] Tests für Polling-Erfolg, Polling-Timeout und Fallback-Komplettfehler ergänzen.

### Task 2: Manifest-/Output-QA

**Files:**
- Modify: `productvideo_generator.py`
- Modify: `tests/test_productvideo_generator.py`

- [ ] Manifest-Pflichtfelder validieren.
- [ ] QA-Ergebnis intern strukturiert mit Fehlern/Warnungen bilden.
- [ ] `ffprobe`-Warnungen von echten QA-Fehlern unterscheiden.
- [ ] Tests für Schemafehler und Warnpfade ergänzen.

### Task 3: Atomare Writes

**Files:**
- Modify: `productvideo_generator.py`
- Test: `tests/test_productvideo_generator.py`

- [ ] JSON- und Textartefakte zuerst in temporäre Dateien schreiben.
- [ ] Mit `os.replace` atomar ins Ziel verschieben.
- [ ] Temporäre Dateien bei Fehlern entfernen.
- [ ] Test für Schreibfehler und kein halbfertiges Zielartefakt ergänzen.

### Task 4: Dependency-Warnung

- [ ] Dependabot-Warnung und `pip-audit`-Status prüfen.
- [ ] Nur eine sichere, kompatible Dependency-Aktualisierung durchführen.
- [ ] Tests und Audit erneut ausführen.

### Task 5: Verifikation und PR

- [ ] Tests, Ruff, Compile, Markdown und Shell-Syntax ausführen.
- [ ] PR öffnen und beide CI-Matrixläufe prüfen.
- [ ] PR nach grüner CI mergen und Branches löschen.
