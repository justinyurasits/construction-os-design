# Construction OS

Design docs for Construction OS: what the product is, how it's built, what we decided and why, and what we learned.

## How these docs work

**The Claude Docs are the working copy. This folder is the reviewed, versioned record.**

- Every design doc is written and edited in Claude Docs. Each file here starts with a link to its source doc.
- When a doc changes in a way that matters (a decision, a principle, a design change, or the end of a working session), it's exported to Markdown and synced here in a pull request. The PR diff is the review of what changed.
- Nobody edits these files by hand. If something here is wrong, fix the Claude Doc and re-sync. A PR that changes a design file without a matching Claude Docs change means the two copies have drifted.
- Between syncs, this folder can be behind the Claude Docs. The Claude Doc is current; this folder is the last reviewed version.
- `sync-manifest.yaml` records which Claude Doc each file comes from and the revision last synced.

## The docs

| File | What it is |
| --- | --- |
| [product-brief.md](product-brief.md) | Who it's for, the painful moment, what it replaces, the wedge, what's out of scope. Every product and architecture decision is checked against it. |
| [system-design.md](system-design.md) | The architecture and the decision log. Decisions are recorded once, here. |
| [pco-technical-design.md](pco-technical-design.md) | The build design for the first vertical slice: a priced potential change order. |
| [plan.md](plan.md) | The work: phases, what's done, what's next. Tracks work only; decisions live in the System Design. |
| [build-log.md](build-log.md) | The story of the build, step by step. Raw material for the article. |
| [principles.md](principles.md) | The ten principles for building a great document set, each with the rules that follow, the incidents that taught it, and where it's enforced. |

## Related repositories

- `construction-os-corpus`: the company knowledge package (currently Beacon Hill Interiors').
- `construction-os`: the application. Holds no company content.

Product design docs live here, not in the corpus, because the corpus is one company's package and the template every company copy is forked from.
