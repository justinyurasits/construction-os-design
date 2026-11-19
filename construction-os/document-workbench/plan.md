> **Synced from Claude Docs. Edit there, not here.**
> Source: [Construction OS — Document Workbench Plan](https://claude.ai/artifact/XLGhnNkJU17qqeLQThboPP) · doc revision 34 · synced 2026-11-19

# Construction OS Document Workbench — Plan

Nov 17, 2026 · @Justin

Work still ahead for the workbench: milestones, each with an exit criterion. Finished work is in the [workbench Build Log](https://claude.ai/artifact/NftJYcF7HYKyDsLxmv2pjp), and the PCO slice's first steps are in the [corpus Build Log](https://claude.ai/artifact/16iv5fjzH4Nvqsgx3aYbo8). Decisions live in the [workbench System Design](https://claude.ai/artifact/NcfkMXfG83Tg4NQpkh77TN). Bugs and small tasks are issues in construction-os-workbench. The corpus keeps its own [Plan](https://claude.ai/artifact/6FvtBWB9bFMVdzMMTrwi42).

## Now

### PM review and revision (build step 5b)

The PM reads a draft and gives feedback in plain words ("super is 2 days, drop the dumpster, add a second coat of finish"). The app produces the next version (v002, v003) in the same project folder, with the feedback saved as an input and a change summary: what moved, from what to what, and the new total.

- **Rules:** an amount the PM gives is a sourced amount (source PM, dated); code computes every total; lines the feedback doesn't mention stay unchanged, and a test checks that every difference between versions traces to a feedback item; feedback that conflicts with company policy (for example, skipping the Executive co-sign) is flagged and policy holds.
- **Exit criterion:** acceptance case 6 passes. The cedar closet transcript gives a v001 with a complete, sourced line structure, and Justin's written feedback gives a v002 that changes exactly what he asked and nothing else.
- **Depends on:** Justin rerunning case 6 with the wording fix and writing his feedback as a PM.

## Next

### Retrieval and contract terms (build step 6)

The workbench finds the rules and contract terms that apply instead of assuming them. Contract type (fixed price, cost-plus, GMP, T&M) becomes a project fact read from the executed contract. On cost-plus, the contract's fee replaces company markup and subcontract markup limits apply; cost backup goes monthly with billing, not with the PCO. PCO pricing assumes fixed price until then.

- **Exit criterion:** the retrieval evaluation set is scored and its baseline recorded, and case 4 prices under its contract ($5,737.00), citing the contract section, without the contract\_terms\_not\_applied flag.
- **Depends on:** designed with the corpus's "Contract type across the library" milestone.

### Acceptance set of about 20 cases

Realistic PCO requests (incomplete, conflicting rules, different contract terms, subcontractor quotes, missing costs), graded on the generated document. Six are written.

- **Exit criterion:** about 20 cases, including a cost-plus change and a change that extends the schedule enough to add general conditions. Every check that can run without the live model runs on every pull request; the live cases run on demand.

### Advisor path (build step 7)

The PM tells the advisor what happened; it cites the rules that apply and drafts the documents (Product Brief, the wedge).

- **Exit criterion:** advice cases 2, 3 and 5, skipped in step 5, pass: each answer cites the governing rule IDs, and the same conversation can start a PCO draft.

### Second-company regression (build step 8)

The workbench works for a company it was never written for.

- **Exit criterion:** a fictional second company's package produces PCOs that pass the acceptance cases under its own configuration, with no change to workbench code.
- **Depends on:** built with the corpus's "Configuration proven on a second company" milestone, as the test of the starter split.

## Later

- **Project workspaces for customers:** access control and retention, required before any customer.

## Open questions blocking the plan

- None today.
