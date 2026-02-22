# Repository Sync & GitHub Pages Blueprint

This document defines how `IrsanAI-Universe` stays synchronized with the broader IrsanAI repository ecosystem and how each repository can ship its own GitHub Pages site.

## 1) Single Source of Truth Model

- `IrsanAI-Universe` is the **navigation and governance hub**.
- Protocol-specific repositories (e.g., `NTF-v1.0`, `IrsanAI-LRP-v1.3`) remain implementation homes.
- Universe should avoid duplicating implementation code and instead reference upstream repositories and pinned snapshots.

## 2) Recommended Sync Strategy

### Preferred: Git Submodules

Use submodules under `external/` for repositories that must remain independently versioned.

```bash
git submodule add https://github.com/IrsanAI/NTF-v1.0 external/NTF-v1.0
git submodule add https://github.com/IrsanAI/IrsanAI-LRP-v1.3 external/IrsanAI-LRP-v1.3
git submodule add https://github.com/IrsanAI/IrsanAI-PDP-v2.0 external/IrsanAI-PDP-v2.0
```

Benefits:
- Clear provenance and commit pinning.
- No content drift between Universe docs and source repositories.
- Easy audit trail for protocol updates.

### Alternative: Scheduled Pull Sync

If submodules are not desired, schedule a GitHub Action in Universe that:
1. Checks latest commits in target repositories.
2. Regenerates a manifest file.
3. Opens an automated PR when drift is detected.

## 3) Repository Manifest

Maintain a machine-readable registry in Universe (recommended file: `spec/repo_manifest.json`) containing:
- repository name
- canonical GitHub URL
- docs URL (GitHub Pages)
- protocol category
- last reviewed date

This enables automated checks and dashboard rendering.

## 4) GitHub Pages Rollout (All Repositories)

For each repository:
1. Enable Pages from `main` (or `gh-pages`) in repository settings.
2. Add a minimal landing page (`index.md` or `index.html`) with:
   - project purpose
   - quick links to spec/docs
   - changelog/version pointer
3. Use consistent URL pattern:
   - `https://irsanai.github.io/<repo-name>/`

## 5) Universe as the Command Center

Universe should include a "Project Pages" table in `README.md` with links to:
- source repository
- live docs page
- sync status

Suggested sync states:
- `ACTIVE` — synced in last 7 days
- `STALE` — no review in >7 days
- `DIVERGED` — known spec/code mismatch

## 6) Immediate Execution Checklist

- [ ] Add submodule or manifest-based sync for all active protocol repositories.
- [ ] Add `.github/workflows/repo-sync.yml` in Universe.
- [ ] Add Pages landing pages in each protocol repository.
- [ ] Update Universe README Project Pages table with live links.
- [ ] Review duplicate repositories and define canonical names.

## 7) Naming Consolidation Recommendation

Current naming suggests overlap (e.g., `LRP-v1.3` and `IrsanAI-LRP-v1.3`).

Recommendation:
- Keep one canonical protocol repository per protocol/version.
- Archive or redirect duplicates via README notice.
- Reference canonical repository only in Universe navigation.
