---
type: readme
status: current
---

# Document workbench

The Construction OS component that turns a company's governed knowledge into documents: retrieval over the company's library, rules loaded by ID, deterministic pricing, structured drafting and Word rendering, with the PM reviewing and revising each draft. The first slice is a priced potential change order, reached through the advisor or drafted directly. The knowledge itself is the [corpus](../corpus/), which the workbench reads through its published package.

Product-level docs (the Product Brief, the Principles and the Architecture) are one folder up, in [construction-os/](../).

## Where things stand

The PCO slice drafts and prices end to end: the pricing engine, cost history, LLM drafting into structured data and Word rendering are built, and acceptance case 6 runs live. The PM revision loop (step 5b) is next. Retrieval is designed, not running: the evaluation set is written and has not been scored.

**Code:** the [`construction-os-workbench`](https://github.com/justinyurasits/construction-os-workbench) repository (public; holds no company content) — its CLAUDE.md points back to this folder. **Knowledge:** the [corpus](../corpus/), in [`construction-os-corpus`](https://github.com/justinyurasits/construction-os-corpus).

## The docs

| File | What it is |
| --- | --- |
| [spec.md](spec.md) | Points to the corpus spec for the domain; requirements not yet written. |
| [design.md](design.md) | The workbench's scope and boundaries, what isn't designed yet, and the workbench decision log. Decisions are recorded once, there. |
| [pco-design.md](pco-design.md) | The build design for the first vertical slice: components, the PCO definition, the pricing engine, structured drafts and Word rendering, retrieval, acceptance tests, stack and build order. |
| [plan.md](plan.md) | The workbench work still ahead: milestones, each with an exit criterion, starting with the PM revision loop (step 5b). Bugs and small tasks are GitHub issues. |
| [build-log.md](build-log.md) | The story of the workbench build. Its first steps (28, 29 and 34) are told in the [corpus build log](../corpus/build-log.md); the steps from Nov 8 on are told here. |

`README.md` and `spec.md` are written in this repo. The other four are synced from Claude Docs; `sync-manifest.yaml` records the source doc and revision for each. Edit the Claude Doc, not these files.

The architecture diagram in the PCO technical design doesn't export to Markdown; see it in the Claude Doc.
