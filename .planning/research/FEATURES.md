# Feature Research

**Domain:** Produkt-Video-Generator (Python CLI, Gemini/Veo)
**Researched:** 2026-02-24
**Confidence:** LOW

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = product feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| CLI-Eingabe eines Produkts/Topics | Minimaler Einstieg ohne UI | LOW | Ein Argument oder Prompt; klare Usage-Hilfe |
| End-to-End-Run (Skript + Video + Metadaten) | Kernversprechen: ein Durchlauf | MEDIUM | Orchestrierung, Fehlerpropagation, Statusausgaben |
| Skript-Generierung im Sales-Framework | Erwartete Werbewirkung | MEDIUM | Hook, Solution, Benefits, CTA als feste Struktur |
| Video-Generierung ueber Veo | Hauptoutput ist Video | HIGH | Modell-Call, Zeitlimits, Fehler-Handling |
| Output-Dateien konsistent benennen | Nutzer erwartet Wiederfindbarkeit | LOW | Topic-Normalisierung, klare Pfade |
| Konfiguration via .env | Standard fuer API-Keys | LOW | Validierung, hilfreiche Fehlermeldungen |
| DACH-fokussierte Trends + Fallback | Relevanz + Robustheit | MEDIUM | geo=DE, Fallback-Themenliste |
| Lauf-Logs/Status | Transparenz bei langer Laufzeit | LOW | Schrittweises Logging |

### Differentiators (Competitive Advantage)

Features that set the product apart. Not required, but valuable.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Skript + Veo-Prompt-Kopplung | Konsistente Visuals zum Script | MEDIUM | Visuelle Cues pro Abschnitt |
| Tonalitaets-Profile (z. B. B2B/B2C) | Mehr Passung zum Zielpublikum | MEDIUM | Prompt-Templates, konfigurierbar |
| Qualitaets-Fallbacks bei API-Ausfaellen | Verlaesslichkeit statt Abbruch | MEDIUM | Graceful Degradation pro Schritt |
| Metadaten-Optimierung (SEO/Plattform) | Upload spart Zeit | LOW | Titel/Tags/Description Regeln |
| Deterministische Re-Runs | Reproduzierbare Outputs | MEDIUM | Seed/Cache-Strategie |
| Lokale Vorschau-Assets | Schnellere Review-Schleife | LOW | Skript + Metadaten im Ordner |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create problems.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Web-UI im MVP | Bequeme Bedienung | Hoher Overhead, Scope-Creep | CLI-Workflow + gute Hilfeausgaben |
| Batch-Verarbeitung vieler Produkte | Skalierung | Erhoeht Komplexitaet, Kosten, Fehlerflaeche | Single-Run, spaeter Batch |
| Externe TTS/Mixing-Pipeline | Kontrolle ueber Audio | Bricht Constraint, mehr Abhaengigkeiten | Veo-Audio nutzen |
| Vollautomatische Multi-Plattform-Uploads | End-to-End | API-Limits, Compliance, Auth | Export fertiger Metadaten |

## Feature Dependencies

```
CLI-Eingabe
    └──requires──> Konfiguration via .env
                       └──requires──> API-Clients (Gemini/Veo)

Skript-Generierung
    └──requires──> Trend-Recherche (DE) oder Fallback

Video-Generierung
    └──requires──> Skript-Generierung
                       └──requires──> Output-Dateibenennung

Metadaten-Optimierung
    └──enhances──> End-to-End-Run

Deterministische Re-Runs ──conflicts──> Stochastische Prompt-Varianten
```

### Dependency Notes

- **CLI-Eingabe requires Konfiguration via .env:** Ohne Keys kein API-Zugriff.
- **Skript-Generierung requires Trend-Recherche:** Trends liefern Input; Fallback verhindert Blocker.
- **Video-Generierung requires Skript-Generierung:** Veo-Prompt basiert auf Script.
- **Metadaten-Optimierung enhances End-to-End-Run:** Mehr Nutzen ohne den Flow zu blockieren.
- **Deterministische Re-Runs conflicts with stochastischen Varianten:** Reproduzierbarkeit vs. Vielfalt.

## MVP Definition

### Launch With (v1)

Minimum viable product — what's needed to validate the concept.

- [ ] CLI-Eingabe eines Produkts/Topics — Basis-UX fuer Single-Run
- [ ] End-to-End-Run (Skript + Video + Metadaten) — Kernwert
- [ ] Sales-Skript (Hook/Solution/Benefits/CTA) — Werbewirkung
- [ ] Video-Generierung via Veo — Hauptoutput
- [ ] Output-Dateien konsistent benennen — Wiederauffindbarkeit
- [ ] .env-Konfiguration + Validierung — Zuverlaessiger Betrieb

### Add After Validation (v1.x)

Features to add once core is working.

- [ ] Tonalitaets-Profile — wenn Zielgruppen variieren
- [ ] Qualitaets-Fallbacks pro Schritt — wenn API-Stabilitaet schwankt
- [ ] Metadaten-Optimierung — wenn Upload-Pipeline entsteht

### Future Consideration (v2+)

Features to defer until product-market fit is established.

- [ ] Deterministische Re-Runs — wenn Reproduzierbarkeit gefordert wird
- [ ] Batch-Verarbeitung — wenn Single-Run stabil und gefragt ist

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| End-to-End-Run | HIGH | MEDIUM | P1 |
| Sales-Skript-Framework | HIGH | MEDIUM | P1 |
| Video-Generierung via Veo | HIGH | HIGH | P1 |
| Output-Dateibenennung | MEDIUM | LOW | P1 |
| .env-Konfiguration | MEDIUM | LOW | P1 |
| Trend-Recherche + Fallback | MEDIUM | MEDIUM | P2 |
| Tonalitaets-Profile | MEDIUM | MEDIUM | P2 |
| Metadaten-Optimierung | MEDIUM | LOW | P2 |
| Deterministische Re-Runs | LOW | MEDIUM | P3 |

**Priority key:**
- P1: Must have for launch
- P2: Should have, add when possible
- P3: Nice to have, future consideration

## Competitor Feature Analysis

| Feature | Competitor A | Competitor B | Our Approach |
|---------|--------------|--------------|--------------|
| End-to-End-Run | Unbekannt | Unbekannt | CLI-One-Shot, klare Outputs |
| Sales-Skript-Framework | Unbekannt | Unbekannt | Hook/Solution/Benefits/CTA |
| Video-Generierung | Unbekannt | Unbekannt | Veo als Renderer |

## Sources

- Keine externen Quellen recherchiert (Tooling fuer WebSearch nicht verfuegbar).

---
*Feature research for: Produkt-Video-Generator*
*Researched: 2026-02-24*
