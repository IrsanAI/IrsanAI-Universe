```text
██╗██████╗ ███████╗ █████╗ ███╗   ██╗    █████╗ ██╗    ██╗██╗   ██╗███╗   ██╗██╗██╗   ██╗███████╗██████╗ ███████╗
██║██╔══██╗██╔════╝██╔══██╗████╗  ██║   ██╔══██╗██║    ██║██║   ██║████╗  ██║██║██║   ██║██╔════╝██╔══██╗██╔════╝
██║██████╔╝███████╗███████║██╔██╗ ██║   ███████║██║ █╗ ██║██║   ██║██╔██╗ ██║██║██║   ██║█████╗  ██████╔╝███████╗
██║██╔══██╗╚════██║██╔══██║██║╚██╗██║   ██╔══██║██║███╗██║██║   ██║██║╚██╗██║██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║
██║██║  ██║███████║██║  ██║██║ ╚████║██╗██║  ██║╚███╔███╔╝╚██████╔╝██║ ╚████║██║ ╚████╔╝ ███████╗██║  ██║███████║
╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝
```

# IrsanAI Universe

**Spec-First Multi-Agent Resonance Framework**  
IrsanAI Universe defines protocols for high-fidelity reasoning across human prompts and cooperating AI agents. The repository has moved from conceptual manifesto to implementation-ready technical framework with explicit schemas, conflict-resolution logic, and measurable quality targets.

## Core Objective

Reduce semantic noise while maximizing resonance:

- **Noise** = ambiguity, unsupported assumptions, hallucinated drift.
- **Resonance** = preservation of user intent, evidence traceability, and agent alignment.
- **Target** = measurable semantic fidelity of **0.98** in controlled benchmark settings.

## Protocol Stack

### 1) NTF — Neural Translation Framework
A deterministic-normalized transformation layer from user text to canonical semantic form.

**Responsibilities**
- Normalize lexical variance (aliases, multilingual terms, abbreviations).
- Extract invariant task intent.
- Encode structure for downstream LRP/PDP processing.

**Output Guarantees**
- Canonical intent object.
- Confidence and provenance metadata.
- Evaluability against benchmark pairs.

### 2) LRP — Logic Resonance Protocol
An agent-to-agent transfer protocol that preserves logical constraints and suppresses hallucination through structured evidence binding.

**Responsibilities**
- Serialize reasoning state as bounded JSON.
- Attach each claim to either source evidence or derivation rule.
- Enforce contradiction checks before message handoff.

### 3) PDP — Perspective-Driven Protocol
A multi-perspective consensus protocol for heterogeneous model ecosystems (e.g., Grok, Gemini, Claude).

**Responsibilities**
- Run perspective-specialized passes on the same canonical task.
- Resolve conflicts through weighted voting and synthesis-relay.
- Emit final consensus with dissent trace.

## Repository Layout (Spec-First)

```text
IrsanAI-Universe/
├── README.md
├── TECHNICAL_SPEC.md
├── CONSENSUS_MONUMENT.md
├── spec/                  # Protocol and schema artifacts (JSON schema, ADRs, formal rules)
├── examples/              # Input/output examples for NTF, LRP, PDP
├── eval/                  # Benchmark scripts, metrics, reproducibility harness
│   └── ntf_bench.py
└── src/                   # Future reference implementations
```

## Implementation Roadmap

### Phase A — Schema Hardening
- Formalize NTF canonical object schema.
- Freeze LRP message templates with validation rules.
- Define PDP consensus envelope and dissent representation.

### Phase B — Evaluation Infrastructure
- Build `eval/ntf_bench.py` for semantic fidelity tracking.
- Curate benchmark corpus (prompt-paraphrase-intent triples).
- Add pass/fail thresholds and trend reporting.

### Phase C — Execution Layer
- Implement protocol runtime in `src/`.
- Integrate model adapters and replay logs.
- Publish deterministic test vectors under `examples/`.

## Definition of Done

A protocol revision is considered complete when:
1. Schema validates against all examples.
2. Benchmark fidelity remains at/above target.
3. Consensus conflicts are reproducible and auditable.
4. Changes include migration notes and compatibility status.

## Immediate Next Step

Read **TECHNICAL_SPEC.md** for exact JSON templates, benchmark methodology, and consensus rule implementation details.
