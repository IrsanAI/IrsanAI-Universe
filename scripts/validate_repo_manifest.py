"""Validate spec/repo_manifest.json structure for sync automation."""

from __future__ import annotations

import json
from pathlib import Path

ALLOWED_STATUSES = {"ACTIVE", "REVIEW", "STALE", "DIVERGED"}
REQUIRED_FIELDS = {
    "name",
    "category",
    "source_url",
    "docs_url",
    "sync_status",
    "last_reviewed",
    "canonical",
}


def main() -> None:
    manifest_path = Path("spec/repo_manifest.json")
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    if "repositories" not in payload or not isinstance(payload["repositories"], list):
        raise SystemExit("Manifest must contain a repositories list")

    for idx, repo in enumerate(payload["repositories"], start=1):
        missing = REQUIRED_FIELDS.difference(repo.keys())
        if missing:
            raise SystemExit(f"Repository #{idx} missing required fields: {sorted(missing)}")

        if repo["sync_status"] not in ALLOWED_STATUSES:
            raise SystemExit(
                f"Repository #{idx} has invalid sync_status: {repo['sync_status']}"
            )

        if not str(repo["source_url"]).startswith("https://github.com/"):
            raise SystemExit(f"Repository #{idx} has invalid source_url")

        if not str(repo["docs_url"]).startswith("https://"):
            raise SystemExit(f"Repository #{idx} has invalid docs_url")

    print("repo_manifest.json validation passed")


if __name__ == "__main__":
    main()
