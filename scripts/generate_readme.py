#!/usr/bin/env python3
"""Generate the bilingual root README from docs/repo_manifest.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs" / "repo_manifest.json"
README_PATH = ROOT / "README.md"

CATEGORY = {
    "de": {"hub": "Hub", "protocol": "Protokoll", "agent": "Agent", "tool": "Tool", "system": "System", "other": "Sonstiges"},
    "en": {"hub": "Hub", "protocol": "Protocol", "agent": "Agent", "tool": "Tool", "system": "System", "other": "Other"},
}
STATUS = {
    "de": {"ACTIVE": "AKTIV", "REVIEW": "REVIEW", "STALE": "RUHIG", "DIVERGED": "ABWEICHEND"},
    "en": {"ACTIVE": "ACTIVE", "REVIEW": "REVIEW", "STALE": "QUIET", "DIVERGED": "DIVERGED"},
}


def cell(value: object) -> str:
    return str(value or "—").replace("|", "\\|").replace("\n", " ").strip()


def table_rows(repositories: list[dict], lang: str) -> str:
    rows: list[str] = []
    for repo in repositories:
        avatar = repo.get("avatar")
        picture = f'<img src="docs/{avatar}" alt="{cell(repo["name"])} passfoto" width="52" height="52">' if avatar and avatar.startswith("assets/") else "—"
        name = cell(repo["name"])
        code = f"[Repository]({cell(repo['source_url'])})"
        page = f"[Page]({cell(repo['pages_url'])})" if repo.get("pages_detected") and repo.get("pages_url") else "—"
        description = repo.get(f"description_{lang}") or repo.get("description") or "—"
        role = repo.get("role") or "—"
        category = CATEGORY[lang].get(repo.get("category", "other"), CATEGORY[lang]["other"])
        status = STATUS[lang].get(repo.get("sync_status", "REVIEW"), repo.get("sync_status", "REVIEW"))
        rows.append(f"| {picture} | {code} | {cell(category)} | {cell(repo.get('layer'))} | {cell(role)} | {cell(description)} | {cell(status)} | {cell(repo.get('last_pushed'))} | {page} |")
    return "\n".join(rows)


def build() -> str:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    repos = manifest.get("repositories", [])
    pages = sum(1 for repo in repos if repo.get("pages_detected"))
    stars = sum(int(repo.get("stars") or 0) for repo in repos)
    synced = manifest.get("last_updated", "—")
    de_rows = table_rows(repos, "de")
    en_rows = table_rows(repos, "en")
    return f'''# IrsanAI Universe — Resonance Engine

[**Deutsch**](#deutsch) · [**English**](#english) · [**Live Dashboard**](https://irsanai.github.io/IrsanAI-Universe/)

> **IrsanAI Universe** is the public map of an evolving human–AI resonance stack: protocols anchor meaning, agents move intent, systems route capability, and tools turn ideas into repeatable action.

[Open the Resonance Engine](https://irsanai.github.io/IrsanAI-Universe/) · [Browse every repository on GitHub](https://github.com/IrsanAI)

| Live snapshot | Value |
|---|---:|
| Repository nodes | {len(repos)} |
| Connected GitHub Pages | {pages} |
| Community stars | {stars} |
| Manifest generated | `{synced}` |

---

<a name="deutsch"></a>

## Deutsch

Das Universe ist das **Aushängeschild und die lesbare Control Plane** des IrsanAI-Stacks. Die Landingpage verbindet aktuelle GitHub-Metadaten mit einer bewusst gekennzeichneten Heuristik: Der **Resonance Index** bewertet Aktualität, semantische Abdeckung und erkannte Pages-Verbindungen. Er ist ein Orientierungssignal, keine Aussage über Laufzeitgesundheit, Sicherheit oder wissenschaftliche Validierung.

Der Stack lässt sich als sechs Bewegungen lesen: **NTF verankert Bedeutung**, **LRP formt Antworten**, **PDP wechselt die Perspektive**, **ARIA bewegt Intent zwischen Agenten**, **VERA prüft Evidenz**, und **IS routet Capabilities**. Die übrigen Repositorys bilden die Infrastruktur, Werkzeuge, Simulationen und experimentellen Räume, in denen diese Grammatik praktisch wird.

### Vollständige Repository-Konstellation

Die folgende Tabelle wird durch den Manifest-Sync aktualisiert und listet **jedes öffentliche Repository der Organisation** auf. Das Passfoto ist die visuelle Kurzsignatur des jeweiligen Knotens.

| Passfoto | Repository | Kategorie | Schicht | Architekturrolle | Kurzbeschreibung | Sync | Letzter Push | Page |
|---|---|---|---|---|---|---|---|---|
{de_rows}

### Lesen und Mitwirken

Beginne auf dem [Live Dashboard](https://irsanai.github.io/IrsanAI-Universe/), wechsle zwischen Karten- und Konstellationsansicht und starte den lokalen Signal-Scan. Für technische Details, Spezifikationen und die Automatisierung ist dieses [Universe-Repository](https://github.com/IrsanAI/IrsanAI-Universe) die maßgebliche Quelle.

---

<a name="english"></a>

## English

The Universe is the **flagship and readable control plane** of the IrsanAI stack. Its landing page combines current GitHub metadata with an explicitly labelled heuristic: the **Resonance Index** scores freshness, semantic coverage, and detected Pages connections. It is a navigation signal, not a claim about runtime health, security, or scientific validation.

The stack can be read as six movements: **NTF anchors meaning**, **LRP shapes responses**, **PDP changes the lens**, **ARIA moves intent between agents**, **VERA challenges evidence**, and **IS routes capability**. The remaining repositories provide infrastructure, tools, simulations, and experimental spaces where this grammar becomes practical.

### Complete repository constellation

The table below is regenerated by the manifest sync and lists **every public repository in the organization**. Each passfoto is a compact visual signature for its node.

| Passfoto | Repository | Category | Layer | Architecture role | Short description | Sync | Last push | Page |
|---|---|---|---|---|---|---|---|---|
{en_rows}

### Read and contribute

Start with the [Live Dashboard](https://irsanai.github.io/IrsanAI-Universe/), switch between card and constellation views, and run the local signal scan. For technical details, specifications, and automation, the [Universe repository](https://github.com/IrsanAI/IrsanAI-Universe) is the canonical source.

---

*Generated from `docs/repo_manifest.json` · manifest v{manifest.get('version', '—')} · IrsanAI Universe*
'''


if __name__ == "__main__":
    README_PATH.write_text(build(), encoding="utf-8")
    print(f"Generated bilingual README for {len(json.loads(MANIFEST_PATH.read_text())['repositories'])} repositories")
