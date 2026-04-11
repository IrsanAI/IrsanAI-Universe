import json
import subprocess
import datetime

def get_repos():
    cmd = ["gh", "repo", "list", "IrsanAI", "--limit", "100", "--json", "name,description,url,pushedAt,homepageUrl,stargazerCount"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return []
    return json.loads(result.stdout)

def generate_manifest():
    repos = get_repos()
    manifest = {
        "version": "2.0.0",
        "last_updated": datetime.datetime.now().isoformat(),
        "repositories": []
    }
    for repo in repos:
        name = repo['name']
        desc = repo['description'] or ""
        category = "other"
        if "Universe" in name: category = "hub"
        elif any(p in name for p in ["LRP", "PDP", "NTF", "RKP", "RP"]): category = "protocol"
        elif any(t in name.lower() for t in ["tool", "forge", "engine", "scape", "messenger"]): category = "tool"
        elif "Agent" in name or "Void" in name: category = "agent"
        manifest['repositories'].append({
            "name": name,
            "description": desc,
            "url": repo['url'],
            "homepage": repo['homepageUrl'] or f"https://irsanai.github.io/{name}/",
            "last_pushed": repo['pushedAt'],
            "stars": repo['stargazerCount'],
            "category": category
        })
    with open("docs/repo_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    with open("spec/repo_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

if __name__ == "__main__":
    generate_manifest()
