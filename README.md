# Product Video Generator (Veo Edition)

Dieser Generator erstellt automatisch verkaufsfördernde Produktvideos unter Verwendung von Google Trends, Gemini Textmodellen und dem **Gemini Veo 3.1** Videomodell.

Im Gegensatz zum Podcast-Generator wird hier **alles** (Video, Audio, Musik) direkt vom Veo-Modell generiert.

## Onboarding für neue Entwickler

Wenn du neu im Projekt bist, gehe in dieser Reihenfolge vor:

1. **Projektüberblick lesen:** Diese README für Setup, Ablauf und Output.
1. **Beitragsprozess lesen:** [CONTRIBUTING.md](CONTRIBUTING.md) für lokale Checks, PR-Workflow und Projektkonventionen.
1. **Agentenregeln lesen:** [AGENTS.md](AGENTS.md) für Copilot/AI-Guardrails und Arbeitsweise im Repository.

Schnellstart:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
python -m pip install mdformat
./run.sh "Smarte Kaffeemaschine"
```

## Voraussetzungen

- Python 3.10+
- Ein Google GenAI API Key mit Zugriff auf Veo 3.1 (Preview).

## Installation

1. Projekt klonen oder entpacken.
1. Umgebungsvariablen setzen:
   \`\`\`bash
   cp .env.example .env # .env bearbeiten und GEMINI_API_KEY eintragen
   \`\`\`
1. Setup ausführen:
   \`\`\`bash
   chmod +x setup.sh run.sh
   ./setup.sh
   \`\`\`

## Nutzung

Einfach das Run-Skript starten. Optional kann ein Thema übergeben werden.

\`\`\`bash
./run.sh "Smarte Kaffeemaschine" # Mit spezifischem Produkt/Thema

./run.sh # Ohne Thema (sucht automatisch nach Trends)
\`\`\`

## Funktionsweise

1. **Trends:** Prüft Google Trends DE auf Relevanz des Themas.
1. **Skript:** Gemini 2.0 Flash erstellt ein Verkaufs-Skript (Hook, Benefits, CTA).
1. **Video:** Gemini Veo 3.1 generiert das komplette Video inkl. Sprache und Musik basierend auf dem Skript.
1. **Metadaten:** Erstellt Titel und Beschreibung für YouTube/Social Media.

## Output

Die Ergebnisse landen im Ordner \`finished_videos\`:

- \`\*.mp4\`: Das fertige Video.
- \`\*.json\`: Metadaten für den Upload.
- \`\*\_script.txt\`: Das genutzte Skript.

## Hinweise für Agents / Copilot

Siehe [AGENTS.md](AGENTS.md) für Leitplanken, Arbeitsweise und Qualitätssicherung.
Für Contributor-Prozess und lokale Validierung siehe [CONTRIBUTING.md](CONTRIBUTING.md).
