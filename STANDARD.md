> **Synced from Claude Docs. Edit there, not here.**
> Source: [Document Standard](https://claude.ai/artifact/XH2r6ocKxZXUpUdyndiDWN) · doc revision 6 · synced 2026-11-05

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

A project is a folder under the repo root holding one product's documents, with its components as subfolders beneath it.

**Required at the project level:** `README.md`, `brief.md`, `sync-manifest.yaml`.

**Optional, by named type:**

| File | Its one job |
| --- | --- |
| `principles.md` | Craft knowledge — what building this taught, each principle anchored to the incident that taught it and to where it is enforced |
| `architecture.md` | How the components fit together and how a request moves through them |

The project level is deliberately not a fixed file set the way a component is, and the difference is structural rather than a matter of judgment. Components repeat: each does the same job, so fixing the set removes decisions that would otherwise get made differently each time. Projects do not repeat — as one with two components needs an architecture document and one with a single component does not. New optional types are added to the table above as they appear, so a document has a name and a stated job rather than arriving ad hoc.

A new project gets a folder, a README, a brief, and a row in the root README's index table.

## Maintaining this document

**Changes are made here.** `STANDARD.md` in the repo is a snapshot and is never edited, the same rule as every other synced file.

**Re-sync at the moment it matters, not on a schedule.** The standard is only load-bearing when a component is created or restructured, so the sync happens immediately before that work. If nothing has changed, the sync is a no-op. If something has, the repo was stale and now isn't. Nothing detects drift automatically — the manifest records the rev it was synced at, and comparing that to this doc's current rev is a manual check — so tying the sync to the moment of use is what keeps it honest.

**Every change gets a dated line in the history below.** One line, what changed and why. This is what makes a convention trustworthy to someone reading it six months later, including a Claude Code session that has never seen the conversation it came from.

**A component that doesn't fit is evidence about the standard, not an exception to it.** Either the shape is wrong and this document changes, or the component is wrong and it changes. No component is exempted. Exemptions are how a convention stops being one.

## The document index

`DOCS.md` at the repo root lists every synced document: its title, its Claude Doc URL, the file it syncs to, and the rev and date of that snapshot.

It is **generated from the sync manifests and never hand-written** — its first line says so. The manifests stay the source; this is a derived view that collects what is already there into one table.

It is regenerated in the same pull request as any manifest change, which is the only moment it can go wrong.

It does two jobs at once. It is the list of every working document, so no bookmarks are needed — open the repo, open the index, follow a link. And because it carries each snapshot's rev beside its source, it is the staleness check: a rev behind the live doc means that file in the repo is out of date, visible at a glance instead of by opening four manifests.

## Change history

| Date | Change |
| --- | --- |
| 2026-11-05 | Project level given a required set (README, brief, manifest) and a table of named optional types, after `principles.md` was found to match no row in the standard. Components stay fixed because they repeat; projects vary structurally, so the project level is required-plus-named-optional rather than fixed. |
| 2026-11-05 | Added `DOCS.md`, a generated index of every synced document and its Claude Doc URL, so working documents are reachable from the repo rather than from bookmarks. |
| 2026-11-05 | Front matter rule corrected: for synced files `type` and `status` live in the manifest and the sync writes them, because a hand-added block is wiped on the next sync. |
| 2026-11-05 | Created. Fixed component file set replacing per-component judgment, after `build-log.md` and `build-guide.md` diverged between the two existing components. Decision logs consolidated to `design.md` after `document-workbench` was found keeping three. |
