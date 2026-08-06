# Security, Run-Manifest und Output-QA

## Ziel

Die lokale Productvideo-CLI erhält reproduzierbare Dependency-Sicherheitsprüfungen, ein mit `podcast_generator` kompatibles Run-Manifest und einen abschließenden Output-QA-Schritt.

## Umfang

- `pip-audit` läuft in CI und blockiert nur bei HIGH/CRITICAL-Schwachstellen.
- LOW/MODERATE-Schwachstellen werden sichtbar gewarnt, blockieren den Build aber nicht.
- Productvideo erzeugt ein Manifest mit gemeinsamen Feldern für Status, Laufzeit, Modelle, Artefakte und Fehler.
- Productvideo führt nach Metadaten einen eigenen abschließenden QA-Schritt aus.
- Die QA prüft Dateien, Größen, gültiges JSON und referenzierte Artefakte.
- `ffprobe` wird verwendet, wenn es verfügbar ist; ein fehlendes `ffprobe` erzeugt nur eine Warnung.
- Podcast behält seine bestehende QA-, Resume- und Manifest-Semantik und wird strukturell angeglichen.

## Nicht im Umfang

- Keine neuen Cloud- oder Deployment-Jobs.
- Keine echten API-Aufrufe in Tests oder CI.
- Keine gemeinsame Runtime-Bibliothek.
- Keine Änderung der CLI-Argumente oder Output-Namenskonventionen.

## Fehlerverhalten

- QA-Fehler setzen den Laufstatus auf `failed` und führen zu einem Fehler-Exit-Code.
- API-, Konfigurations- und lokale Artefaktfehler bleiben unterscheidbar.
- Secrets und Credentials erscheinen weder im Manifest noch in Audit-Logs.

## Teststrategie

- Productvideo erhält deterministische Tests für Manifest, QA, JSON-Fehler und optionales `ffprobe`.
- Podcast erhält Regressionstests für unveränderte QA-/Manifest-/Resume-Semantik.
- Beide CI-Workflows führen `pip-audit` auf Python 3.12 und 3.13 aus.
