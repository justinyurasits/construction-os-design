---
type: readme
status: current
---

# Document workbench

The Construction OS component that holds a company's governed knowledge and turns it into documents: retrieval over the company's library, rules loaded by ID, deterministic pricing, structured drafting and Word rendering. The first slice is a priced potential change order, reached through the advisor or drafted directly.

Product-level docs (the Product Brief and the Principles) are one folder up, in [construction-os/](../).

## Where things stand

Corpus and governance built. PCO generation designed and built. Retrieval designed, not running — the evaluation set is written and has not been scored.

## The docs

| File | What it is |
| --- | --- |
| [design.md](design.md) | The workbench architecture: knowledge model, document types, configuration and registry, the publish step, authority order. Holds the decision log; decisions are recorded once, there. |
| [pco-design.md](pco-design.md) | The build design for the first vertical slice: components, the PCO definition, the pricing engine, structured drafts and Word rendering, retrieval, acceptance tests, stack and build order. |
| [plan.md](plan.md) | The work: phases, what's done, what's next, future work. Tracks work only; decisions live in the System Design. |
| [build-log.md](build-log.md) | The story of the build, step by step, with the numbers. Raw material for the article. |

All four are synced from Claude Docs; `sync-manifest.yaml` records the source doc and revision for each. Edit the Claude Doc, not these files.

The architecture diagram in the PCO technical design doesn't export to Markdown; see it in the Claude Doc.
