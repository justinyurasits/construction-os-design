---
type: readme
status: current
---

# PCO Generator

Turns a description of a change into a formatted construction change order (scope
language, pricing, and the structure a general contractor actually issues) as a Word
document and a PDF.

## Where things stand

Live at [draftconstructionchangeorder.com](https://draftconstructionchangeorder.com/).
Built (v3), not validated. In the live version the model writes every price and total,
and nothing checks them. The [design](design.md#4-decision-log) records the decision to
move all pricing arithmetic into code; it isn't built or scheduled.

**Code:** [`pco-generator`](https://github.com/justinyurasits/pco-generator)

The free, standalone version of the job. Construction OS builds the same document as
its first governed slice, from a company's own standards, in
[`construction-os-workbench`](https://github.com/justinyurasits/construction-os-workbench).

## The docs

| File | What it is |
| --- | --- |
| [brief.md](brief.md) | Who it's for, the painful moment, what it replaces, what's out of scope. Draft: audience open. |
| [spec.md](spec.md) | Requirements R1–R11, each marked met or not met by the live code. Draft. |
| [design.md](design.md) | How v3 works, the decided pricing-in-code design, and the decision log. Draft. |
| [plan.md](plan.md) | M1–M4, unscheduled: the app stays as it is for now. Draft. |
| [build-log.md](build-log.md) | June 19 build, reconstructed from commits, and the Nov 19 findings. |
