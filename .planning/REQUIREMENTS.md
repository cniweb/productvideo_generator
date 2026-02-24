# Requirements: Produkt Video Generator

**Defined:** 2026-02-24
**Core Value:** Ein einziger CLI-Aufruf erzeugt schnell ein vollständiges Produkt-Video (Skript, Video, Metadaten).

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### CLI & Konfiguration

- [x] **CLI-01**: Nutzer kann Produkt/Topic per CLI-Argument oder Prompt eingeben
- [ ] **CLI-02**: Ein einzelner Lauf erzeugt Skript, Video und Metadaten ohne manuelle Zwischenschritte
- [x] **CLI-03**: Pflicht-ENVs werden validiert und klar gemeldet (.env/OS)
- [x] **CLI-04**: Output-Dateien folgen konsistenter Namens- und Normalisierungslogik

### Skript

- [ ] **SCR-01**: Skript folgt dem Sales-Framework (Hook, Solution, Benefits, CTA)
- [ ] **SCR-02**: Skript enthaelt kurze visuelle Cues fuer Veo-Prompts
- [ ] **SCR-03**: Tonalitaets-Profile (z. B. B2B/B2C) sind konfigurierbar

### Video & Metadaten

- [ ] **VID-01**: Video wird ueber Veo generiert und gespeichert
- [ ] **VID-02**: Laengensteuerung haelt das Zeitbudget ein
- [ ] **VID-03**: Skript und Veo-Prompt sind konsistent gekoppelt
- [ ] **META-01**: Metadaten-JSON wird erzeugt (Titel, Beschreibung, Tags)

### Resilienz

- [ ] **RES-01**: DACH-Trends (DE) werden genutzt, mit Fallback bei Fehlern
- [ ] **RES-02**: API-Ausfaelle werden mit Retry/Backoff abgefedert

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Quality & Observability

- **QA-01**: Prompt-Versioning und Run-IDs fuer Reproduzierbarkeit
- **QA-02**: Erweiterte QA-Checks vor Video-Render

### Skalierung

- **SCALE-01**: Batch-Verarbeitung mehrerer Produkte in einem Lauf

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Web-UI | CLI-Workflow ist ausreichend |
| Externe TTS/Mixing-Pipeline | Veo uebernimmt Audio/Musik/Video |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| CLI-01 | Phase 1 | Complete |
| CLI-03 | Phase 1 | Complete |
| CLI-04 | Phase 1 | Complete |
| SCR-01 | Phase 2 | Pending |
| SCR-02 | Phase 2 | Pending |
| SCR-03 | Phase 2 | Pending |
| RES-01 | Phase 2 | Pending |
| VID-01 | Phase 3 | Pending |
| VID-02 | Phase 3 | Pending |
| VID-03 | Phase 3 | Pending |
| META-01 | Phase 4 | Pending |
| RES-02 | Phase 4 | Pending |
| CLI-02 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 13 total
- Mapped to phases: 13
- Unmapped: 0 ✓

---
*Requirements defined: 2026-02-24*
*Last updated: 2026-02-24 after initial definition*
