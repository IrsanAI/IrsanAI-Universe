import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
payload = json.loads((root / "docs" / "repo_manifest.json").read_text(encoding="utf-8"))
missing = [repo["name"] for repo in payload["repositories"] if not repo.get("avatar")]
print("\n".join(missing))
print(f"missing_count={len(missing)}")
