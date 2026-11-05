---
type: readme
status: current
---

# Document workbench

The Construction OS component that holds a company's governed knowledge and turns it into documents: retrieval over the company's library, rules loaded by ID, deterministic pricing, structured drafting and Word rendering. The first slice is a priced potential change order, reached through the advisor or drafted directly.

Product-level docs (the Product Brief and the Principles) are one folder up, in [construction-os/](../).

## Where things stand

Corpus and governance built. PCO generation designed; the Word template and renderer are built, while the pricing engine (build step 4) and LLM drafting (step 5) are not. Retrieval designed, not running: the evaluation set is written and has not been scored.

**Code:** the [`document-workbench`](https://github.com/justinyurasits/document-workbench) repository. **Domain:** the governed library it reads, in [`construction-os-corpus`](https://github.com/justinyurasits/construction-os-corpus).

## The docs

| File | What it is |
| --- | --- |
| [spec.md](spec.md) | The domain: what the governed library holds, where each of its rules is defined (SYS-00, POL-01, definitions, registry), its boundaries, the audit reports, and known gaps in the source. |
| [design.md](design.md) | The workbench architecture: knowledge model, document types, configuration and registry, the publish step, authority order. Holds the decision log; decisions are recorded once, there. |
| [pco-design.md](pco-design.md) | The build design for the first vertical slice: components, the PCO definition, the pricing engine, structured drafts and Word rendering, retrieval, acceptance tests, stack and build order. |
| [plan.md](plan.md) | The work: phases, what's done, what's next, future work. Tracks work only; decisions live in the System Design. |
| [build-log.md](build-log.md) | The story of the build, step by step, with the numbers. Raw material for the article. |

`spec.md` is written in this repo. The other four are synced from Claude Docs; `sync-manifest.yaml` records the source doc and revision for each. Edit the Claude Doc, not these files.

The architecture diagram in the PCO technical design doesn't export to Markdown; see it in the Claude Doc.
