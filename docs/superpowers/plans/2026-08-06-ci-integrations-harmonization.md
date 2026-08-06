# CI- und Integrationsharmonisierung Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Die lokale CLI-Anwendung erhält dieselbe reproduzierbare CI- und Entwicklungsqualität wie `podcast_generator`, ohne ihre fachliche Pipeline zu verändern.

**Architecture:** Die Änderungen bleiben auf Workflow-, Dependency- und Shell-Skript-Ebene. Echte externe APIs werden nicht in CI aufgerufen; Tests verwenden vorhandene Dummies. CI und `ci.sh` führen dieselben wesentlichen Prüfungen aus.

**Tech Stack:** GitHub Actions, Python 3.12/3.13, pytest, pytest-cov, Ruff, mdformat, Renovate, Bash.

## Global Constraints

- Kein Deployment und keine Veröffentlichung generierter Medien.
- Keine echten Gemini-, Trends-, Freesound- oder Google-Cloud-Aufrufe in CI.
- Keine Änderung der CLI-Eingaben oder Output-Namenskonventionen.
- Secrets, `.env` und generierte Dateien bleiben untracked.
- Actions werden auf feste Versionen gepinnt; `latest` wird nicht verwendet.

### Task 1: Baseline prüfen

**Files:** Keine Änderungen.

- [ ] `git status --short --branch` ausführen.
- [ ] `python3 -m pytest -q` oder verfügbare venv-Alternative ausführen.
- [ ] Ruff, Compile-Check und Markdown-Check ausführen.
- [ ] Fehlende lokale Tools dokumentieren, ohne Codeänderungen vorzutäuschen.

### Task 2: CI-Workflow harmonisieren

**Files:**
- Modify: `.github/workflows/ci.yml`
- Modify: `requirements.txt`

- [ ] `permissions: contents: read` und Concurrency pro Workflow/Ref ergänzen.
- [ ] Python-Matrix `3.12`, `3.13` verwenden.
- [ ] `pytest-cov` und `pymarkdownlnt` verfügbar machen.
- [ ] Markdown-Linting ergänzen.
- [ ] Tests mit JUnit- und Coverage-XML ausführen und Reports als Artefakte hochladen.
- [ ] Import-Sanity-Check auf tatsächlich verwendete Productvideo-Abhängigkeiten begrenzen.
- [ ] YAML-Struktur mit `actionlint` oder einem vergleichbaren Syntaxcheck prüfen.

### Task 3: Lokale Skripte korrigieren

**Files:**
- Modify: `ci.sh`
- Modify: `setup.sh`
- Modify: `run.sh`

- [ ] Eine Unix-kompatible Python-Auswahl über `${PYTHON_BIN:-python3}` verwenden.
- [ ] Venv mit `.venv/bin/python` und `.venv/bin/pip` nutzen.
- [ ] Direkte Aufrufe durch `python -m pip`, `python -m pytest`, `python -m ruff` und `python -m mdformat` ersetzen.
- [ ] Keine fachliche Änderung am CLI-Aufruf oder an der Topic-Auflösung vornehmen.
- [ ] Shell-Syntax mit `bash -n` prüfen.

### Task 4: Renovate ergänzen

**Files:**
- Create: `renovate.json`
- Create: `.github/workflows/renovate.yml`

- [ ] Dieselbe wöchentliche Renovate-Struktur wie im Podcast-Projekt verwenden.
- [ ] Renovate-Action auf feste Version pinnen.
- [ ] `RENOVATE_TOKEN` ausschließlich als Secret verwenden.
- [ ] Workflow- und JSON-Syntax prüfen.

### Task 5: Gesamtprüfung und Commit

- [ ] `python -m ruff check productvideo_generator.py tests/` erfolgreich ausführen.
- [ ] `python -m compileall productvideo_generator.py` erfolgreich ausführen.
- [ ] `python -m pytest -q --junitxml=test-results.xml --cov=productvideo_generator --cov-report=term-missing` erfolgreich ausführen.
- [ ] Markdown-Linting und `git diff --check` erfolgreich ausführen.
- [ ] Einen fokussierten Commit erstellen.
- [ ] Branch pushen, PR öffnen und CI abwarten.
