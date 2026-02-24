# Architecture Research

**Domain:** Produkt-Video-Generator (Python CLI mit LLM + Video-Modell)
**Researched:** 2026-02-24
**Confidence:** MEDIUM

## Standard Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                           CLI / Orchestrator                          │
├──────────────────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌──────────────┐  ┌─────────────┐  ┌───────────┐ │
│  │ Input Handler │  │ Config/Env   │  │ Logger      │  │ Validators│ │
│  └──────┬────────┘  └──────┬───────┘  └─────┬───────┘  └─────┬─────┘ │
│         │                 │                │                  │     │
├─────────┴─────────────────┴────────────────┴──────────────────┴─────┤
│                          Pipeline Services                           │
├──────────────────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌───────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │ Trend Research│→ │ Script Gen     │→ │ Video Gen    │→ │ Metadata │ │
│  └──────┬────────┘  └──────┬────────┘  └──────┬───────┘  └────┬─────┘ │
│         │                 │                 │               │        │
├─────────┴─────────────────┴─────────────────┴───────────────┴────────┤
│                             Persistence                               │
├──────────────────────────────────────────────────────────────────────┤
│  ┌────────────────┐  ┌─────────────────┐  ┌────────────────────────┐  │
│  │ Output Writer  │  │ Cache/Temp (opt)|  │ File System / Output Dir│  │
│  └────────────────┘  └─────────────────┘  └────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| CLI / Orchestrator | Steuerung des End-to-End-Laufs, Fehlerbehandlung, Reihenfolge | Python CLI (argparse/typer), zentrale Pipeline-Funktion |
| Input Handler | Produkt-Input lesen, normalisieren, validieren | Topic Normalizer + Validator |
| Config/Env | Secrets und Settings laden, Defaults, Feature Flags | dotenv + env mapping |
| Logger | Konsistente Logs, Warnungen bei Fallbacks | stdlib logging |
| Trend Research | DACH-Trends holen, Fallbacks bei Ausfällen | pytrends Adapter |
| Script Generator | Sales-Skript generieren (Hook, Solution, Benefits, CTA) | LLM Adapter (Gemini) |
| Video Generator | Video aus Skript/Prompt erzeugen | Veo Adapter |
| Metadata Generator | Titel, Beschreibung, Tags aus Skript/Topic | Template + LLM optional |
| Output Writer | Dateien schreiben, Namenskonventionen | File IO + normalized topic |
| Cache/Temp (opt.) | Zwischenergebnisse, Retry-Backoff | File cache oder in-memory |

## Recommended Project Structure

```
productvideo_generator.py      # CLI entry + pipeline orchestration
src/
├── config/                    # Env loading + settings
├── pipeline/                  # Orchestrator + step runners
├── services/                  # Trend, Script, Video, Metadata
├── prompts/                   # Prompt templates and formatters
├── io/                         # Output writers + path helpers
├── utils/                      # Normalization, logging helpers
└── adapters/                  # External API clients (Gemini, Veo, Trends)
tests/                         # Unit tests + stub adapters
```

### Structure Rationale

- **pipeline/:** Trennschicht fuer Ablaufsteuerung vs. Business-Logik der Schritte.
- **services/:** Jede Pipeline-Stufe als klarer Service mit stabiler Schnittstelle.
- **adapters/:** Externe APIs kapseln, damit Tests stubben und Fehler abfangen koennen.
- **prompts/:** Prompts versionieren und getrennt von Logik halten.

## Architectural Patterns

### Pattern 1: Orchestrated Pipeline

**What:** Sequenzielle Schritte mit klaren Inputs/Outputs pro Stufe.
**When to use:** Lineare CLI-Workflows mit klarer Abhaengigkeit der Schritte.
**Trade-offs:** Einfach und testbar, aber weniger parallelisierbar.

**Example:**
```python
topic = normalize_input(raw_input)
trends = trends_service.fetch(topic)
script = script_service.generate(topic, trends)
video_path = video_service.generate(script)
metadata = metadata_service.generate(topic, script)
writer.persist(script, video_path, metadata)
```

### Pattern 2: Adapter + Port

**What:** Externe Services hinter Interfaces kapseln.
**When to use:** Wenn APIs instabil sind oder Tests ohne Netz laufen sollen.
**Trade-offs:** Mehr Boilerplate, dafuer robuste Tests und Fallbacks.

**Example:**
```python
class GeminiClient:
    def generate_text(self, prompt: str) -> str:
        ...
```

### Pattern 3: Idempotente Ausgaben

**What:** Dateinamen deterministisch aus Topic ableiten.
**When to use:** CLI-Runs duerfen wiederholbar sein.
**Trade-offs:** Risiko von Ueberschreiben, daher klare Namenskonvention.

## Data Flow

### Request Flow

```
User CLI Input
    ↓
Input Handler → Config Loader → Orchestrator
    ↓
Trend Research → Script Generator → Video Generator → Metadata Generator
    ↓
Output Writer → Filesystem
```

### Key Data Flows

1. **Trend→Script:** Trends beeinflussen Hook/Benefits, optionaler Fallback auf Topic-only.
2. **Script→Video:** Skript liefert Story/Prompt fuer Veo; Video-Pfad wird persistiert.
3. **Topic+Script→Metadata:** Titel/Beschreibung/Tags generiert und als JSON gespeichert.

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 0-1k runs | Monolith CLI reicht, lokales File-Output |
| 1k-10k runs | Caching + Retry-Backoff, strukturierte Logs |
| 10k+ runs | Queue/Batch, getrennte Worker fuer Video-Generierung |

### Scaling Priorities

1. **First bottleneck:** Externe API-Limits → Backoff, Caching, Queueing.
2. **Second bottleneck:** IO/Output-Verwaltung → klare Struktur + Storage Abstraktion.

## Anti-Patterns

### Anti-Pattern 1: API-Calls ohne Fallbacks

**What people do:** Fehler nicht abfangen, Run bricht ab.
**Why it's wrong:** Nutzer bekommt kein Output, Pipeline ist fragil.
**Do this instead:** Definierte Fallbacks und Warnlogs, Best-Effort Output.

### Anti-Pattern 2: Prompts in die Pipeline mischen

**What people do:** Prompt-Strings in Orchestrator/IO verteilen.
**Why it's wrong:** Prompt-Änderungen werden riskant und schwer testbar.
**Do this instead:** Prompts zentral in prompts/ kapseln.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| Google Trends (pytrends) | Adapter + Retry | DACH-Geo, Fallback bei Ausfall |
| Gemini | Adapter + Prompt Formatter | Sales-Framework erzwingen |
| Veo | Adapter + Asset Output | Video/Music via API, kein ffmpeg |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| Orchestrator ↔ Services | Method calls with DTOs | Schrittweise Inputs/Outputs |
| Services ↔ Adapters | Interface calls | Einfach mockbar |
| Pipeline ↔ IO | Write-only | Keine Business-Logik in IO |

## Build Order Implications

1. **Config + CLI input parsing** → Grundlage fuer alle nachfolgenden Schritte.
2. **Topic Normalization + Validation** → notwendig fuer stabile Dateinamen/Prompts.
3. **Trend Research Service** → optionaler Input fuer Script; Fallback definieren.
4. **Script Generator** → zentrale Abhaengigkeit fuer Video + Metadata.
5. **Video Generator** → braucht Skript/Prompt + Output-Pfade.
6. **Metadata Generator** → braucht Topic + Script.
7. **Output Writer** → persistiert alle Artefakte; darf keine Logik enthalten.
8. **Retries/Logging** → quer ueber alle Services.

## Sources

- Internal codebase context (PRODUCT.md, existing pipeline)

---
*Architecture research for: Produkt-Video-Generator*
*Researched: 2026-02-24*
