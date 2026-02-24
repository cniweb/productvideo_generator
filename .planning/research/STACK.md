# Stack Research

**Domain:** Produkt-Video-Generator (Python CLI mit Gemini/Veo)
**Researched:** 2026-02-24
**Confidence:** MEDIUM

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python | 3.10+ | Runtime fuer CLI und Pipeline | Passt zu SDK-Anforderungen (google-genai erfordert Python >=3.10); vermeidet Kompatibilitaetsrisiken. Confidence: HIGH |
| google-genai | 1.64.0 | Gemini/Veo SDK (Text, Video, Operations) | Offizielles Google Gen AI SDK fuer Gemini + Veo; aktive Releases, einheitliche API fuer Text/Video. Confidence: HIGH |
| pytrends | 4.9.2 | Google Trends Zugriff (DACH/DE) | De-facto Standard fuer Trends-Scraping in Python; keine offizielle Trends-API. Version ist alt, aber aktuellste Release. Confidence: MEDIUM |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| python-dotenv | 1.2.1 | .env Laden fuer Secrets/Config | Immer, wenn lokale Entwicklung oder CLI-Run mit .env genutzt wird. Confidence: HIGH |
| tenacity | 9.1.4 | Retry/Backoff bei externen APIs | Bei Trends/Gemini/Veo Calls fuer resiliente Fallbacks. Confidence: HIGH |
| pydantic | 2.12.5 | Strukturierte Outputs/Schema Validierung | Wenn JSON-Outputs (Metadata, Script-Teile) strikt validiert werden sollen. Confidence: HIGH |
| typer | 0.24.1 | CLI-UX (Args, Help, Completion) | Wenn CLI ueber argparse hinausgehen soll (Subcommands, Auto-Help). Confidence: HIGH |
| rich | 14.3.3 | CLI-Ausgaben/Status/Logs | Fuer klare Statusanzeigen, Fehlerausgaben, Progress. Confidence: HIGH |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| ruff | Linting/Formatierung | CI nutzt ruff; konsistente Checks lokal. |
| pytest | Tests | Standard fuer Unit-Tests, passend zum Repo. |

## Installation

```bash
# Core
python -m pip install google-genai pytrends

# Supporting
python -m pip install python-dotenv tenacity pydantic typer rich

# Dev dependencies
python -m pip install ruff pytest
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| google-genai | Vertex AI Python SDK | Wenn du ausschliesslich Vertex AI verwendest und keine Gemini Developer API brauchst; sonst google-genai als einheitliche Schicht. |
| typer | argparse | Wenn Minimal-CLI ohne Subcommands/Completion gewuenscht ist oder externe Abhaengigkeiten reduziert werden sollen. |
| tenacity | eigene Retry-Logik | Wenn du volle Kontrolle ueber Backoff/Logging willst und keine Abhaengigkeit moechtest. |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| google-generativeai | SDK ist deprecated und seit 2025-11-30 EOL; keine neuen Features/Support. | google-genai |
| ffmpeg / moviepy / externe TTS | Bricht Constraint: Audio/Video soll von Veo kommen; erhoeht Abhaengigkeiten. | Veo ueber google-genai |
| Web-UI Frameworks im MVP | Scope-Creep, hoehere Wartung, CLI ist Ziel-Workflow. | Typer CLI |

## Stack Patterns by Variant

**Wenn Gemini Developer API genutzt wird:**
- google-genai Client mit `api_key` nutzen
- Weil Developer API einfache API-Key Auth bietet und Veo Preview direkt via SDK erreichbar ist

**Wenn Vertex AI genutzt wird:**
- google-genai Client mit `vertexai=True`, `project`, `location`
- Weil Vertex AI stabilere Enterprise-Auth, IAM und GCS-Integration bietet

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| google-genai 1.64.0 | Python >=3.10 | SDK setzt Python >=3.10 voraus. |
| typer 0.24.1 | Python >=3.10 | Passt zur Repo-Constraint. |
| pytest 9.0.2 | Python >=3.10 | CI-Target kompatibel. |

## Sources

- https://pypi.org/project/google-genai/ — Version 1.64.0, Python >=3.10
- https://googleapis.github.io/python-genai/ — Gemini/Veo SDK Nutzung, Veo Video-Generierung
- https://pypi.org/project/pytrends/ — Version 4.9.2
- https://pypi.org/project/python-dotenv/ — Version 1.2.1
- https://pypi.org/project/tenacity/ — Version 9.1.4
- https://pypi.org/project/pydantic/ — Version 2.12.5
- https://pypi.org/project/typer/ — Version 0.24.1
- https://pypi.org/project/rich/ — Version 14.3.3
- https://pypi.org/project/ruff/ — Version 0.15.2
- https://pypi.org/project/pytest/ — Version 9.0.2
- https://pypi.org/project/google-generativeai/ — Deprecated/EOL Hinweis

---
*Stack research for: Produkt-Video-Generator (Python CLI mit Gemini/Veo)*
*Researched: 2026-02-24*
