> **Synced from Claude Docs. Edit there, not here.**
> Source: [Construction OS — Document Workbench Build Log](https://claude.ai/artifact/NftJYcF7HYKyDsLxmv2pjp) · doc revision 27 · synced 2026-11-19

# Construction OS — Document Workbench Build Log

Nov 17, 2026 · @Justin

The story of building the document workbench, step by step, with the numbers. Started Nov 17, 2026, when the corpus became its own component and its Build Log stayed with it.

## Before this log

The workbench's first steps are told in the [corpus Build Log](https://claude.ai/artifact/16iv5fjzH4Nvqsgx3aYbo8), where they happened alongside the corpus work, and stay there so that story reads whole:

- **Step 28:** the PCO definition, the registry and the company configuration (corpus #61, #62; app #1).
- **Step 29:** the first rendered PCO, compared with the old system's (corpus #63; app #2).
- **Step 34:** the pricing engine (app #4 to #6; corpus #69, #70).

## Steps

1. **Drafted from rough notes with an LLM, and kept every number in code (Nov 8–10).** Build step 5 (app #7) took PM notes in and gave a priced Word draft out. Claude proposes scope, quantities and amounts, each cited word for word from the inputs, through one tool call. Code validates the proposal (one retry with the errors, then a clear error), assembles the draft, prices it with the engine and renders it; a proposal that carries a price is rejected. Project context lives behind a ProjectStore interface: one folder per project, read-only inputs, versioned drafts. 229 tests; case 1 priced at $5,614.40 and case 4 at $6,129.00. Two rounds of polish followed. The first rendered the new layout, inserted the company's default clarifications word for word and split the PM checklist into two tiers (app #8). The second made the PCO a standalone letter: backup filed with it in the job folder instead of attached, Owner selections referenced by ID through PRO-34 (CHG-53 4.0; corpus #72, app #10). General conditions weeks now round before they multiply, so the printed line reconciles (app #9). On Nov 10 the live runs passed and Justin judged the case 1 PCO good.

2) **Took the old system's layout and kept the new system's rules (Nov 10).** The old system's cedar closet PCO was better organized, so step 5a brought its format across (corpus #73, app #11): a branded first page, a description paragraph with "The work includes:", pricing grouped by division with subtotals (a new PRICING-PRESENTATION setting; Beacon Hill Interiors uses by\_division), schedule activities, grouped assumptions, and the Contractor and the Owner signing side by side. The correctness rules stayed: the notice box, the Executive co-sign, no email approval, no rounding. The old PCO rounded $54,415.34 to $54,500.00; ours never rounds. No tagline on the cover (principle 8). A cedar closet test from a transcript with no prices found the first real pricing bug: day-rate crews weren't priced from the company rate table. Now they are, and a different draft rate yields to the table and is flagged (app #12).

3. **Estimated from cost history instead of leaving blanks (Nov 10).** Step 5c (corpus #74, app #13) moved ahead of the revision loop, so the PM's first review would be of a fully estimated draft. A read-only script extracted SYS-09's unit-cost sheet into structured cost data: 1,258 rows, 1,249 used, with the problems reported rather than fixed (947 items with a single data point, 4 misfiled rows, 5 totals that don't add up). The model looks up cost items and picks one by id; code checks the id and unit, takes the price at the company's range point (mid) and does the takeoff math with the company's waste factors. Measurements and durations are labeled estimates, listed on the PM checklist and never shown to the Owner. Acceptance case 6 (cedar closets, from a real site-walk transcript with the Owner's name changed) is graded on structure, not on a total. 371 tests passed. Live, case 6 passed every structure check except one unpriced line.

4) **Said each thing once (Nov 10–17).** Reading the case 6 draft as a PM, Justin found it better but repetitive: the scope of work came through twice, and quantities and sizes repeated across descriptions, basis phrases and assumptions. The fix put checks where the model can't get past them (corpus #75, app #14). A line description is a short label, rejected if it starts with its trade, puts a number next to a unit or says "lump sum". A measurement appears only in Basis of quantities, and an assumption may not repeat an inclusion. Code adds the field-measurement assumption whenever a draft has measurements, and the Owner-upgrades clarification became generic. 412 tests passed.
5) **Graded the acceptance cases without calling the model (Nov 17–19).** The acceptance tests had skipped on every run, with a stale "build step 5 doesn't exist" reason and an empty body, so no passing test count had ever included a PCO acceptance case. Now each draft case with a recorded model proposal is replayed through the pipeline offline and graded with the same checks the live script uses; advice cases skip until step 7. The live script gained `--record` and `--runs` to refresh recordings. The recordings for cases 1 and 4 moved into the corpus, next to their cases, because they come from the company's own jobs (app #20, corpus #83). 414 passed, 4 skipped. Case 6 has no recording yet; the next live run makes one. Alongside it, CLAUDE.md took the corpus spec into its reading list and then template v1.3 (app #18, #22).

Roll-up: construction-os-workbench #1–#16 (baseline, Nov 17, 2026). Pull requests through #16 are covered by the steps in the corpus Build Log or by steps 1 to 4 above; the first roll-up starts at #17.

Roll-up: construction-os-workbench #17–#22 (Nov 19, 2026).
