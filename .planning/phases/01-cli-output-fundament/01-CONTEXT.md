# Phase 1: CLI & Output-Fundament - Context

**Gathered:** 2026-02-24
**Status:** Ready for planning

<domain>
## Phase Boundary

CLI-Input, .env-Validierung und konsistente Output-Dateinamen fuer den Start des Runs. Keine neuen Features ausserhalb des Inputs/Configs/Outputs.

</domain>

<decisions>
## Implementation Decisions

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

</decisions>

<specifics>
## Specific Ideas

- Beispiel-Topic im Prompt, um die erwartete Eingabe klar zu machen

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 01-cli-output-fundament*
*Context gathered: 2026-02-24*
