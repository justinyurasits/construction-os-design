# CLAUDE.md

Design docs for several projects, one folder per project.

## Rules

- Never commit or push directly to main. Every change goes on a branch and through a pull request.
- A synced file (one that starts with the "Synced from Claude Docs" header) is never edited by hand. Change the Claude Doc, export it, and replace the file in a sync PR. Keep the two-line header, and update that file's `rev` and `synced` in the folder's `sync-manifest.yaml`.
- One sync PR per project unless asked otherwise.
- A new project gets its own folder, a README, and a row in the root README table.
- Within a project, product-level docs sit at the top of its folder and each component gets a subfolder with its own README and `sync-manifest.yaml`.
- Don't rewrite git history.
- No secrets, ever.

## Component structure

Every component has the same files from the day it is created. A file with
nothing settled in it yet exists at `status: draft` and says what is open.
Nothing holds two jobs.

| File | Its one job |
|---|---|
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

- **One decision, one source.** Decisions live in that component's `design.md`
  log. A plan or build log may reference a decision; neither records one.
- **One document, one job.** If a file matches two rows above, it is two files.
- Every `.md` carries front matter: `type` and `status`
  (`draft | current | superseded`). Sync state lives in the manifest, not here.
- Filenames are lowercase-kebab `.md`. No version numbers in filenames.
- Restructuring happens in the Claude Docs first. The repo follows via sync;
  synced files are never hand-edited.
- A new component is this file set, not a decision about which files to make.
