---
type: readme
status: current
---

# Design records

How the systems get designed, written while they're being built rather than
reconstructed afterward. Every document is drafted in a Claude Doc, reviewed,
and synced here through a pull request — so the history shows what changed,
when, and what it said before.

**Start with [principles.md](construction-os/principles.md).** Ten principles
for building organizational knowledge an AI can rely on, each one anchored to
a specific failure in this build: a carpenter rate recorded as $89 in one
source and $90 in another, so two systems priced the same change $7.26 apart.
2,526 stale document references that GitHub turned into links to unrelated
pull requests. Four days of governance work before anyone had named a
customer.

| Project | Folder | What it is |
| --- | --- | --- |
| Construction OS | [construction-os/](construction-os/) | A company-specific AI system for residential builders. Components: the [document workbench](construction-os/document-workbench/) — knowledge, retrieval and drafting — and the [intake router](construction-os/intake-router/), which classifies inbound messages and routes them to a workflow. |
| Agents | [agents/](agents/) | Small agents built to learn how agent loops work, starting with a job evaluator. Docs moving here from the [`agents`](https://github.com/justinyurasits/agents) repo ([#26](https://github.com/justinyurasits/design/issues/26)). |
| Fieldscope | [fieldscope/](fieldscope/) | Subcontractor safety compliance prototype. Docs moving here from the [`fieldscope`](https://github.com/justinyurasits/fieldscope) repo ([#26](https://github.com/justinyurasits/design/issues/26)). |

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
- **The Claude Doc is the working copy; the folder is the reviewed, versioned
  record.** Changes sync here by pull request and the files are never edited
  by hand. Each synced file starts with a link to its source.
- **[DOCS.md](DOCS.md)** lists every synced document across all manifests,
  with its source, path and revision.
- **[STANDARD.md](STANDARD.md)** is the document model: what each file in a
  component is for, and the rules that keep it that way.
- **[_template/](_template/)** is the standard as files: `project/` with every
  project-level file, `component/` with the full component set, and `repo/`
  with the files every code repository starts with (CLAUDE.md, pull request
  template, README, .gitignore).
- **Design leads, code follows.** Every design doc lives here. Code pull
  requests capture small decisions and build notes; Claude Code asks to roll
  them up into the design docs, and nothing goes in without approval.
- **Every change is a branch and a pull request.** Never commit to main.

To add a project: copy `_template/project/`, rename it, fill it in, and add a row
to the table above. To add a component: copy `_template/component/` into the
project and list it in the project README. To start a code repository: copy
`_template/repo/` into it and fill in section 7 of its CLAUDE.md.
