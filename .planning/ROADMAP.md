# Roadmap: Produkt Video Generator

## Overview

Ziel ist ein CLI-first Workflow, der aus einem Produkt-Input ein vollstaendiges, verkaufsorientiertes Video erzeugt. Die Roadmap folgt der Pipeline-Logik (Input/Config → Skript/Trends → Video → Metadaten/Resilienz) und stellt sicher, dass Nutzer schrittweise verifizierbare Ergebnisse erhalten.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [ ] **Phase 1: CLI & Output-Fundament** - Eingabe, Konfiguration und stabile Output-Namen funktionieren.
- [ ] **Phase 2: Trends & Sales-Skript** - DACH-Trends liefern ein konsistentes Sales-Skript mit visuellen Cues.
- [ ] **Phase 3: Video-Generierung** - Veo-Video folgt dem Skript und haelt Laengenbudget ein.
- [ ] **Phase 4: Metadaten & Resilienz** - Meta-JSON und robuste Fehlerbehandlung liefern den End-to-End-Run.

## Phase Details

### Phase 1: CLI & Output-Fundament
**Goal**: Nutzer koennen das Tool mit sauberer Konfiguration starten und erhalten stabile Output-Dateinamen.
**Depends on**: Nothing (first phase)
**Requirements**: CLI-01, CLI-03, CLI-04
**Success Criteria** (what must be TRUE):
  1. Nutzer kann Produkt/Topic per CLI-Argument oder interaktiv eingeben und der Run startet.
  2. Fehlende Pflicht-ENVs werden vor dem Run klar gemeldet und blockieren nachvollziehbar.
  3. Output-Dateien werden mit konsistenter Normalisierung benannt und im Zielverzeichnis angelegt.
**Plans**: 1 plan

Plans:
- [ ] 01-01-PLAN.md — CLI-Input-Flow, klare ENV-Fehler, stabile Output-Namen

### Phase 2: Trends & Sales-Skript
**Goal**: Nutzer erhalten ein verkaufsorientiertes Skript, das DACH-Trends nutzt und Veo-Cues enthaelt.
**Depends on**: Phase 1
**Requirements**: SCR-01, SCR-02, SCR-03, RES-01
**Success Criteria** (what must be TRUE):
  1. Das generierte Skript folgt dem Hook/Solution/Benefits/CTA-Framework und ist klar erkennbar.
  2. Das Skript enthaelt kurze visuelle Cues in Klammern, die fuer Veo nutzbar sind.
  3. Nutzer kann ein Tonalitaets-Profil (z. B. B2B/B2C) konfigurieren und sieht dessen Wirkung im Skript.
  4. Bei Trend-Fehlern wird ein DACH-relevanter Fallback genutzt, sodass der Run ein Skript liefert.
**Plans**: TBD

### Phase 3: Video-Generierung
**Goal**: Nutzer erhalten ein Veo-Video, das zum Skript passt und das Zeitbudget einhaelt.
**Depends on**: Phase 2
**Requirements**: VID-01, VID-02, VID-03
**Success Criteria** (what must be TRUE):
  1. Ein Video wird ueber Veo generiert und als Datei gespeichert.
  2. Die Videolaenge liegt innerhalb des konfigurierten Zeitbudgets.
  3. Nutzer kann nachvollziehen, dass der Veo-Prompt konsistent aus dem Skript abgeleitet ist.
**Plans**: TBD

### Phase 4: Metadaten & Resilienz
**Goal**: Nutzer erhalten Meta-JSON und einen stabilen End-to-End-Run trotz externer Ausfaelle.
**Depends on**: Phase 3
**Requirements**: META-01, RES-02, CLI-02
**Success Criteria** (what must be TRUE):
  1. Nach einem Lauf existieren Skript, Video und Meta-JSON ohne manuelle Zwischenschritte.
  2. Meta-JSON enthaelt Titel, Beschreibung und Tags passend zum generierten Skript.
  3. Bei API-Ausfaellen werden Retries/Backoff angewendet und der Run liefert bestmoegliche Outputs.
**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. CLI & Output-Fundament | 1/1 | Complete | 2026-02-24 |
| 2. Trends & Sales-Skript | 0/TBD | Not started | - |
| 3. Video-Generierung | 0/TBD | Not started | - |
| 4. Metadaten & Resilienz | 0/TBD | Not started | - |
