#!/usr/bin/env python3
"""Rebuild DOCS.md, the synced document index, from every sync-manifest.yaml.

Run from the repo root after any sync, or after adding or removing a synced doc:
    python tools/build_docs.py

Order: the root manifest first, then each project (alphabetical) with its
project-level docs before its components (alphabetical). Within a manifest,
entries keep the order they're listed in. tools/validate.py fails a pull request
whose DOCS.md doesn't match what this script would write.
"""
import os

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", ".github", "tools", "_template"}

HEADER = """# Synced document index

Every document synced from a Claude Doc: its source, where it syncs to, and the revision last synced. Generated from the sync manifests by `python tools/build_docs.py`. Do not edit by hand.

Repo-authored docs (written here directly, such as the agents docs) aren't listed; find them through each project's README.

| Document | Claude Doc | Syncs to | Rev | Synced |
| --- | --- | --- | --- | --- |
"""


def manifest_entries(folder):
    path = os.path.join(folder, "sync-manifest.yaml")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("docs") or []


def subfolders(folder):
    return sorted(d for d in os.listdir(folder)
                  if d not in SKIP_DIRS and not d.startswith(".")
                  and os.path.isdir(os.path.join(folder, d)))


def manifest_folders():
    """Root, then each project, then its components."""
    yield ROOT
    for project in subfolders(ROOT):
        pdir = os.path.join(ROOT, project)
        yield pdir
        for component in subfolders(pdir):
            yield os.path.join(pdir, component)


def build():
    rows = []
    for folder in manifest_folders():
        for e in manifest_entries(folder):
            path = os.path.relpath(os.path.join(folder, e["file"]), ROOT)
            rows.append(f"| {e['title']} | [source]({e['source']}) | {path} | {e['rev']} | {e['synced']} |")
    return HEADER + "\n".join(rows) + "\n"


if __name__ == "__main__":
    with open(os.path.join(ROOT, "DOCS.md"), "w", encoding="utf-8") as f:
        f.write(build())
    print("DOCS.md rebuilt from the sync manifests.")
