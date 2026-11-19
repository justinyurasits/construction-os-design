---
type: readme
status: current
---

# Intake router (Pass 0)

Design docs for the Construction OS intake router: an intent classifier and router, built with an eval set so its accuracy can be measured. Pass 0 uses construction data only and stops at a label plus a simulated routing record.

## Where things stand

Designed. Not built.

**Code:** none yet. The labeled set and the code will live in a separate `intake-router` code repo once the build starts.

## The docs

| File | What it is |
| --- | --- |
| [build-guide.md](build-guide.md) | What we are building, the architecture, how it fits Construction OS, the classifier prompt design, build order and open decisions. |
| [spec.md](spec.md) | The source of truth for the 14 intents, the pair rules, the hold rules and the labeled set. Its Handling lines still carry SOP IDs. |
| [brief.md](brief.md), [design.md](design.md), [plan.md](plan.md) | Drafts. Their content is still in the build guide, until it's split into the standard file set in Claude Docs. |
| [classifier-prompt.md](classifier-prompt.md) | The full prompt the router sends to the model, with a version log. Derived from the spec; change the spec first. |

The diagrams in the build guide are static PNG snapshots in `images/`. Re-export them when the drawing changes.
