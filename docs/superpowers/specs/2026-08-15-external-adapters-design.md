# External Adapter Seams

## Ziel

Die externen Dienste des Product Video Generators werden hinter kleinen
Interfaces verborgen. Die Pipeline bleibt fachlich unverändert; Prompts,
Fallbacks, Dateinamen und CLI-Verträge bleiben stabil.

## Architektur

Ein `adapters.py`-Modul definiert `TrendProvider`, `TextGenerator`,
`VideoRenderer`, `MediaStore` und die zugehörigen Ergebnisverträge. Die
bisherigen Google-Trends-, Gemini/Veo- und Dateisystemzugriffe werden als
konkrete Adapter implementiert. `ProductVideoGenerator` akzeptiert optionale
Adapter und verwendet standardmäßig die Produktionsadapter.

Tests injizieren In-Memory-Adapter. Dadurch werden keine echten Netzwerkaufrufe
benötigt und die fachlichen Methoden werden über ihre externe seam getestet.

## Umfang

- Adapter für Trends, Text, Video und Artefaktpersistenz.
- Bestehende Retry-/Fallback-Logik bleibt erhalten.
- Keine neuen Laufzeitabhängigkeiten.
- Keine Änderung an CLI-Ausgabe oder Manifestformat.
- Deterministische Tests für Injektion und die bestehenden Produktionspfade.
