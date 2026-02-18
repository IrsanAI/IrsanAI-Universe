"""NTF benchmark harness (concept implementation).

This script evaluates semantic fidelity between gold and predicted intent strings.
It supports cosine similarity over embeddings and an LLM-judge placeholder mode.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass
class Record:
    raw_prompt: str
    gold_intent: str
    system_intent: str


def cosine(a: List[float], b: List[float]) -> float:
    num = sum(x * y for x, y in zip(a, b))
    den_a = sum(x * x for x in a) ** 0.5
    den_b = sum(y * y for y in b) ** 0.5
    return num / (den_a * den_b + 1e-12)


def embed(text: str) -> List[float]:
    """Placeholder embedder.

    Replace with provider call (OpenAI, local sentence transformer, etc.).
    """
    raise NotImplementedError("Implement embedding provider in embed()")


def judge(gold: str, pred: str) -> float:
    """Placeholder LLM-as-a-Judge function.

    Should return a bounded score in [0,1] using structured rubric output.
    """
    raise NotImplementedError("Implement judge provider in judge()")


def run(records: Iterable[Record], mode: str) -> Dict[str, float]:
    scores: List[float] = []
    for record in records:
        if mode == "cosine":
            score = cosine(embed(record.gold_intent), embed(record.system_intent))
        elif mode == "judge":
            score = judge(record.gold_intent, record.system_intent)
        else:
            raise ValueError(f"Unsupported mode: {mode}")
        scores.append(score)

    mean_score = sum(scores) / max(len(scores), 1)
    return {
        "count": float(len(scores)),
        "mean_score": mean_score,
        "pass_0_98": 1.0 if mean_score >= 0.98 else 0.0,
    }


def load_dataset(path: str) -> List[Record]:
    rows: List[Record] = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            data = json.loads(line)
            rows.append(Record(**data))
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate NTF semantic fidelity")
    parser.add_argument("--dataset", required=True, help="Path to JSONL benchmark dataset")
    parser.add_argument(
        "--mode",
        choices=["cosine", "judge"],
        default="cosine",
        help="Evaluation mode",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records = load_dataset(args.dataset)
    report = run(records, args.mode)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
