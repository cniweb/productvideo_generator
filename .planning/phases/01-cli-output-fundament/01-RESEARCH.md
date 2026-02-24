# Phase 1: CLI & Output-Fundament - Research

**Researched:** 2026-02-25
**Domain:** CLI-Input, ENV-Validierung, Output-Normalisierung (Python CLI)
**Confidence:** MEDIUM

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
### CLI-Eingabe
- Prioritaet: CLI-Argument > stdin > interaktiver Prompt
- Leerer/zu kurzer Topic-Input wird blockiert (Minimallaenge erzwingen)
- Fehlende Flags/ENV erhalten explizite Defaults, die im Output genannt werden
- Interaktiver Prompt enthaelt ein Beispiel-Topic

### Fehlertexte
- Struktur: Kurz + konkrete naechste Aktion
- ENV-Fehler: Fail fast (Run bricht sofort ab)
- Fehlende Output-Pfade werden automatisch angelegt
- Fehlende ENV-Keys werden als konkrete Liste inkl. Beispiel kommuniziert

### Claude's Discretion
- Genaue Minimallaenge fuer Topic-Input
- Exaktes Prompt-Layout (Formatting/Spacing)

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| CLI-01 | Nutzer kann Produkt/Topic per CLI-Argument oder Prompt eingeben | CLI-Parsing-Flow (Argument > stdin > Prompt) mit validiertem Input und Beispiel-Topic im Prompt. |
| CLI-03 | Pflicht-ENVs werden validiert und klar gemeldet (.env/OS) | Fail-fast ENV-Check mit Liste fehlender Keys, Beispielsnippet und naechstem Schritt. |
| CLI-04 | Output-Dateien folgen konsistenter Namens- und Normalisierungslogik | Zentrale Normalisierung (Topic -> Dateiname) fuer Skript, Video, Metadaten. |
</phase_requirements>

## Summary

Die Basis fuer Phase 1 ist bereits im Code sichtbar: `.env` wird geladen, Pflicht-ENVs werden geprueft, und Output-Dateien werden im Zielverzeichnis geschrieben. Was fehlt, ist ein klar definierter CLI-Eingabeflow (Argument > stdin > Prompt) mit blockierender Validierung fuer zu kurze/leer Inputs sowie eine einheitliche Normalisierung des Topics fuer Dateinamen. Beides muss in `productvideo_generator.py` zentralisiert werden, um Konsistenz zwischen Skript-, Video- und Metadatenpfaden zu sichern.

Die ENV-Validierung ist schon als Fail-fast-Mechanik vorhanden (`_check_env_file`, `_require_env`), jedoch braucht Phase 1 klare Fehlermeldungen mit konkreten naechsten Schritten, einer Liste der fehlenden Keys und einem Beispiel. Zudem sollen fehlende Output-Pfade automatisch angelegt werden; das passiert bereits bei `_initialize_config()` (os.makedirs), muss aber bei der Planung beruecksichtigt und in Fehlermeldungen konsistent kommuniziert werden.

Die Normalisierung der Dateinamen sollte als einzelne Funktion umgesetzt werden und von allen Output-Dateien genutzt werden. Aktuell wird nur Leerzeichen-zu-Unterstrich ersetzt, was bei Sonderzeichen, Schraegstrichen oder sehr kurzen Inputs instabil ist (insbesondere auf Windows). Phase 1 sollte robuste Normalisierung definieren (z. B. Whitelist fuer Zeichen, Collapse von Leerraum, Trim, Mindestlaenge) und die gleiche Logik fuer `_script.txt`, `.mp4` und `_meta.json` verwenden.

**Primary recommendation:** Einfuehrung eines zentralen CLI-Input-Handlers und einer `normalize_topic()`-Funktion, die zusammen ENV-Validierung, Input-Prioritaet und konsistente Dateinamen garantieren.

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.10+ (CI 3.13) | CLI, Dateisystem, IO | Bereits Projektbasis; keine neuen Dependencies noetig. |
| python-dotenv | current (requirements.txt) | .env laden | Bereits im Code; standard fuer .env Workflows. |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| argparse (stdlib) | Python stdlib | CLI-Argumente parsen | Wenn CLI-Argumente strukturiert und erweiterbar sein sollen. |
| pathlib (stdlib) | Python stdlib | Dateipfade robust bauen | Fuer konsistente Pfadmanipulationen. |
| re/unicodedata (stdlib) | Python stdlib | Dateinamen normalisieren | Wenn Sonderzeichen/Whitespace bereinigt werden. |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| argparse | click/typer | Extra Abhaengigkeiten; nicht noetig fuer Phase 1. |

**Installation:**
```bash
python -m pip install -r requirements.txt
```

## Architecture Patterns

### Recommended Project Structure
```
productvideo_generator.py  # CLI entry + Pipeline
tests/                     # pytest
```

### Pattern 1: Zentraler Input-Flow
**What:** Ein einzelner Pfad bestimmt Topic-Input: CLI-Argument, sonst stdin (Pipe), sonst interaktiver Prompt mit Beispiel. Validierung erfolgt vor Run-Start.
**When to use:** Immer beim CLI-Start (Phase 1).
**Example:**
```python
# Source: productvideo_generator.py
try:
    topic = input("Produkt/Thema (Leer lassen fuer Trend): ").strip()
except EOFError:
    topic = ""
```

### Pattern 2: Fail-fast ENV-Validation
**What:** Pflicht-ENVs werden geprueft, fehlende Keys gesammelt, Fehlermeldung mit naechster Aktion und Beispiel ausgegeben.
**When to use:** Vor jeglicher Verarbeitung/Netzwerkzugriff (Phase 1).
**Example:**
```python
# Source: productvideo_generator.py
missing_env = [name for name in REQUIRED_ENV_VARS if not os.getenv(name)]
if missing_env:
    _raise_env_error("Die .env Datei ist unvollstaendig oder leer.", missing=missing_env)
```

### Anti-Patterns to Avoid
- **Mehrere Normalisierungsstellen:** Fuehrt zu inkonsistenten Dateinamen zwischen Skript, Video und Metadaten.
- **Input-Validierung nach Start:** Verbraucht API-Calls, bevor Fehler sichtbar sind.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| CLI-Parsing | Eigene argv-Parser-Logik | argparse (stdlib) | Vermeidet Edge-Cases und erhaelt standardisierte Hilfe-Ausgaben. |
| Pfad-Handling | String-Konkatenation | pathlib / os.path | Plattformuebergreifend, weniger Fehler. |

**Key insight:** Stabilitaet und Fehlertexte entstehen durch konsistente, zentrale Hilfsfunktionen statt duplizierter String-Manipulation.

## Common Pitfalls

### Pitfall 1: Ungueltige Dateinamen durch Topic
**What goes wrong:** Sonderzeichen, Slashes oder sehr kurze Inputs fuehren zu ungueltigen Pfaden oder Ueberschreibungen.
**Why it happens:** Normalisierung beschraenkt sich nur auf Leerzeichenersetzung.
**How to avoid:** `normalize_topic()` mit Whitelist, Collapse von Whitespace und Mindestlaenge.
**Warning signs:** Fehler beim Schreiben, unerwartete Dateien, unterschiedliche Namen pro Output.

### Pitfall 2: Input-Prioritaet ignoriert
**What goes wrong:** Piped Input oder CLI-Argumente werden ueberschrieben vom Prompt.
**Why it happens:** `input()` wird immer ausgefuehrt, egal ob argv/stdin vorhanden sind.
**How to avoid:** Expliziter Prioritaets-Flow (Argument > stdin > Prompt).
**Warning signs:** Automatisierte Runs haengen oder nutzen falsches Topic.

### Pitfall 3: Fehlende ENV-Keys werden zu spaet erkannt
**What goes wrong:** Script startet, aber scheitert erst bei API-Aufruf.
**Why it happens:** ENV-Check passiert zu spaet oder ohne klare Liste der fehlenden Keys.
**How to avoid:** Fail-fast vor Run-Start, fehlende Keys als Liste ausgeben.
**Warning signs:** Run startet, bricht spaeter mit unklarem Fehler ab.

## Code Examples

Verified patterns from project sources:

### Fail-fast ENV-Check
```python
# Source: productvideo_generator.py
def _check_env_file():
    if not os.path.exists(ENV_FILE) and not all(os.getenv(var) for var in REQUIRED_ENV_VARS):
        _raise_env_error("Keine .env Datei gefunden und nicht alle Umgebungsvariablen sind gesetzt.")
```

### Output-Datei schreiben
```python
# Source: productvideo_generator.py
script_filename = f"{self.topic.replace(' ', '_')}_script.txt"
script_path = os.path.join(OUTPUT_DIR, script_filename)
with open(script_path, "w", encoding="utf-8") as f:
    f.write(self.script_content)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Direkte input()-Abfrage | Prioritaets-Flow (Argument > stdin > Prompt) | Phase 1 | Bessere CLI-Automation und stabiler Run-Start. |

**Deprecated/outdated:**
- Nur `replace(' ', '_')` fuer Dateinamen ist zu schwach; robuste Normalisierung ist erforderlich.

## Open Questions

1. **Minimallaenge fuer Topic-Input**
   - What we know: Min Laenge muss erzwungen werden (Decision).
   - What's unclear: Exakter Wert.
   - Recommendation: Standard 3 Zeichen fuer Blocker, dokumentieren und im Prompt nennen.

2. **Prompt-Layout fuer interaktive Eingabe**
   - What we know: Prompt braucht Beispiel-Topic.
   - What's unclear: Formatierung/Spacing.
   - Recommendation: Einzeilig mit Beispiel in Klammern, damit Pipes/Automation nicht stoeren.

## Sources

### Primary (HIGH confidence)
- productvideo_generator.py - CLI-Eingabe, ENV-Checks, Output-Schreiben
- tests/test_productvideo_generator.py - Output-Assertions und Test-Setup
- requirements.txt - Abhaengigkeiten
- run.sh - aktueller CLI-Start/ stdin-Flow
- .planning/phases/01-cli-output-fundament/01-CONTEXT.md - User Decisions
- .planning/REQUIREMENTS.md - Phase Requirements

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - basiert auf Repo-Dateien und CI-Konfiguration.
- Architecture: MEDIUM - Input-Flow/Normalisierung abgeleitet aus Entscheidungen + aktuellem Code.
- Pitfalls: MEDIUM - aus aktuellem Verhalten und bekannten CLI-Datei-Edge-Cases.

**Research date:** 2026-02-25
**Valid until:** 2026-03-27
