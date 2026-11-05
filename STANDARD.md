# Construction OS Design — Document Standard

Nov 5, 2026 · @Justin

The document model for the `construction-os-design` repository. This doc is the working copy; the repo holds a synced snapshot at `STANDARD.md`. Anything that needs the standard — a Claude Code session, a project doing design-document work — reads it from here or from that snapshot, never from a second copy.

Repo operation rules stay in `CLAUDE.md`: no direct commits to main, synced files are never hand-edited, no history rewrites, no secrets. Those are guardrails against damage and have to be read rather than followed to. This document holds the model, which is the part that grows.

## Component structure

Every component has the same files from the day it is created. A file with nothing settled in it yet exists at `status: draft` and says what is open. Nothing holds two jobs.

| File | Its one job |
| --- | --- |
| `README.md` | Index, plus the short public version: what this is, why it exists, the two or three decisions worth knowing, and what is designed vs. built vs. validated |
| `brief.md` | Who it's for, the painful moment, what it replaces, what's out of scope |
| `spec.md` | The domain, named and bounded. A pointer if the domain lives elsewhere. |
| `design.md` | Architecture, boundaries, and the decision log |
| `plan.md` | Phased work. Work only. |
| `build-log.md` | What happened, in order, and what each finding changed |
| `sync-manifest.yaml` | Source Claude Doc, rev, sync date, per synced file |
| `images/` | Static exports, re-exported when the drawing changes |
| `<slice>-design.md` | Technical design for one vertical slice |

## Rules

- **One decision, one source.** Decisions live in that component's `design.md` log. A plan or build log may reference a decision; neither records one.
- **One document, one job.** If a file matches two rows above, it is two files.
- **Front matter: `type` and `status`** (`draft | current | superseded`) on every `.md`. For a **synced** file those two values live in the manifest beside `source` and `rev`, and the sync writes the front matter into the file — a block added by hand is wiped the next time that file syncs. For a **repo-authored** file, the READMEs included, the front matter is written in the file itself.
- Filenames are lowercase-kebab `.md`. No version numbers in filenames.
- Restructuring happens in the Claude Docs first. The repo follows via sync; synced files are never hand-edited.
- A new component is this file set, not a decision about which files to make.

## Project structure

A project is a folder under the repo root holding one product's documents. Its own level carries `README.md`, `brief.md`, and a `sync-manifest.yaml`; components sit beneath it as folders. A new project gets a folder, a README, and a row in the root README's index table.

## Maintaining this document

**Changes are made here.** `STANDARD.md` in the repo is a snapshot and is never edited, the same rule as every other synced file.

**Re-sync at the moment it matters, not on a schedule.** The standard is only load-bearing when a component is created or restructured, so the sync happens immediately before that work. If nothing has changed, the sync is a no-op. If something has, the repo was stale and now isn't. Nothing detects drift automatically — the manifest records the rev it was synced at, and comparing that to this doc's current rev is a manual check — so tying the sync to the moment of use is what keeps it honest.

**Every change gets a dated line in the history below.** One line, what changed and why. This is what makes a convention trustworthy to someone reading it six months later, including a Claude Code session that has never seen the conversation it came from.

**A component that doesn't fit is evidence about the standard, not an exception to it.** Either the shape is wrong and this document changes, or the component is wrong and it changes. No component is exempted. Exemptions are how a convention stops being one.

## Change history

| Date | Change |
| --- | --- |
| 2026-11-05 | Created. Fixed component file set replacing per-component judgment, after `build-log.md` and `build-guide.md` diverged between the two existing components. Decision logs consolidated to `design.md` after `document-workbench` was found keeping three. |
