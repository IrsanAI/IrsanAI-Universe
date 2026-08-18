import json
from pathlib import Path

payload = json.loads(Path("docs/repo_manifest.json").read_text(encoding="utf-8"))
repositories = payload["repositories"]
print(f"repositories={len(repositories)}")
print(f"version={payload['version']}")
print(f"latest={repositories[0]['name'] if repositories else 'none'}")
print(f"pages_detected={sum(1 for repo in repositories if repo['pages_detected'])}")
print(f"canonical={sum(1 for repo in repositories if repo['canonical'])}")
print(f"categories={sorted({repo['category'] for repo in repositories})}")
