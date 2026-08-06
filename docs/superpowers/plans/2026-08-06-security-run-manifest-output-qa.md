# Security, Run-Manifest und Output-QA Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans (recommended) to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Productvideo erhält Dependency-Auditing, ein gemeinsames Run-Manifest und eine abschließende Artefaktprüfung.

**Architecture:** Die Änderungen bleiben im bestehenden Hauptmodul und dessen Tests. Das Manifest wird am Ende des Laufs geschrieben; QA prüft danach die vollständige Ausgabe und aktualisiert den finalen Status.

**Tech Stack:** Python, pytest, pytest-cov, pip-audit, ffprobe, GitHub Actions.

## Global Constraints

- `pip-audit` blockiert nur HIGH/CRITICAL.
- LOW/MODERATE erzeugen Warnungen, blockieren aber nicht.
- Keine echten API-Aufrufe in Tests oder CI.
- CLI-Eingaben und Output-Namenskonventionen bleiben unverändert.
- `ffprobe` ist optional; bei Abwesenheit bleibt die Basis-QA aktiv.

### Task 1: Security-Audit in CI

**Files:**
- Modify: `.github/workflows/ci.yml`
- Modify: `requirements.txt`

- [ ] `pip-audit` als CI-Abhängigkeit ergänzen.
- [ ] Audit auf installierter Umgebung für Python 3.12/3.13 ausführen.
- [ ] Ausgabe nach HIGH/CRITICAL filtern und nur diese per Exit-Code blockieren.
- [ ] LOW/MODERATE als GitHub-Warnung ausgeben.
- [ ] Keine Secrets an `pip-audit` übergeben.
- [ ] Workflow-Syntax prüfen.

### Task 2: Manifest- und QA-Tests

**Files:**
- Modify: `tests/test_productvideo_generator.py`

- [ ] Test für vollständiges Manifest mit Status, Zeit, Modellen und Artefakten ergänzen.
- [ ] Test für fehlende/leere MP4- und Skriptdateien ergänzen.
- [ ] Test für ungültiges Metadaten-JSON ergänzen.
- [ ] Test für vorhandenes `ffprobe` mit gültigem Stream ergänzen.
- [ ] Test für fehlendes `ffprobe` als Warnpfad ergänzen.
- [ ] Tests zunächst isoliert fehlschlagen lassen.

### Task 3: Productvideo-Manifest und Output-QA implementieren

**Files:**
- Modify: `productvideo_generator.py`

- [ ] `write_run_manifest(...)` mit stabilen Feldern `topic`, `status`, `started_at`, `finished_at`, `duration_seconds`, `models`, `artifacts`, `error` implementieren.
- [ ] `validate_outputs()` als eigene Methode implementieren.
- [ ] Datei-/Größen-/JSON-Prüfungen durchführen.
- [ ] `shutil.which("ffprobe")` verwenden; bei Verfügbarkeit einen Videostream via `subprocess.run` prüfen.
- [ ] Fehlendes `ffprobe` nur warnen.
- [ ] Pipeline um den abschließenden QA-Schritt erweitern.
- [ ] Fehlerstatus im Manifest schreiben und mit Fehler-Exit-Code beenden.

### Task 4: Verifikation und PR

- [ ] Productvideo-Tests, Ruff, Compile-Check und Markdown-Linting ausführen.
- [ ] `pip-audit` lokal auf der unterstützten Python-Version ausführen.
- [ ] Branch pushen und PR erstellen.
- [ ] Beide CI-Matrixläufe und Audit-Ergebnis prüfen.
- [ ] PR nach grüner CI mergen.
