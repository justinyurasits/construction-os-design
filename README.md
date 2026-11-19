---
type: readme
status: current
---

# Design records

How the systems get designed, written while they're being built rather than
reconstructed afterward. Most documents are drafted in a Claude Doc, reviewed,
and synced here through a pull request; the rest are written here directly, also
by pull request. Either way the history shows what changed, when, and what it
said before.

**Start with [principles.md](construction-os/principles.md).** Ten principles
for building organizational knowledge an AI can rely on, each one anchored to
a specific failure in this build: a carpenter rate recorded as $89 in one
source and $90 in another, so two systems priced the same change $7.26 apart.
2,526 stale document references that GitHub turned into links to unrelated
pull requests. Four days of governance work before anyone had named a
customer.

| Project | Folder | What it is |
| --- | --- | --- |
| Construction OS | [construction-os/](construction-os/) | A company-specific AI system for residential builders. Components: the [corpus](construction-os/corpus/) — the company's governed knowledge — the [document workbench](construction-os/document-workbench/) — retrieval, pricing and drafting — and the [intake router](construction-os/intake-router/), which classifies inbound messages and routes them to a workflow. |
| Agents | [agents/](agents/) | Small agents built to learn how agent loops work, starting with a job evaluator. Component: the job evaluator. Code in [`agents`](https://github.com/justinyurasits/agents). |
| Construction OS demos | [construction-os-demos/](construction-os-demos/) | Standalone tools in the same domain: Fieldscope (subcontractor safety compliance) and the PCO Generator (live at draftconstructionchangeorder.com). |

## Where things stand

| | Designed | Built | Validated |
| --- | --- | --- | --- |
| Document corpus and governance | ✓ | ✓ | Partial — policy verified against procedures |
| PCO generation | ✓ | ✓ | — |
| Retrieval | ✓ | — | — |
| Intake router | ✓ | — | — |

Nothing here is claimed as working until it is. An evaluation set written is
not an evaluation run.

## How this repo works

- **Each project gets its own folder**, with its own README listing its docs.
  Each folder of synced files has a `sync-manifest.yaml`.
- **Synced documents:** the Claude Doc is the working copy and the folder is the
  reviewed, versioned record. Changes sync here by pull request and the files
  are never edited by hand. Each synced file starts with a link to its source.
- **Repo-authored documents** (no sync header, such as the agents docs) are
  edited here by pull request and follow the same standard.
- **[DOCS.md](DOCS.md)** lists every synced document across all manifests,
  with its source, path and revision.
- **[STANDARD.md](STANDARD.md)** is the document model: what each file in a
  component is for, and the rules that keep it that way.
- **[_template/](_template/)** is the standard as files: `project/` with every
  project-level file, `component/` with the full component set, and `repo/`
  with the files every code repository starts with (CLAUDE.md, pull request
  template, README, .gitignore).
- **Design leads, code follows.** Every design doc lives here, except visual
  design: colors, type, marks and components are in
  [`brand-system`](https://github.com/justinyurasits/brand-system), and product
  docs that need a visual rule point there. Code pull
  requests capture small decisions and build notes; Claude Code asks to roll
  them up into the design docs, and nothing goes in without approval.
- **Every change is a branch and a pull request.** Never commit to main.

`python tools/validate.py` checks the structure (required files, front matter, manifests, DOCS.md, links) and runs on every pull request.

To add a project: copy `_template/project/`, rename it, fill it in, and add a row
to the table above. To add a component: copy `_template/component/` into the
project and list it in the project README. To start a code repository: copy
`_template/repo/` into it and fill in section 7 of its CLAUDE.md.
