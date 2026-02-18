```text
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                IRSANAI UNIVERSE                                     ║
║                    SPEC-FIRST TECHNICAL HARDENING DOCUMENT                          ║
║                  Noise→Signal Transformation | Resonance by Construction             ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
```

# TECHNICAL_SPEC.md

## 0. Scope

This document formalizes the IrsanAI protocol stack for technical implementation:

- **NTF** (Neural Translation Framework): semantic normalization and fidelity measurement.
- **LRP** (Logic Resonance Protocol): evidence-bound reasoning exchange with anti-hallucination controls.
- **PDP** (Perspective-Driven Protocol): multi-agent consensus and conflict-resolution mechanics.

The design principle is **spec-first**: behavior is defined by schemas and rules before runtime code.

---

## 1. NTF — Neural Translation Framework

## 1.1 Problem Statement
Natural-language prompts are noisy, under-specified, and style-dependent. NTF maps this variability into a canonical semantic representation while preserving intent invariants.

## 1.2 Canonical NTF Output (Template)

```json
{
  "ntf_version": "1.0.0",
  "task_id": "uuid-v4",
  "source": {
    "raw_input": "<original user message>",
    "language": "en",
    "timestamp_utc": "2026-02-14T10:30:00Z"
  },
  "semantic_core": {
    "intent": "<single sentence imperative objective>",
    "constraints": ["<hard constraints>"],
    "preferences": ["<soft constraints>"],
    "deliverables": ["<required artifacts>"],
    "acceptance_criteria": ["<success conditions>"]
  },
  "disambiguation": {
    "resolved_entities": [
      {
        "surface": "LRP",
        "canonical": "Logic Resonance Protocol",
        "confidence": 0.99
      }
    ],
    "open_questions": ["<if unresolved ambiguity remains>"]
  },
  "quality": {
    "semantic_fidelity_estimate": 0.0,
    "normalization_confidence": 0.0
  },
  "trace": {
    "normalization_steps": ["token_normalize", "constraint_extract", "intent_compress"],
    "evidence_links": ["line-span or source reference"]
  }
}
```

## 1.3 NTF Benchmark Methodology (0.98 Semantic Fidelity)

### Dataset Construction
- Build benchmark records as `(raw_prompt, canonical_intent, paraphrase_set)`.
- Include adversarial paraphrases: reordering, synonym swaps, omitted context, multilingual fragments.
- Partition into train/dev/test with zero leakage.

### Metric A: Embedding Cosine Similarity
- Encode model output intent and gold canonical intent with the same embedding model.
- Compute cosine similarity:
  - `sim = dot(a, b) / (||a|| * ||b||)`
- Track macro-average on test split.
- **Primary threshold**: `mean(sim) >= 0.98`.

### Metric B: LLM-as-a-Judge (Structured)
Judge prompt asks whether generated canonical object preserves:
1. Objective equivalence,
2. Constraint integrity,
3. Deliverable completeness,
4. No fabricated assumptions.

Outputs strict JSON scorecard with pass/fail + rationale.

### Final Score
`NTF_score = 0.7 * cosine_score + 0.3 * judge_score`

Release gate:
- `NTF_score >= 0.98`
- hallucination_rate < 0.5%
- zero critical constraint omissions.

## 1.4 `eval/ntf_bench.py` Concept

```python
"""
Conceptual benchmark harness for NTF fidelity.
Usage:
  python eval/ntf_bench.py --dataset eval/data/ntf_test.jsonl --mode cosine
  python eval/ntf_bench.py --dataset eval/data/ntf_test.jsonl --mode judge
"""

import argparse
import json
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Record:
    raw_prompt: str
    gold_intent: str
    system_intent: str


def cosine(a, b):
    num = sum(x * y for x, y in zip(a, b))
    den_a = sum(x * x for x in a) ** 0.5
    den_b = sum(y * y for y in b) ** 0.5
    return num / (den_a * den_b + 1e-12)


def embed(text: str) -> List[float]:
    # placeholder for embedding provider call
    raise NotImplementedError


def judge(gold: str, pred: str) -> float:
    # placeholder for LLM judge call; returns [0, 1]
    raise NotImplementedError


def run(records: List[Record], mode: str) -> Dict[str, float]:
    sims = []
    for r in records:
        if mode == "cosine":
            sims.append(cosine(embed(r.gold_intent), embed(r.system_intent)))
        else:
            sims.append(judge(r.gold_intent, r.system_intent))
    mean_score = sum(sims) / max(len(sims), 1)
    return {"count": len(sims), "mean_score": mean_score}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", required=True)
    p.add_argument("--mode", choices=["cosine", "judge"], default="cosine")
    args = p.parse_args()

    rows = []
    with open(args.dataset, "r", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            rows.append(Record(**d))

    report = run(rows, args.mode)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
```

---

## 2. LRP — Logic Resonance Protocol (Hardened)

## 2.1 Design Goal
Enable agent-to-agent exchange that is compact, auditable, and resistant to hallucinated reasoning.

## 2.2 LRP Message Template (Complete JSON)

```json
{
  "lrp_version": "1.0.0",
  "message_id": "uuid-v4",
  "conversation_id": "uuid-v4",
  "sender": {
    "agent_id": "gemini",
    "role": "analyst",
    "model": "gemini-2.x"
  },
  "receiver": {
    "agent_id": "claude",
    "role": "validator"
  },
  "intent_frame": {
    "task": "draft NTF benchmark method",
    "objective": "maximize semantic fidelity and reproducibility",
    "constraints": [
      "must include cosine metric",
      "must include judge metric",
      "must define release gate"
    ]
  },
  "reasoning_packet": {
    "claims": [
      {
        "claim_id": "c1",
        "text": "Cosine similarity captures semantic closeness for intent strings.",
        "type": "methodological",
        "confidence": 0.93,
        "supports": ["e1"],
        "depends_on": []
      }
    ],
    "derivations": [
      {
        "derivation_id": "d1",
        "rule": "weighted_combination",
        "inputs": ["c1", "c2"],
        "output": "c3"
      }
    ],
    "uncertainties": [
      {
        "topic": "embedding model drift",
        "impact": "medium",
        "mitigation": "pin model version"
      }
    ]
  },
  "evidence_registry": [
    {
      "evidence_id": "e1",
      "source_type": "spec",
      "source_ref": "TECHNICAL_SPEC.md#1.3",
      "quote": "Primary threshold: mean(sim) >= 0.98"
    }
  ],
  "integrity": {
    "contradiction_check": {
      "ran": true,
      "result": "pass",
      "conflicts": []
    },
    "hallucination_guard": {
      "unsupported_claims": [],
      "status": "pass"
    }
  },
  "handoff": {
    "required_actions": ["verify c1 against external benchmark literature"],
    "response_format": "lrp_message"
  }
}
```

## 2.3 Input-to-Resonance Examples (Anti-Hallucination)

### Example 1 — Unsupported Metric Claim is Blocked
**Input (Agent A):** “Fidelity can be measured by token overlap only; no embeddings needed.”  
**LRP Control:** claim enters with no evidence links → `hallucination_guard.unsupported_claims=[c1]`  
**Resonance Output:** Agent B rejects c1, requests evidence or replacement metric. Drift is prevented.

### Example 2 — Constraint Omission Detected
**Input (Agent A):** Provides benchmark method but omits “judge metric” constraint.  
**LRP Control:** `intent_frame.constraints` requires judge metric; contradiction/omission check flags gap.  
**Resonance Output:** Agent B returns structured diff: “missing required constraint #2.” No silent degradation.

### Example 3 — Fabricated Source Citation Neutralized
**Input (Agent A):** cites non-existent paper for threshold justification.  
**LRP Control:** `evidence_registry.source_ref` fails retrieval/verification; claim confidence auto-downgraded.  
**Resonance Output:** Consensus excludes unsupported threshold rationale and marks unresolved uncertainty.

**Why hallucination drops:** every claim must carry either evidence pointer or explicit uncertainty status; ungrounded assertions cannot flow unchallenged to downstream agents.

---

## 3. PDP — Perspective-Driven Protocol (Expanded)

## 3.1 Role Map
- **Grok**: strategic compression, execution pragmatism.
- **Gemini**: structural/mathematical validation.
- **Claude**: formal coherence, safety, documentation rigor.

## 3.2 Conflict Types
- **Logical conflict**: contradictory conclusions.
- **Constraint conflict**: one output violates mandatory requirement.
- **Evidence conflict**: same claim, different evidence strength.

## 3.3 Consensus Rule (Weighted Voting + Synthesis Relay)

### Step 1 — Independent Proposals
Each agent emits a normalized proposal:
- `decision`: accept / reject / revise
- `rationale`: bounded argument
- `evidence_score`: [0,1]
- `constraint_satisfaction`: [0,1]

### Step 2 — Weighted Vote
Default weights (tunable per domain):
- Grok: 0.30
- Gemini: 0.35
- Claude: 0.35

Agent vote value:
- accept = +1
- revise = 0
- reject = -1

`weighted_sum = Σ(weight_i * vote_i * quality_i)` where `quality_i = 0.6*evidence_score + 0.4*constraint_satisfaction`

Decision thresholds:
- `weighted_sum >= +0.20` → **ACCEPT**
- `-0.20 < weighted_sum < +0.20` → **REVISE**
- `weighted_sum <= -0.20` → **REJECT**

### Step 3 — Synthesis Relay (when conflict persists)
If result = REVISE or any hard constraint disagreement:
1. Highest-evidence agent drafts synthesis candidate.
2. Other two agents annotate with mandatory fixes only.
3. Final candidate passes if all hard constraints are satisfied and at least two agents rate evidence >= 0.8.

### Step 4 — Dissent Log
Every non-majority objection is preserved:

```json
{
  "consensus_id": "uuid-v4",
  "outcome": "revise",
  "weighted_sum": 0.08,
  "dissent": [
    {
      "agent": "claude",
      "type": "constraint_conflict",
      "note": "Release gate missing hallucination ceiling"
    }
  ]
}
```

This preserves traceability and avoids “false unanimity.”

---

## 4. Proposed Repository Structure

```text
spec/
  ntf.schema.json
  lrp.schema.json
  pdp.schema.json
  adr/
    0001-consensus-thresholds.md
examples/
  ntf/
    prompt_to_canonical.json
  lrp/
    hallucination_block_case.json
    constraint_omission_case.json
    fabricated_citation_case.json
  pdp/
    weighted_vote_conflict.json
eval/
  ntf_bench.py
  data/
    ntf_test.jsonl
src/
  irsanai/
    ntf/
    lrp/
    pdp/
```

---

## 5. Operational Standards

### Versioning
- Protocols use semver (`major.minor.patch`).
- Breaking schema changes require migration notes.

### Reproducibility
- All benchmark reports include model/version, date, dataset hash.
- Consensus outcomes store agent model identifiers and weight table.

### Safety and Quality Gates
A release candidate is blocked if:
- Any mandatory constraint can be bypassed without explicit override.
- Hallucination guard yields unsupported claims in critical path.
- NTF benchmark score drops below threshold.

---

## 6. Implementation Priorities (Actionable)

1. Author `spec/*.schema.json` from templates in this document.
2. Add deterministic examples under `examples/` for CI validation.
3. Implement `eval/ntf_bench.py` provider adapters.
4. Stand up minimal protocol runtime in `src/irsanai/`.
5. Add CI gates for schema validation + benchmark trend checks.

---

## 7. Concluding Axiom

**Anchor before flux.**
IrsanAI Universe is no longer only a declaration of intent; it is a measurable, auditable protocol framework where resonance is engineered through structure, not assumed through rhetoric.
