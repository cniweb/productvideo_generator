# Pitfalls Research

**Domain:** Product video generator (Python CLI, Gemini + Veo)
**Researched:** 2026-02-24
**Confidence:** LOW

## Critical Pitfalls

### Pitfall 1: Script-zu-Video-Drift (Sales-Text passt nicht zum Video)

**What goes wrong:**
Das Skript ist verkaufsstark, aber die visuellen Hinweise sind zu vage oder widerspruechlich. Das generierte Video zeigt unpassende Szenen oder generische Bilder, die die Botschaft verwässern.

**Why it happens:**
Prompting fuer LLM und Video-Model wird getrennt optimiert; visuelle Cues fehlen oder sind nicht kurz genug fuer Veo.

**How to avoid:**
Einheitliches Skriptformat erzwingen (Hook, Solution, Benefits, CTA + kurze visuelle Klammern), automatische Validierung fuer Cue-Laenge/Anzahl, und ein Mapping von Textabschnitt -> visueller Cue.

**Warning signs:**
Wiederholte Szenen, generische Stock-Optik, oder Nutzerfeedback wie "Video zeigt etwas anderes als der Text".

**Phase to address:**
Phase 2 (Skript-Generierung) und Phase 3 (Video-Generierung).

---

### Pitfall 2: Laufzeit-Mismatch (Skript laenger als Video-Zeitbudget)

**What goes wrong:**
Das Skript ist laenger als das erlaubte Video-Maximum; Veo kuerzt oder bricht ab. CTA/Benefits fehlen im finalen Output.

**Why it happens:**
Keine harte Laengensteuerung oder Zeitschatzung (WPM) vor Video-Call.

**How to avoid:**
Max-Sekunden aus Config als harte Obergrenze nutzen, automatische Skript-Kuerzung mit Prioritaet (CTA behalten), und Zeitschatzung per Tokens/WPM vor dem Video-Call.

**Warning signs:**
Unvollstaendige CTA, stark gekuerzte Enden, oder Video-Antworten mit "duration limit"-Hinweisen.

**Phase to address:**
Phase 2 (Skript-Generierung) und Phase 3 (Video-Generierung).

---

### Pitfall 3: Keine Resilienz bei externen Abhaengigkeiten

**What goes wrong:**
Ein Trend- oder Modell-Call faellt aus und die gesamte Pipeline stoppt. Keine Ausgabe-Dateien werden erstellt.

**Why it happens:**
Pipeline ist linear ohne Fallbacks/Retry; Fehler werden als fatal behandelt.

**How to avoid:**
Best-effort Fallbacks pro Schritt (z.B. Default-Trends), begrenzte Retries mit Backoff, und Teil-Outputs speichern (Skript auch wenn Video scheitert).

**Warning signs:**
Hohe Fehlerquote in Logs, wiederholte Abbrueche bei Rate-Limits, oder fehlende Dateien trotz erfolgreichem Vorlauf.

**Phase to address:**
Phase 1 (Grundlagen/Config) und Phase 4 (Reliability/Fehlerbehandlung).

---

### Pitfall 4: Output-Overwrites durch Topic-Normalisierung

**What goes wrong:**
Unterschiedliche Topics normalisieren auf den gleichen Dateinamen und ueberschreiben Skript/Video/Meta.

**Why it happens:**
Zu aggressive Normalisierung, fehlende Collision-Checks, keine Run-IDs.

**How to avoid:**
Collision-Check vor dem Schreiben, optionaler Suffix (Timestamp/Hash), und eine eindeutigere Normalisierung fuer DACH-Zeichen.

**Warning signs:**
Verschwundene alte Outputs oder "falsche" Metadaten bei neuen Runs.

**Phase to address:**
Phase 1 (Grundlagen/Config) und Phase 4 (Output/Datei-Management).

---

### Pitfall 5: Fehlende Reproduzierbarkeit (Prompt/Versionen nicht gespeichert)

**What goes wrong:**
Ergebnisse koennen nicht reproduziert oder verbessert werden, weil Prompt-Version, Config und Modell-Parameter fehlen.

**Why it happens:**
Fokus auf schnellen Output ohne Audit/Metadata.

**How to avoid:**
Prompt-Versionierung, Speichern der verwendeten Config im Meta-JSON, und eine Run-ID pro Durchlauf.

**Warning signs:**
"Warum sieht das heute anders aus?" ohne Antwort; keine Vergleichbarkeit zwischen Runs.

**Phase to address:**
Phase 4 (Metadata/Output) und Phase 5 (Qualitaet/Observability).

---

### Pitfall 6: Trend-Input ignoriert DACH-Relevanz

**What goes wrong:**
Skripte treffen nicht die Zielregion; Video wirkt generisch oder sprachlich unpassend.

**Why it happens:**
Trends werden global geholt oder Sprach-/Regionseinstellungen sind inkonsistent.

**How to avoid:**
Geo-Fokus DE als Default, Sprache strikt auf Deutsch, und Fallback-Listen fuer DACH-relevante Themen.

**Warning signs:**
Hohe Anzahl nicht-deutscher Begriffe oder Themen ohne lokalen Bezug.

**Phase to address:**
Phase 2 (Trend-Recherche) und Phase 3 (Skript-Generierung).

## Technical Debt Patterns

Shortcuts that seem reasonable but create long-term problems.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Kein Prompt-Versioning | Schnellere Umsetzung | Keine reproduzierbaren Verbesserungen | Nur im ersten Spike |
| Keine Output-Schemas | Flexibel, weniger Code | Bruechige Downstream-Tools | Nie in Produktionspfad |
| Ein monolithischer Prompt | Weniger Logik | Schwer zu steuern, mehr Drift | MVP, wenn eng getestet |

## Integration Gotchas

Common mistakes when connecting to external services.

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Gemini Text | Unklare Prompt-Constraints | Explizite Struktur (Hook/Solution/Benefits/CTA) und Langenlimit |
| Veo Video | Ignorieren von Dauer/Format | Parameter-Validierung (max seconds, aspect ratio) vor Request |
| Pytrends | Keine Rate-Limit-Strategie | Caching, Backoff, und Default-Trends |

## Performance Traps

Patterns that work at small scale but fail as usage grows.

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Kein Cache fuer Trends/Skripte | Wiederholte API-Calls | Cache pro Topic/Tag | Ab Dutzenden Runs/Tag |
| Serielles Warten ohne Timeouts | Lange Laufzeiten, Haenger | Timeouts pro Schritt | Bei instabilen APIs |
| Grosse Video-Dateien in RAM | Speicherdruck | Streamen/Speichern auf Disk | Bei HD/mehreren Runs |

## Security Mistakes

Domain-specific security issues beyond general web security.

| Mistake | Risk | Prevention |
|---------|------|------------|
| API-Keys in Logs | Key-Leak, Account-Missbrauch | Secrets maskieren, Logging-Filter |
| Topic als Pfad ohne Sanitizing | Path Traversal, Ueberschreiben | Strikte Normalisierung, Whitelist |
| Outputs in gemeinsam genutzten Ordnern | Datenleak | Projektspezifische Output-Dirs |

## UX Pitfalls

Common user experience mistakes in this domain.

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Keine klare Progress-Anzeige | Nutzer bricht Run ab | Schrittweises Logging + ETA |
| Skript nicht sichtbar | Keine qualitative Kontrolle | Skript als Output anzeigen/speichern |
| Fehlende Dry-Run/Preview | Unerwartete Kosten | Dry-Run mit Prompt-Preview |

## "Looks Done But Isn't" Checklist

Things that appear complete but are missing critical pieces.

- [ ] **Skript:** Hook/CTA fehlen trotz "fertig"-Status — pruefe Abschnitts-Validator.
- [ ] **Video:** Dauer OK, aber Inhalte nicht passend — pruefe Cue-Alignment.
- [ ] **Meta-JSON:** Titel/Tags leer — pruefe Pflichtfelder.
- [ ] **Outputs:** Dateien vorhanden, aber ueberschrieben — pruefe Collision-Check.

## Recovery Strategies

When pitfalls occur despite prevention, how to recover.

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Script-zu-Video-Drift | MEDIUM | Prompt-Template anpassen, Cue-Validator, Re-Run Video |
| Laufzeit-Mismatch | LOW | Skript kuerzen, CTA priorisieren, Re-Run Video |
| API-Ausfall | MEDIUM | Fallbacks aktivieren, Teil-Outputs speichern, Retry spaeter |

## Pitfall-to-Phase Mapping

How roadmap phases should address these pitfalls.

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Script-zu-Video-Drift | Phase 2-3 | Stichprobe: Video spiegelt jeden Skript-Block |
| Laufzeit-Mismatch | Phase 2 | WPM-Schaetzung <= max seconds |
| API-Ausfall | Phase 4 | Mehrere Runs ohne Vollabbruch |
| Output-Overwrites | Phase 1/4 | Keine ueberschriebenen Dateien bei 10 Topics |
| Reproduzierbarkeit | Phase 4/5 | Meta-JSON enthaelt Prompt+Config |
| DACH-Relevanz | Phase 2 | Trend-Inputs sind deutsch/DE-geo |

## Sources

- Erfahrungswissen zu generativen Pipelines (unverifiziert, LOW)

---
*Pitfalls research for: Product video generator (Python CLI, Gemini + Veo)*
*Researched: 2026-02-24*
