---
type: readme
status: current
---

# Construction OS demos

Small, standalone tools built in the same domain as Construction OS, to show the
approach to general contractors, subcontractors and clients. Each one solves one real
problem end to end. None of them shares code or data with the Construction OS product
(the corpus and workbench in [`construction-os/`](../construction-os/)).

## Product-level docs

| File | What it is |
| --- | --- |
| [brief.md](brief.md) | What the demos are for and who they're shown to. Draft. |

## Components

| Component | Folder | Status | What it is |
| --- | --- | --- | --- |
| Fieldscope | [fieldscope/](fieldscope/) | prototype | Subcontractor safety compliance: OSHA-grounded protocols, training tracking, PPE checks from site photos. |
| PCO Generator | [pco-generator/](pco-generator/) | live | Turns a described change into a formatted change order, live at [draftconstructionchangeorder.com](https://draftconstructionchangeorder.com/). |

## Repositories

| Repository | What it holds |
| --- | --- |
| [`fieldscope`](https://github.com/justinyurasits/fieldscope) | Fieldscope's code. Public. Deployed on Render. |
| [`pco-generator`](https://github.com/justinyurasits/pco-generator) | The PCO Generator's code. Public. Deployed on Render, serving draftconstructionchangeorder.com. |

The two may later merge into one `construction-os-demos` repository, one folder per
demo. That needs both Render services repointed in the same sitting.

## How these docs work

Repo-authored, edited by pull request. Nothing is synced from Claude Docs yet.
