#!/usr/bin/env python3
"""Build the machine-readable data layer for the IrsanAI Universe landing page.

The script intentionally keeps repository facts coming from GitHub and stores only
presentation metadata locally. New repositories appear automatically with safe
fallbacks; known projects receive richer architecture and metacognitive framing.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

OWNER = "IrsanAI"
ROOT = Path(__file__).resolve().parents[1]

# Presentation metadata is deliberately separate from live GitHub facts. This lets
# the dashboard explain the stack without pretending that a heuristic is runtime
# telemetry or a formal architectural certification.
PROJECT_META: dict[str, dict[str, Any]] = {
    "IrsanAI-Universe": {
        "category": "hub", "layer": "orchestration", "role": "The central map of the stack",
        "de": "Zentraler Orchestrierungs-Hub für Protokolle, Agenten und Werkzeuge.",
        "en": "Central orchestration hub for protocols, agents, and tools.",
    },
    "root-ascent-method": {
        "category": "tool", "layer": "reasoning", "role": "Incident-to-root-cause ladder",
        "de": "Disziplinierte Ursachenanalyse vom konkreten Vorfall zum systemischen Hebel.",
        "en": "Disciplined causal analysis from concrete incidents to systemic levers.",
    },
    "irsanai-360": {
        "category": "system", "layer": "cognition", "role": "Intent-centred cognitive system",
        "de": "Intent-zentriertes kognitives System als 360-Grad-Blick auf Aufgaben und Kontext.",
        "en": "Intent-centred cognitive system for a 360-degree view of tasks and context.",
    },
    "NEXUS-Recover": {
        "category": "tool", "layer": "recovery", "role": "Recovery and continuity node",
        "de": "Recovery-Knoten für Wiederherstellung, Kontinuität und robuste Übergaben.",
        "en": "Recovery node for restoration, continuity, and resilient handoffs.",
    },
    "IrsanAI-LiveShare": {
        "category": "tool", "layer": "experience", "role": "Session-first live sharing",
        "de": "Session-first-Live-Sharing mit Tracking, sicheren Tokens und Viewer-Projektion.",
        "en": "Session-first live sharing with tracking, secure tokens, and viewer projections.",
    },
    "IrsanAI-MetaFabric": {
        "category": "hub", "layer": "control-plane", "role": "Capability and reflection control plane",
        "de": "Metakognitive Control Plane für Capabilities, Provider, Feedback und Reflexion.",
        "en": "Metacognitive control plane for capabilities, providers, feedback, and reflection.",
    },
    "IrsanAI-IS": {
        "category": "system", "layer": "routing", "role": "Capability inventory and loadout router",
        "de": "Inventory-System, das Modelle, Essenzen und Loadouts auf konkrete Aufgaben routet.",
        "en": "Inventory system routing models, essences, and loadouts to concrete tasks.",
    },
    "LRP-v1.3": {
        "category": "protocol", "layer": "response", "role": "Structured LLM response contract",
        "de": "Strukturiert Intent, Aufgabe, Constraints und Ausgabe für belastbare LLM-Kommunikation.",
        "en": "Structures intent, task, constraints, and output for reliable LLM communication.",
    },
    "IrsanAI-ARIA-Protocol": {
        "category": "protocol", "layer": "agent-network", "role": "Agent reasoning and intent architecture",
        "de": "Offener Standard für typisierte Agent-to-Agent-Kommunikation.",
        "en": "Open standard for typed agent-to-agent communication.",
    },
    "IrsanAI-dis-core": {
        "category": "system", "layer": "security", "role": "Device intelligence and anti-surveillance",
        "de": "Autonomer Security-Stack für gerätenahe Intelligenz und Anti-Surveillance.",
        "en": "Autonomous security stack for device intelligence and anti-surveillance.",
    },
    "IrsanAI-VERA": {
        "category": "agent", "layer": "epistemics", "role": "Evidence, adversarial challenge, and belief update",
        "de": "Epistemische Engine für Evidenzketten, Red-Team-Prüfung und Bayes-Updates.",
        "en": "Epistemic engine for evidence chains, red-team challenge, and Bayesian updates.",
    },
    "IrsanAI-Nexus-Server": {
        "category": "hub", "layer": "infrastructure", "role": "Encrypted cross-LLM intelligence network",
        "de": "Verschlüsselter Nexus für den Austausch zwischen unterschiedlichen LLM-Instanzen.",
        "en": "Encrypted nexus for exchange between different LLM instances.",
    },
    "irsanai-hfar-engine": {
        "category": "tool", "layer": "ingestion", "role": "Header-first anchor reader",
        "de": "Token-sparende Lese-Engine, die zuerst Struktur und Anker extrahiert.",
        "en": "Token-efficient reading engine that extracts structure and anchors first.",
    },
    "irsanai-mom4ai-forge": {
        "category": "tool", "layer": "evolution", "role": "Evolutive neural skeleton forge",
        "de": "Forge für evolutive neuronale Skelette und gerichtete Entwicklungsgraphen.",
        "en": "Forge for evolutive neural skeletons and directed development graphs.",
    },
    "IrsanAI-MindScape-3D": {
        "category": "tool", "layer": "visualization", "role": "Spatial cognitive architecture",
        "de": "Interaktive 3D-Visualisierung von Systemarchitektur, Entropie und kognitiven Mustern.",
        "en": "Interactive 3D visualization of system architecture, entropy, and cognitive patterns.",
    },
    "NTF-v1.0": {
        "category": "protocol", "layer": "semantic-anchor", "role": "NeuroToken semantic anchoring",
        "de": "Semantische Anker und Drift-Kontrolle für stabile Begriffe über lange Prozesse.",
        "en": "Semantic anchors and drift control for stable concepts across long processes.",
    },
    "mycelial-echo-forge": {
        "category": "agent", "layer": "emergence", "role": "Biologically inspired agentic architecture",
        "de": "Biologisch inspirierte, dezentrale Architektur für emergentes Agentenverhalten.",
        "en": "Biologically inspired decentralized architecture for emergent agent behaviour.",
    },
    "irsanai-nexus": {
        "category": "tool", "layer": "repository-intelligence", "role": "Repository analysis and insight console",
        "de": "Repository-Intelligence-Plattform mit Analyse-API, Reports und Insight Console.",
        "en": "Repository intelligence platform with analysis API, reports, and insight console.",
    },
    "IrsanAI-Void": {
        "category": "agent", "layer": "simulation", "role": "Psychological survival simulation",
        "de": "Terminal-Survivalspiel, das Mustererkennung, Paranoia und Kooperation erfahrbar macht.",
        "en": "Terminal survival game making pattern recognition, paranoia, and cooperation tangible.",
    },
    "TPM-Agent": {
        "category": "agent", "layer": "prediction", "role": "High-entropy signal extraction",
        "de": "Agent für das Herauslösen der kleinsten wesentlichen Information aus chaotischen Daten.",
        "en": "Agent for extracting the smallest essential signal from chaotic data.",
    },
    "IrsanAI-Forge": {
        "category": "tool", "layer": "activation", "role": "Intent-to-agent activation forge",
        "de": "Aktive Schmiede für Intent-Binding, LRP-Prompts und Agenten-Handoffs.",
        "en": "Active forge for intent binding, LRP prompts, and agent handoffs.",
    },
    "IrsanAI-PDP-v2.0": {
        "category": "protocol", "layer": "perspective", "role": "Perspective-driven logic factory",
        "de": "Perspektiven-Linsen für Manager-, Dev-, Creative- und Analysten-Sicht.",
        "en": "Perspective lenses for manager, developer, creative, and analyst views.",
    },
    "IrsanAI-NLM-Neural-Link-Messenger": {
        "category": "tool", "layer": "agent-network", "role": "Decentralized agent-to-agent messenger",
        "de": "Dezentraler Messenger mit DID-Registry, LRP-Integration und strukturierten Nachrichten.",
        "en": "Decentralized messenger with DID registry, LRP integration, and structured messages.",
    },
    "IrsanAI-RP-v1.0": {
        "category": "protocol", "layer": "handshake", "role": "Three-way resonance handshake",
        "de": "3-Way-Handshake für unmittelbare kognitive Kopplung zwischen Mensch und LLM.",
        "en": "Three-way handshake for immediate cognitive coupling between human and LLM.",
    },
    "RKP-v2.0-": {
        "category": "protocol", "layer": "prediction", "role": "Resonant kinetic prediction",
        "de": "Experimenteller Protokollknoten für resonante Bewegungs- und Verlaufsvorhersage.",
        "en": "Experimental protocol node for resonant kinetic and trajectory prediction.",
    },
    "IrsanAI-Sata_Erase_Tool": {
        "category": "tool", "layer": "sanitization", "role": "Auditable data sanitization",
        "de": "Auditierbare Datenbereinigung mit Live-I/O-Visualisierung und Compliance-Report.",
        "en": "Auditable data sanitization with live I/O visualization and compliance reporting.",
    },
}


def run_json(args: list[str]) -> Any:
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "GitHub CLI request failed")
    # Some hosted shells force ANSI colours even for captured output.
    clean_stdout = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", result.stdout or "")
    return json.loads(clean_stdout or "[]")


def detect_pages(repo_name: str) -> tuple[str | None, bool]:
    """Return an explicitly configured Pages URL when GitHub exposes one."""
    result = subprocess.run(
        ["gh", "api", f"repos/{OWNER}/{repo_name}/pages", "--jq", ".html_url"],
        capture_output=True,
        text=True,
        check=False,
    )
    page = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", result.stdout or "").strip()
    if not page.startswith("https://"):
        return (None, False)
    return (page, True)


def classify_status(pushed_at: str | None) -> str:
    if not pushed_at:
        return "REVIEW"
    try:
        timestamp = dt.datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
        age_days = (dt.datetime.now(dt.timezone.utc) - timestamp).days
    except ValueError:
        return "REVIEW"
    if age_days <= 30:
        return "ACTIVE"
    if age_days <= 120:
        return "REVIEW"
    return "STALE"


def fallback_page(name: str) -> str:
    return f"https://{OWNER.lower()}.github.io/{name}/"


def build_manifest() -> dict[str, Any]:
    fields = [
        "name", "description", "url", "pushedAt", "homepageUrl",
        "stargazerCount", "primaryLanguage", "isFork", "visibility",
    ]
    repos = run_json(["gh", "repo", "list", OWNER, "--limit", "100", "--json", ",".join(fields)])
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    output: list[dict[str, Any]] = []

    for raw in repos:
        name = raw["name"]
        meta = PROJECT_META.get(name, {})
        detected_page, has_page = detect_pages(name)
        configured_homepage = (raw.get("homepageUrl") or "").strip() or None
        docs_url = detected_page or configured_homepage or fallback_page(name)
        description = (raw.get("description") or "").strip()
        output.append({
            "name": name,
            "description": description,
            "description_de": meta.get("de") or description or "Noch keine Beschreibung hinterlegt.",
            "description_en": meta.get("en") or description or "No description has been published yet.",
            "url": raw.get("url") or f"https://github.com/{OWNER}/{name}",
            "source_url": raw.get("url") or f"https://github.com/{OWNER}/{name}",
            "homepage": docs_url,
            "docs_url": docs_url,
            "pages_url": detected_page,
            "pages_detected": has_page,
            "last_pushed": raw.get("pushedAt"),
            "last_reviewed": now[:10],
            "stars": raw.get("stargazerCount") or 0,
            "language": (raw.get("primaryLanguage") or {}).get("name") if isinstance(raw.get("primaryLanguage"), dict) else None,
            "visibility": raw.get("visibility", "PUBLIC"),
            "is_fork": bool(raw.get("isFork", False)),
            "category": meta.get("category", "other"),
            "layer": meta.get("layer", "unmapped"),
            "role": meta.get("role", "Repository in the IrsanAI stack"),
            "avatar": f"assets/img/passfotos/{name}.png" if (ROOT / "docs" / "assets" / "img" / "passfotos" / f"{name}.png").exists() else None,
            "sync_status": classify_status(raw.get("pushedAt")),
            "canonical": name in PROJECT_META,
        })

    output.sort(key=lambda item: item.get("last_pushed") or "", reverse=True)
    return {"version": "3.0.0", "last_updated": now, "owner": OWNER, "repositories": output}


def main() -> None:
    manifest = build_manifest()
    for relative in ("docs/repo_manifest.json", "spec/repo_manifest.json"):
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated manifest for {len(manifest['repositories'])} repositories at {manifest['last_updated']}")


if __name__ == "__main__":
    main()

# The workflow supplies GH_TOKEN/GITHUB_TOKEN to gh. No token is stored in this file.
_ = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
