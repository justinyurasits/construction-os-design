---
type: readme
status: current
---

# Construction OS

A company-specific AI system for residential builders that understands how a company operates and produces the documents its PMs and superintendents need. First slice: a priced potential change order.

This folder holds the product-level docs. Each component has its own folder.

## Product-level docs

| File | What it is |
| --- | --- |
| [brief.md](brief.md) | Who it's for, the painful moment, what it replaces, the wedge, what's out of scope. Every product and architecture decision is checked against it. |
| [principles.md](principles.md) | The ten principles for building company knowledge an AI can rely on, each with the rules that follow, the incidents that taught it, and where it's enforced. Applies to every component. |
| [architecture.md](architecture.md) | The product's map: terms, how it works (onboarding, drafting, library changes), how company knowledge flows, every part and its responsibility, one PCO request start to finish, boundaries, authority, status, and product-level decisions. Draft: four proposals await review. |

## Components

| Component | Folder | What it is |
| --- | --- | --- |
| Document workbench | [document-workbench/](document-workbench/) | The knowledge and authoring component (the RAG part): governed company knowledge, retrieval, pricing, drafting and Word rendering. Builds the priced potential change order first. |
| Intake router | [intake-router/](intake-router/) | Reads inbound messages and says which workflow each should start. Pass 0 is a classifier with evals. |

## How these docs work

**The Claude Docs are the working copy. These folders are the reviewed, versioned record.**

- Every design doc is written and edited in Claude Docs. Each synced file starts with a link to its source doc.
- When a doc changes in a way that matters (a decision, a principle, a design change, or the end of a working session), it's exported to Markdown and synced here in a pull request. The PR diff is the review of what changed.
- Nobody edits synced files by hand. If something here is wrong, fix the Claude Doc and re-sync.
- Between syncs, a folder can be behind the Claude Docs. The Claude Doc is current; the folder is the last reviewed version.
- Each folder's `sync-manifest.yaml` records which Claude Doc each file comes from and the revision last synced.

**Where decisions live:** product-level decisions are on [architecture.md](architecture.md); until the docs are reorganized, most of them are still recorded in the document workbench's [design.md](document-workbench/design.md) decision log, which stays their source.

## Related repositories

- `construction-os-corpus`: the company knowledge package (currently Beacon Hill Interiors').
- `document-workbench`: the document workbench application (renamed from `construction-os` on Nov 5). Holds no company content.

Product design docs live here, not in the corpus, because the corpus is one company's package and the template every company copy is forked from.
