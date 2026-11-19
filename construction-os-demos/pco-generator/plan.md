---
type: plan
status: draft
---

# PCO Generator — Plan

**Draft.** No code work is scheduled: the live app stays as it is. The milestones
below are what it would take to build the decided design
([design.md](design.md#4-decision-log)) when that changes.

## Now

Nothing scheduled.

## Next

### M1 Code repository ready to change safely

The repository follows the standard and has tests that run, so the pricing change has
something to stand on.

- **Exit criterion:** the repository has CLAUDE.md, README, .gitignore and the pull
  request template from `_template/repo/`. `__pycache__/`, `.DS_Store`, `output/` and
  the test documents are no longer tracked. pytest runs in CI on every pull request,
  with the model call stubbed, and passes.
- **Covers:** groundwork for R4–R8.
- **Depends on:** nothing.

### M2 Pricing in code

Every number in the document is calculated by code from a rate or a contractor input.

- **Exit criterion:** the rate table is a data file. The model returns structured line
  items with no dollar amounts. Unit tests cover line, subtotal, each markup component,
  total and `[TBD]` handling. Golden tests for the three `test_run.py` cases match
  totals worked out by hand. Justin signs off on one live PCO for each cause category
  he picks.
- **Covers:** [R4](spec.md#r4-every-number-comes-from-code),
  [R5](spec.md#r5-no-number-without-a-source),
  [R6](spec.md#r6-revised-contract-sum), [R7](spec.md#r7-validity-date).
- **Depends on:** M1.

### M3 Fixed language and complete documents

- **Exit criterion:** Contract Modification, Validity and Authorization come from
  templates. A missing narrative section fails the request instead of being dropped.
  Errors return a plain message.
- **Covers:** [R2](spec.md#r2-produce-every-section-in-order),
  [R8](spec.md#r8-fixed-contract-language-comes-from-code),
  [R11](spec.md#r11-fail-without-leaking).
- **Depends on:** M2.

### M4 Evaluation set

- **Exit criterion:** at least ten realistic field-note cases, covering every cause
  category and blank costs, each with the expected line items and a reviewer's check
  that no scope was added. Results are recorded and re-run whenever the prompt or model
  changes.
- **Covers:** [R3](spec.md#r3-scope-language-stays-within-the-input).

## Later

- Move to a current model ID and recheck output length at the new max_tokens.
- Merge into a `construction-os-demos` repository with Fieldscope (both Render services
  repointed in the same sitting).
- Decide the demo's call to action once the [demos brief](../brief.md) is settled.

## Open questions blocking the plan

- None. Rate ranges, the PM's numbers vs. the rate sheet, sample-rate labelling and the
  Authorization clause were decided on 2026-11-19 ([design.md](design.md#4-decision-log)).
