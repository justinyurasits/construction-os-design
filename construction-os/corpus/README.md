---
type: readme
status: current
---

# Corpus

The Construction OS component that holds a company's governed knowledge: its policies, procedures, controls, contracts and forms, the registry of configurable values, the company's own values and rate tables, document definitions and Word templates. Every other part that needs the company's knowledge, starting with the [document workbench](../document-workbench/), reads it through the published package; none of them owns it. The first company package is Beacon Hill Interiors'.

Product-level docs (the Product Brief, the Principles and the Architecture) are one folder up, in [construction-os/](../).

## Where things stand

Inventoried, converted to Markdown and under change control: 173 documents, the governing policy (POL-01) and the document system rules (SYS-00) approved, front matter on every document, a registry of 24 configurable items, and one document definition (CHG-53-DEF, the potential change order). A remediation report is the dated baseline, and its findings are open GitHub issues. Checks that run on every pull request today: the scope check and the workbench's definition-dependency check. The document structure check is planned, not built. Most of the library outside the change-order family has not been read for conflicts.

**Repository:** [`construction-os-corpus`](https://github.com/justinyurasits/construction-os-corpus) (private) — its CLAUDE.md points back to this folder.

## The docs

| File | What it is |
| --- | --- |
| [brief.md](brief.md) | Who relies on the corpus and what it must make possible, where that narrows the product brief. |
| [spec.md](spec.md) | The domain: what the library holds, where each of its rules is defined (SYS-00, POL-01, definitions, registry), its boundaries, the audit findings, and known gaps in the source. |
| [design.md](design.md) | The corpus architecture: knowledge model, document types, configuration and registry, the publish step, authority order. Holds the corpus decision log; decisions are recorded once, there. |
| [plan.md](plan.md) | The corpus work: phases, what's done, what's next, future work. Tracks work only. |
| [build-log.md](build-log.md) | The story of the corpus build, step by step, with the numbers. Raw material for the article. |

`README.md`, `brief.md` and `spec.md` are written in this repo. The other three are synced from Claude Docs; `sync-manifest.yaml` records the source doc and revision for each. Edit the Claude Doc, not these files.

Until Nov 17, 2026 these docs sat in [document-workbench/](../document-workbench/), and the System Design, Plan and Build Log covered the workbench too. The workbench's sections and decisions moved word for word to its own docs; product-level decisions moved to [architecture.md](../architecture.md).
