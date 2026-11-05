---
type: readme
status: current
---

# Intake router (Pass 0)

Design docs for the Construction OS intake router: an intent classifier and router, built with an eval set so its accuracy can be measured. Pass 0 uses construction data only and stops at a label plus a simulated routing record.

## How these docs work

**The Claude Docs are the working copy. This folder is the reviewed, versioned record.** These files are exported from Claude Docs and synced here by pull request. Nobody edits them by hand. `sync-manifest.yaml` records the source doc and the revision last synced.

## The docs

| File | What it is |
| --- | --- |
| [build-guide.md](build-guide.md) | What we are building, the architecture, how it fits Construction OS, the classifier prompt design, build order and open decisions. |
| [spec.md](spec.md) | The source of truth for the 14 intents, the pair rules, the hold rules and the labeled set. Still carries SOP IDs in its Handling lines, so keep this repo private until they are stripped. |
| [classifier-prompt.md](classifier-prompt.md) | The full prompt the router sends to the model, with a version log. Derived from the spec; change the spec first. |

The diagrams in the build guide are static PNG snapshots in `images/`. Re-export them when the drawing changes.

## Related

The labeled set and the code will live in a separate `intake-router` code repo, once the build starts.
