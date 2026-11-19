#!/usr/bin/env python3
"""Structural checks for the design repository, against STANDARD.md.

Run from the repo root:  python tools/validate.py
Exit code 1 if any ERROR is found; WARNINGs are reported but don't fail.

What it checks
  - every project folder has the required project-level files
  - every component folder has the full component file set
  - repo-authored .md files carry front matter with a valid type and status
  - synced files are listed in their folder's sync-manifest.yaml, and the revision
    in their sync header matches the manifest
  - every manifest entry points to a file that exists
  - DOCS.md lists exactly the manifest entries, with the same revision and date
  - relative links between files resolve
  - the root README links every project

What it can't check: whether a Claude Doc has moved ahead of its synced snapshot.
That needs Claude Docs access, so it belongs to the sync and roll-up steps, not CI.
"""
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", ".github", "tools", "_template"}
STATUSES = {"draft", "current", "superseded"}
PROJECT_REQUIRED = ["README.md", "brief.md", "sync-manifest.yaml"]
COMPONENT_REQUIRED = ["README.md", "brief.md", "spec.md", "design.md", "plan.md",
                      "build-log.md", "sync-manifest.yaml", "images"]
PROJECT_OPTIONAL = {"principles.md", "architecture.md", "product-spec.md"}
COMPONENT_OPTIONAL_RE = re.compile(r"^[a-z0-9-]+-design\.md$")
SYNC_HEADER = re.compile(r"^> \*\*Synced from Claude Docs")
SYNC_REV = re.compile(r"doc revision (\d+) · synced (\d{4}-\d{2}-\d{2})")
LINK = re.compile(r"\]\(([^)\s]+)\)")

errors, warnings = [], []


def err(path, msg):
    errors.append(f"ERROR   {path}: {msg}")


def warn(path, msg):
    warnings.append(f"WARNING {path}: {msg}")


def rel(p):
    return os.path.relpath(p, ROOT)


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def front_matter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    try:
        return yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError:
        return None


def load_manifest(folder):
    p = os.path.join(folder, "sync-manifest.yaml")
    if not os.path.exists(p):
        return None
    try:
        data = yaml.safe_load(read(p)) or {}
    except yaml.YAMLError as e:
        err(rel(p), f"not valid YAML ({e})")
        return {}
    entries = data.get("docs") or []
    out = {}
    for e in entries:
        f = e.get("file")
        if not f:
            err(rel(p), "an entry has no 'file'")
            continue
        for key in ("title", "source", "rev", "synced", "type", "status"):
            if key not in e:
                err(rel(p), f"entry for {f} has no '{key}'")
        if e.get("status") not in STATUSES:
            err(rel(p), f"entry for {f} has status {e.get('status')!r}; use draft, current or superseded")
        if not os.path.exists(os.path.join(folder, f)):
            err(rel(p), f"lists {f}, which doesn't exist")
        out[f] = e
    return out


def check_markdown(folder, manifest):
    for name in sorted(os.listdir(folder)):
        p = os.path.join(folder, name)
        if not name.endswith(".md") or not os.path.isfile(p):
            continue
        text = read(p)
        if SYNC_HEADER.match(text):
            entry = (manifest or {}).get(name)
            if entry is None:
                err(rel(p), "has a sync header but isn't in sync-manifest.yaml")
                continue
            m = SYNC_REV.search(text.split("\n\n", 1)[0])
            if not m:
                err(rel(p), "sync header has no 'doc revision N · synced YYYY-MM-DD'")
            elif int(m.group(1)) != int(entry.get("rev", -1)) or m.group(2) != str(entry.get("synced")):
                err(rel(p), f"sync header says rev {m.group(1)} / {m.group(2)}, "
                            f"manifest says rev {entry.get('rev')} / {entry.get('synced')}")
        else:
            if manifest and name in manifest:
                err(rel(p), "is in sync-manifest.yaml but has no sync header")
            fm = front_matter(text)
            if fm is None:
                err(rel(p), "repo-authored file without front matter (type, status)")
            else:
                if not fm.get("type"):
                    err(rel(p), "front matter has no type")
                if fm.get("status") not in STATUSES:
                    err(rel(p), f"front matter status {fm.get('status')!r}; use draft, current or superseded")


def check_links(path):
    text = read(path)
    text = re.sub(r"```.*?```", "", text, flags=re.S)  # ignore code blocks
    for target in LINK.findall(text):
        if re.match(r"^(https?:|mailto:|#)", target):
            continue
        target = target.split("#", 1)[0]
        if not target:
            continue
        dest = os.path.normpath(os.path.join(os.path.dirname(path), target))
        if not os.path.exists(dest):
            err(rel(path), f"link to {target} doesn't resolve")


def is_component(path):
    return os.path.isdir(path) and os.path.basename(path) != "images"


def main():
    projects = sorted(d for d in os.listdir(ROOT)
                      if os.path.isdir(os.path.join(ROOT, d)) and d not in SKIP_DIRS and not d.startswith("."))
    all_manifests = []

    for proj in projects:
        pdir = os.path.join(ROOT, proj)
        for req in PROJECT_REQUIRED:
            if not os.path.exists(os.path.join(pdir, req)):
                err(proj, f"project is missing {req}")
        manifest = load_manifest(pdir)
        all_manifests.append((pdir, manifest or {}))
        check_markdown(pdir, manifest)
        for name in sorted(os.listdir(pdir)):
            p = os.path.join(pdir, name)
            if os.path.isfile(p) and name.endswith(".md") and name not in PROJECT_REQUIRED and name not in PROJECT_OPTIONAL:
                warn(rel(p), "not a named project-level type in STANDARD.md")
        for name in sorted(os.listdir(pdir)):
            cdir = os.path.join(pdir, name)
            if not is_component(cdir):
                continue
            for req in COMPONENT_REQUIRED:
                if not os.path.exists(os.path.join(cdir, req)):
                    err(rel(cdir), f"component is missing {req}")
            cmanifest = load_manifest(cdir)
            all_manifests.append((cdir, cmanifest or {}))
            check_markdown(cdir, cmanifest)
            for f in sorted(os.listdir(cdir)):
                if f.endswith(".md") and f not in COMPONENT_REQUIRED and not COMPONENT_OPTIONAL_RE.match(f):
                    warn(rel(os.path.join(cdir, f)), "not in the component file set (README, brief, spec, design, plan, build-log, <slice>-design)")

    # root-level synced files (STANDARD.md)
    root_manifest = load_manifest(ROOT) or {}
    all_manifests.append((ROOT, root_manifest))
    for f, e in root_manifest.items():
        text = read(os.path.join(ROOT, f)) if os.path.exists(os.path.join(ROOT, f)) else ""
        m = SYNC_REV.search(text.split("\n\n", 1)[0]) if text else None
        if text and (not SYNC_HEADER.match(text) or not m or int(m.group(1)) != int(e["rev"])):
            err(f, f"sync header doesn't match manifest rev {e['rev']}")

    # DOCS.md matches the manifests
    expected = {}
    for folder, man in all_manifests:
        for f, e in man.items():
            expected[rel(os.path.join(folder, f))] = (str(e.get("rev")), str(e.get("synced")))
    rows = {}
    for line in read(os.path.join(ROOT, "DOCS.md")).splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 5 and cells[2] not in ("Syncs to", "---"):
            rows[cells[2]] = (cells[3], cells[4])
    for path, val in expected.items():
        if path not in rows:
            err("DOCS.md", f"missing a row for {path}")
        elif rows[path] != val:
            err("DOCS.md", f"{path} shows rev {rows[path][0]} / {rows[path][1]}, manifest says {val[0]} / {val[1]}")
    for path in rows:
        if path not in expected:
            err("DOCS.md", f"lists {path}, which no manifest has")

    # root README links every project
    readme = read(os.path.join(ROOT, "README.md"))
    for proj in projects:
        if f"]({proj}/)" not in readme:
            err("README.md", f"doesn't link the {proj}/ project")

    # links everywhere except the templates, whose links are written for where copies end up
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {".git", "_template"}]
        for f in filenames:
            if f.endswith(".md"):
                check_links(os.path.join(dirpath, f))

    for line in errors + warnings:
        print(line)
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s) across {len(projects)} project(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
