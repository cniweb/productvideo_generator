# CI- und Integrationsharmonisierung

## Ziel

Der lokale CLI-Charakter des Product-Video-Generators bleibt unverändert. Dieses Vorhaben harmonisiert nur Entwicklungsqualität und externe Integrationsgrenzen mit `podcast_generator`.

## Umfang

- GitHub Actions verwenden einheitliche Sicherheits-, Cache- und Concurrency-Regeln.
- CI prüft Abhängigkeiten, Ruff, Python-Kompilierung, Tests und Markdown.
- Testresultate und Coverage werden reproduzierbar erzeugt und als Artefakte veröffentlicht.
- Lokale Skripte verwenden konsistente Python-/venv-Aufrufe und bleiben ohne Cloud-Deployment nutzbar.
- Dependency-Updates werden über Renovate in beiden Repositories gleich behandelt.

## Nicht im Umfang

- Kein Deployment und keine Veröffentlichung generierter Medien.
- Keine echten Gemini-, Trends-, Freesound- oder Google-Cloud-Aufrufe in CI.
- Keine Zusammenlegung der fachlichen Generator-Pipelines.
- Keine Änderungen an API-Secrets oder generierten lokalen Dateien.

## Umsetzung

1. Baseline pro Repository erfassen: Status, Tests, Ruff, Compile-Check und Markdown-Linting.
2. Productvideo-CI an die gemeinsame Qualitätsbasis anpassen.
3. Productvideo-Lokalwerkzeuge an plattformtaugliche `python -m`-Aufrufe anpassen.
4. Renovate für Productvideo ergänzen und Dependency-Konfiguration vergleichen.
5. Podcast-CI und Lokalwerkzeuge auf dieselben Sicherheits- und Ausführungsstandards bringen.
6. Jeden Schritt mit den betroffenen Tests und Lintern prüfen.
7. Pro Repository Commits erstellen, Branches pushen und Pull Requests öffnen.
8. GitHub-Actions-Ergebnisse prüfen und Fehler gezielt beheben.
9. Nur grüne Pull Requests mergen.

## Qualitätskriterien

- Keine Änderung der CLI-Eingaben oder Output-Namenskonventionen.
- Unit-Tests bleiben netzwerkfrei und deterministisch.
- CI nutzt Least-Privilege-Berechtigungen.
- CI-Läufe desselben Branches werden durch Concurrency begrenzt.
- Action-Versionen werden nicht unkontrolliert über `latest` bezogen.
- Lokale Checks und GitHub Actions führen dieselben wesentlichen Prüfungen aus.
