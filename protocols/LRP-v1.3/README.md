# IrsanAI LRP v1.3 — Language Resonance Protocol

## Overview
LRP (Language Resonance Protocol) ist ein strukturiertes Prompting-Protokoll, das Ambiguität in LLM-Interaktionen eliminiert. Es trennt klar Context, Task, Constraints und Output-Format und führt einen "Resonance Check" durch, bevor die Aufgabe ausgeführt wird.

## Kern-Komponenten
1. **Context Layer** — Stabile Fakten, Rollen, Hintergrund (bleibt über alle Requests gleich).
2. **Task Layer** — Das konkrete Ziel (ein präziser Satz).
3. **Constraint Layer** — Harte und weiche Regeln (Format, Wortlimits, verbotene Outputs, Ton).
4. **Output Format** — Exaktes Schema (JSON, Markdown, Tabelle etc.).

## Resonance Check (das Herzstück)
Vor der finalen Antwort muss ein LRP-kompatibler Agent:
1. Die interpretierte Context/Task/Constraints kurz zurückspiegeln ("Resonance Echo").
2. Bei Unklarheit explizit Bestätigung einholen.
3. Bei voller Resonanz die Aufgabe ausführen.

Das verhindert stille Fehlinterpretationen und erzwingt Alignment.

## LRP Template (JSON)
```json
{
  "lrp_version": "1.3",
  "context": {
    "role": "Systemrolle / Beschreibung",
    "background": "Persistente Fakten / Referenzen",
    "assumptions": ["Annahme A", "Annahme B"]
  },
  "task": {
    "goal": "Ein-Satz-Beschreibung des gewünschten Outputs",
    "priority": "high/normal/low"
  },
  "constraints": {
    "hard": ["Keine privaten Keys verraten", "max_tokens: 400"],
    "soft": ["Konzise Sätze bevorzugen", "Technisches Vokabular wo passend"]
  },
  "output_format": {
    "type": "json|markdown|text|table",
    "schema": {
      "field1": "string",
      "field2": "integer",
      "notes": "string (optional)"
    }
  },
  "resonance_check": {
    "required": true,
    "echo_max_tokens": 80
  }
}
