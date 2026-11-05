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
- Every `.md` carries front matter: `type` and `status` (`draft | current | superseded`). Sync state lives in the manifest, not here.
- Filenames are lowercase-kebab `.md`. No version numbers in filenames.
- Restructuring happens in the Claude Docs first. The repo follows via sync; synced files are never hand-edited.
- A new component is this file set, not a decision about which files to make.

## Project structure

A project is a folder under the repo root holding one product's documents. Its own level carries `README.md`, `brief.md`, and a `sync-manifest.yaml`; components sit beneath it as folders. A new project gets a folder, a README, and a row in the root README's index table.
