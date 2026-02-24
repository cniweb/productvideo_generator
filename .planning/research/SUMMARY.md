# Project Research Summary

**Project:** Product Video Generator (Veo Edition)
**Domain:** Produkt-Video-Generator (Python CLI mit Gemini/Veo)
**Researched:** 2026-02-24
**Confidence:** MEDIUM

## Executive Summary

Dieses Projekt ist ein Python-CLI-Produkt-Video-Generator, der Trends in DACH (DE) recherchiert, daraus ein verkaufsorientiertes Skript erstellt und per Veo ein Video rendert. Bewaehrte Umsetzung ist eine orchestrierte Pipeline mit klaren Schritten (Trends → Skript → Video → Metadaten) und einem Adapter-Layer fuer externe APIs, damit Tests, Fallbacks und robuste Fehlerbehandlung moeglich sind.

Empfohlen ist ein schlanker CLI-First-Ansatz mit stabilen Dateinamen, .env-Konfiguration und konsistentem Sales-Framework (Hook, Solution, Benefits, CTA). Kritische Risiken liegen in Drift zwischen Skript und Video, Laengen-Mismatch zum Video-Zeitbudget sowie fehlender Resilienz bei externen Abhaengigkeiten. Diese werden durch kurze visuelle Cues im Skript, harte Laengensteuerung, Retry/Backoff plus Best-Effort-Fallbacks und konsequentes Output-Management mitigiert.

## Key Findings

### Recommended Stack

Die Stack-Empfehlung favorisiert ein minimal-invasives Python-Setup mit offizieller Google-GenAI-SDK-Integration und bewussten Hilfsbibliotheken fuer Resilienz, CLI-UX und Validierung (Details in `.planning/research/STACK.md`). Kritisch ist Python >=3.10 sowie das aktuelle `google-genai` SDK.

**Core technologies:**
- **Python 3.10+**: Runtime fuer CLI/Pipeline — notwendig fuer SDK-Kompatibilitaet.
- **google-genai 1.64.0**: Gemini/Veo SDK — einheitliche API fuer Text + Video, offiziell gepflegt.
- **pytrends 4.9.2**: Trends-Zugriff — de-facto Standard ohne offizielle Trends-API.

### Expected Features

Die Feature-Research priorisiert einen End-to-End-Run mit Sales-Skript und Veo-Video, klaren Outputs und .env-Config als MVP (Details in `.planning/research/FEATURES.md`). Differenzierung entsteht ueber Skript↔Prompt-Kopplung, Tonalitaetsprofile und robuste Fallbacks. Web-UI, Batch-Runs und externe TTS sollen bewusst vermieden werden.

**Must have (table stakes):**
- CLI-Eingabe eines Produkts/Topics — minimaler Einstieg.
- End-to-End-Run (Skript + Video + Metadaten) — Kernversprechen.
- Sales-Skript (Hook/Solution/Benefits/CTA) — Werbewirkung.
- Video-Generierung via Veo — Hauptoutput.
- Output-Dateibenennung + .env-Konfiguration — Stabilitaet/Bedienbarkeit.

**Should have (competitive):**
- Skript + Veo-Prompt-Kopplung — konsistente Visuals.
- Tonalitaets-Profile — Zielgruppenpassung.
- Qualitaets-Fallbacks + Metadaten-Optimierung — Zuverlaessigkeit/Upload-Ready.

**Defer (v2+):**
- Deterministische Re-Runs — nur falls Reproduzierbarkeit gefordert ist.
- Batch-Verarbeitung — erst nach stabiler Single-Run-Pipeline.

### Architecture Approach

Die empfohlene Architektur ist eine orchestrierte Pipeline mit klaren Service-Grenzen und Adapter-Layern fuer Trends, LLM und Video (Details in `.planning/research/ARCHITECTURE.md`). Das erleichtert Tests, Fallbacks, Logging und spaetere Skalierung.

**Major components:**
1. **CLI/Orchestrator** — steuert Ablauf, Fehlerbehandlung und Reihenfolge.
2. **Trend/Script/Video/Metadata Services** — je Schritt klare Inputs/Outputs.
3. **Adapters + Output Writer** — kapseln externe APIs und persistieren Artefakte.

### Critical Pitfalls

1. **Script-zu-Video-Drift** — Skript muss kurze visuelle Cues enthalten und validiert werden.
2. **Laufzeit-Mismatch** — Laengenlimit vor Video-Call erzwingen, CTA priorisieren.
3. **Fehlende Resilienz bei API-Ausfaellen** — Retry/Backoff + Best-Effort-Fallbacks.
4. **Output-Overwrites durch Normalisierung** — Collision-Check/Suffixe nutzen.
5. **Fehlende Reproduzierbarkeit** — Prompt/Config in Meta-JSON speichern.

## Implications for Roadmap

Basierend auf Research ergibt sich eine 4-5-Phasen-Roadmap, die Abhaengigkeiten respektiert und zentrale Risiken frueh adressiert.

### Phase 1: Grundlagen & CLI-Stabilitaet
**Rationale:** Alles haengt an stabiler Konfiguration, Input-Normalisierung und Dateipfaden.
**Delivers:** CLI-Input, .env-Validierung, Topic-Normalisierung, Output-Verzeichnisse.
**Addresses:** CLI-Eingabe, .env-Konfiguration, Output-Dateibenennung.
**Avoids:** Output-Overwrites, Pfad-Unsicherheiten.

### Phase 2: Trend-Recherche + Sales-Skript
**Rationale:** Skript ist die zentrale Abhaengigkeit fuer Video und Metadaten.
**Delivers:** DACH-Trends mit Fallback, Sales-Skript (Hook/Solution/Benefits/CTA) inkl. visueller Cues.
**Addresses:** Trend-Recherche + Fallback, Sales-Skript-Framework.
**Avoids:** DACH-Irrelevanz, Script-zu-Video-Drift (Grundlage).

### Phase 3: Video-Generierung & Laengensteuerung
**Rationale:** Video haengt direkt vom Skript ab und birgt die hoechsten Risiken.
**Delivers:** Veo-Video-Call mit Zeitbudget, Prompt-Kopplung, robuste Fehlerbehandlung.
**Addresses:** Video-Generierung via Veo, Skript↔Prompt-Kopplung.
**Avoids:** Laufzeit-Mismatch, Drift zwischen Text und Visuals.

### Phase 4: Metadaten + Reliability/Resilience
**Rationale:** Erhoeht Nutzen ohne den Kernflow zu blockieren und stabilisiert die Pipeline.
**Delivers:** Meta-JSON, Teil-Outputs bei Fehlern, Retry/Backoff, Logging.
**Addresses:** Metadaten-Optimierung, Qualitaets-Fallbacks.
**Avoids:** Pipeline-Abbruch ohne Outputs, fehlende Reproduzierbarkeit.

### Phase 5 (optional): Qualitaet/Observability
**Rationale:** Erst nach stabilem MVP sinnvoll.
**Delivers:** Prompt-Versioning, Run-IDs, erweiterte Checks.
**Addresses:** Reproduzierbarkeit, QA-Checks.
**Avoids:** „Looks done but isn’t“ (fehlende CTA/Meta/Alignment).

### Phase Ordering Rationale

- Abhaengigkeiten aus der Pipeline erzwingen CLI/Config vor Skript, Skript vor Video.
- Adapter/Services-Pattern reduziert Risiko in API-Integrationen.
- Fruehe Laengen- und Cue-Validierung senkt Drift- und Duration-Risiken.

### Research Flags

Phasen likely needing deeper research waehrend Planung:
- **Phase 2:** Prompt-Design, Laengensteuerung, Cue-Validierung fuer Veo.
- **Phase 3:** Veo-API-Parameter, Timeouts, Fehlerszenarien.

Phasen mit Standard-Patterns (skip research-phase):
- **Phase 1:** CLI/.env/Input-Validierung, Output-Pfade (etabliert).
- **Phase 4:** Logging/Retry/Backoff/Meta-JSON (Standard-Python-Patterns).

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | MEDIUM | Offizielle SDK-Quellen, Versionen klar, keine tiefen Integrations-Checks. |
| Features | LOW | Keine externen Quellen; Priorisierung basiert auf Heuristik. |
| Architecture | MEDIUM | Standard-Pipeline-Pattern, aber ohne Vergleich mit konkreten Referenzprojekten. |
| Pitfalls | LOW | Erfahrungswissen, keine verifizierten Quellen. |

**Overall confidence:** MEDIUM

### Gaps to Address

- **Veo-spezifische Prompt/Timing-Grenzen**: vor Implementierung validieren (API-Limits, Dauer/Format).
- **Trend-API Zuverlaessigkeit**: Rate-Limits/Fallback-Strategie mit realen Tests bestaetigen.
- **Output-Normalisierung fuer DACH**: Collision-Checks mit echten Beispielen pruefen.

## Sources

### Primary (HIGH confidence)
- https://pypi.org/project/google-genai/ — SDK Version/Requirements
- https://googleapis.github.io/python-genai/ — Gemini/Veo SDK Nutzung

### Secondary (MEDIUM confidence)
- https://pypi.org/project/pytrends/ — Trends-Library Status
- https://pypi.org/project/python-dotenv/ — .env Handling
- https://pypi.org/project/tenacity/ — Retry/Backoff
- https://pypi.org/project/pydantic/ — Schema-Validierung
- https://pypi.org/project/typer/ — CLI Framework
- https://pypi.org/project/rich/ — CLI Output

### Tertiary (LOW confidence)
- `.planning/research/FEATURES.md` — Feature-Priorisierung ohne externe Quellen
- `.planning/research/PITFALLS.md` — Erfahrungsbasierte Risiken

---
*Research completed: 2026-02-24*
*Ready for roadmap: yes*
