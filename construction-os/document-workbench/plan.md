> **Synced from Claude Docs. Edit there, not here.**
> Source: [Workbench Plan](https://claude.ai/artifact/XLGhnNkJU17qqeLQThboPP) · doc revision 3 · synced 2026-11-17

# Construction OS Document Workbench — Plan

Nov 17, 2026 · @Justin

The workbench's work: the potential change order slice and what follows it. Moved word for word from the corpus Plan on Nov 17, 2026, when the corpus became its own component; the corpus keeps its own [Plan](https://claude.ai/artifact/6FvtBWB9bFMVdzMMTrwi42). Decisions live in the [workbench System Design](https://claude.ai/artifact/NcfkMXfG83Tg4NQpkh77TN); this plan only tracks the work.

## PCO vertical slice

Replaces the old Phases 5 to 7 (kept, superseded, in the corpus Plan) with one end-to-end slice, per the recommended architecture adopted Nov 2 (System Design decision log). Corpus cleanup is no longer a prerequisite; this slice decides which documents get fixed.

Items 1 to 3 of this phase (the change order family map, the fix list and the pricing method) are corpus work and stay in the corpus Plan.

- [x] **4. Technical design:** PCO definition schema (CHG-53-DEF, extracted from CHG-53), registry entries the PCO uses, pricing functions, Word template and deterministic rendering, publish step. The Claude Doc "PCO Slice — Technical Design" is the build spec. The app lives in document-workbench (created Nov 2 as construction-os, renamed Nov 5).
- [ ] **5. Acceptance set:** about 20 realistic potential change order requests (incomplete, conflicting rules, different contract terms, subcontractor quotes, missing costs), graded on the generated document. 5 written (corpus tests/acceptance/cases); none yet extends the schedule enough to add general conditions, so the next batch needs one.
- [ ] **6. Build** (technical design section 10), for Beacon Hill Interiors' package, then a second company:
  - [x] Step 1: examples and the approved pricing method (5 cases with expected totals)
  - [x] Step 2: CHG-53-DEF, registry, company config and the structured draft schema (corpus #61, app #1)
  - [x] Step 3: Word template and renderer, with the PM checklist (corpus #63, app #2)
  - [x] Step 4: pricing engine and evidence interface (app #4 to #6; corpus #69, #70)
  - [x] Step 5: LLM drafting. Built Nov 9 (app PR #7, 229 tests, case 1 at $5,614.40 and case 4 at $6,129.00). Done Nov 10: live runs pass and Justin judged the case 1 PCO good, after the standalone-PCO fixes (corpus #72, app #9 and #10). A cedar closet test from a transcript with no prices found a bug: day-rate roles (Demo Crew, Carpentry Crew (Finish)) are not priced from the rate table; fixed in step 5c. Claude Code's plan reviewed Nov 9 and approved with changes: branch from main; skip advice cases 2, 3 and 5; case 4 prices at company standard with the contract\_terms\_not\_applied flag; architect\_signs may be unknown; amounts the model transcribes are checked word for word; project workspaces are one folder per project behind a ProjectStore interface. Done when cases 1 and 4 produce priced drafts through the CLI (case 1 at $5,614.40) and Justin runs the live script.
  - [ ] Step 5a: PCO layout v2 (added Nov 10). Adopt the old system's format and organization, from its cedar closet PCO, while keeping every correctness rule (notice box, Executive co-sign, no email approval, "Potential", "Owner", letter voice, no rounding of totals). Branded first page; Prepared by and Requested by in the header table; a description paragraph plus "The work includes:" bullets, with scope stated once; an optional basis of quantities block; a new registry entry PRICING-PRESENTATION (by\_division with division subtotals and a separate summary, flat, or summary\_only; BHI set to by\_division); no-wrap pricing columns; an optional schedule activity breakdown; assumptions grouped under subheads with job-specific "Not included" items; Contractor and Owner signatures side by side; new section order. Two PRs, corpus first; before-and-after PDFs on a review-only corpus branch. Built Nov 10: corpus #73, app #11; the day-rate fix is app #12 (crew day rates now priced from the rate table). Tagline left off the cover (principle 8 unchanged); "Subtotal before markup" in the summary.
  - [ ] Step 5c: estimating from cost history (added Nov 10). SYS-09 (1,258 items from 12+ projects) cleaned into structured cost data; the model breaks scope into line items within each division, each mapped to a cost-history item or labeled an estimate; it may propose measurements and durations, and code does the area, waste and totals; a company setting picks which point of a cost range to use; general conditions appear as hours and days at rate so the PM can adjust them. Fix the day-rate pricing bug first. The aim is a better starting point for the PM, not a final price. Moved ahead of 5b on Nov 10, so the PM's first review in case 6 is of a fully estimated draft.
  - [ ] Step 5b: PM review and revision (added Nov 10). The PM reads a draft and gives feedback in plain words ("super is 2 days, drop the dumpster, add a second coat of finish"); the app produces the next version (v002, v003) in the same project folder, with the feedback saved as an input and a change summary: what moved, from what to what, and the new total. Rules: an amount the PM gives is a sourced amount (source PM, dated); code computes every total; lines the feedback does not mention stay unchanged, and a test checks that every difference between versions traces to a feedback item; feedback that conflicts with company policy (for example, skipping the Executive co-sign) is flagged and policy holds. Done when acceptance case 6 passes: the cedar closet transcript gives a v001 with a complete, sourced line structure, and Justin's written feedback gives a v002 that changes exactly what he asked and nothing else. Waiting on Justin's feedback for case 6.
  - [ ] Step 6: retrieval and contract term extraction
  - [ ] Step 7: advisor path
  - [ ] Step 8: second-company regression

**Status, Nov 17:** step 5a and the day-rate fix are merged (corpus #73; app #11, #12). Step 5c is merged (corpus #74, app #13): acceptance case 6 runs live, with every structure check passing except one unpriced line. The wording fix that removes repeated scope, quantities and sizes is merged in the corpus (#75); confirm the app PR. Next: Justin reruns case 6, reviews the draft as a PM, and his written feedback becomes the input for step 5b.

## Open work

Moved from the corpus Plan's lists of Nov 8 to 10:

- [ ] Project workspaces: access control and retention, required before any customer.
- [ ] Step 6 scope: contract type (fixed price, cost-plus, GMP, T&M) becomes a project fact read from the executed contract; on cost-plus, the contract's fee replaces company markup and subcontract markup limits apply. PCO pricing assumes fixed price until then. Cost backup on cost-plus goes monthly with billing, not with the PCO.
- [ ] Acceptance cases, next batch: a cost-plus change and a change that adds general conditions.

Added Nov 17:

- [ ] Write the workbench Build Log from Nov 8 on: LLM drafting (app #7 to #10), layout v2 and day rates (#11, #12), estimating from cost history (#13), the wording fix, and what each review found.
