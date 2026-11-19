---
type: readme
status: current
---

# Construction OS

A company-specific AI system for residential builders that understands how a company operates and produces the documents its PMs and superintendents need. First slice: a priced potential change order.

This folder holds the product-level docs. Each component has its own folder.

**Start with [principles.md](principles.md).** Ten principles for building
organizational knowledge an AI can rely on, each one anchored to a specific failure in
this build: a carpenter rate recorded as $89 in one source and $90 in another, so two
systems priced the same change $7.26 apart. 2,526 stale document references that GitHub
turned into links to unrelated pull requests. Four days of governance work before anyone
had named a customer.

## Where things stand

| | Designed | Built | Validated |
| --- | --- | --- | --- |
| Document corpus and governance | ✓ | ✓ | Partial — policy verified against procedures |
| PCO generation | ✓ | ✓ | — |
| Retrieval | Partial — in scope; lookup, search and authority resolution not yet designed | — | — |
| Intake router | Partial — spec and classifier prompt written; brief, design and plan still in the build guide | — | — |

Nothing here is claimed as working until it is. An evaluation set written is not an
evaluation run.

## Product-level docs

| File | What it is |
| --- | --- |
| [brief.md](brief.md) | Who it's for, the painful moment, what it replaces, the wedge, what's out of scope. Every product and architecture decision is checked against it. |
| [principles.md](principles.md) | The ten principles for building company knowledge an AI can rely on, each with the rules that follow, the incidents that taught it, and where it's enforced. Applies to every component. |
| [product-spec.md](product-spec.md) | What the product must do for its users: capabilities with IDs (`COS-CAP-01`), journeys and acceptance criteria. **Placeholder, not yet written.** |
| [architecture.md](architecture.md) | The product's map: terms, how it works (onboarding, drafting, library changes), how company knowledge flows, every part and its responsibility, one PCO request start to finish, boundaries, authority, status, and the product-level decision log. Draft: three proposals await review. |

## Components

| Component | Folder | What it is |
| --- | --- | --- |
| Corpus | [corpus/](corpus/) | The company's governed knowledge: documents, registry, company values and rate tables, definitions and templates. Every other part reads it through the published package. |
| Document workbench | [document-workbench/](document-workbench/) | The authoring component (the RAG part): retrieval, pricing, drafting, Word rendering and PM revision, reading the corpus. Builds the priced potential change order first. |
| Intake router | [intake-router/](intake-router/) | Reads inbound messages and says which workflow each should start. Pass 0 is a classifier with evals. |

## How these docs work

Most docs here are synced from Claude Docs; each synced file starts with a link to its source, and the folder's `sync-manifest.yaml` records the revision. How syncing, roll-ups and the rest work is in the [root README](../README.md); the rules are in [STANDARD.md](../STANDARD.md).

**Where decisions live:** product-level decisions are on [architecture.md](architecture.md). A component's own decisions are in its design.md: the [corpus](corpus/design.md) and the [document workbench](document-workbench/design.md). Each decision is recorded once.

## Repositories

- [`construction-os-corpus`](https://github.com/justinyurasits/construction-os-corpus) (private): the corpus, the company knowledge package (currently Beacon Hill Interiors'). Its docs are in [corpus/](corpus/).
- [`construction-os-workbench`](https://github.com/justinyurasits/construction-os-workbench): the document workbench application (created as `construction-os`, renamed `document-workbench` on Nov 5, `construction-os-workbench` on Nov 17). Holds no company content. Public.

Product design docs live here, not in the corpus, because the corpus is one company's package and the template every company copy is forked from.
