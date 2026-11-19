> **Synced from Claude Docs. Edit there, not here.**
> Source: [Construction OS — Corpus Plan](https://claude.ai/artifact/6FvtBWB9bFMVdzMMTrwi42) · doc revision 179 · synced 2026-11-19

# Construction OS — Corpus Plan

Oct 30, 2026 · @Justin

Work still ahead for the corpus: milestones, each with an exit criterion. Finished work is in the [Build Log](https://claude.ai/artifact/16iv5fjzH4Nvqsgx3aYbo8). Decisions are in the [System Design](https://claude.ai/artifact/3iEBRhf5uJpBXwf8TsCjG4) decision log. Bugs and small tasks are [issues in construction-os-corpus](https://github.com/justinyurasits/construction-os-corpus/issues). The PCO build steps are in the [workbench Plan](https://claude.ai/artifact/XLGhnNkJU17qqeLQThboPP).

## Now

### Document structure check

Every pull request checks every document's front matter and structure, so the library can't drift from SYS-00 unnoticed. Starts after workbench step 5b (Justin, Nov 10: finish the current work first).

- **Exit criterion:** `tools/check_documents.py` runs on every pull request beside the scope check. It checks front matter with the required fields (id, title, type, status, version, effective\_date, layer, owner, applies\_to.stage); type one of the nine; valid status, layer and stage values; owner a role from SYS-00, never a person; filename ID matches the front matter id; unique IDs; no version or date stamp in a body; no old numeric references (#51, Doc 51, SOP #5). The first run reports existing failures by rule, with no fixes in that pull request.
- **Why:** Principle 1 says it is "enforced by front matter validation", but only `scope_check.py` and the workbench's definition-dependency check run today (found Nov 10).
- **GitHub:** #45. Then #93 (run the checks in GitHub Actions) and design #38 (Principles accuracy pass).

## Next

### Change-order rule passes

The documents a PCO touches agree with POL-01, starting with AUTH-WRITTEN.

- **Exit criterion:** every AUTH-WRITTEN row in `reports/remediation.md` is fixed or recorded as accepted, and #15 is closed. Then the same for each remaining rule, one issue each.
- **Includes:** AUTH-WRITTEN PRs 3 and 4, the change event clock in STG-D, CON-12 and CON-15, billing alignment to FCM-04, and SUB-02 under remediation Decisions 4 and 5. Values move into the registry, not into prose. Items waiting on the attorney stay in #30.
- **GitHub:** #15, then #16 to #27; #31 for per-document fixes.

### Configuration proven on a second company

Everything company-specific lives in configuration, and the library splits into a starter and a company copy.

- **Exit criterion:** change one approved company setting, and every relevant output and validation changes with no core document edited or re-embedded. A fictional second Massachusetts company generates the same PCO under its own configuration. A New Hampshire negative test comes later.
- **Includes:** the mechanical starter split; the configuration decisions still pending in System Design section 7, taken one at a time with the inventory in hand; the registry beyond the PCO (POL-01 and FCM-03).
- **Depends on:** workbench step 8 (the fictional second company), built as the test of the split; #88 (client references) and #89 (SYS-09 in the inventory) first.

### Contract type across the library

Documents know whether a job is fixed price, cost-plus (with or without a GMP) or T&M, and work accordingly: PCO pricing and markup, billing support, time entry, change authorization (CHG-59 for T&M). The knowledge model already names contract type as an applicability dimension; only stage is filled today.

- **Exit criterion:** `applies_to: contract_type` is filled where a requirement differs, CHG-53-DEF keys its rules on it, the project workspace stores the contract type once, and an acceptance case for each contract type passes.
- **Depends on:** designed with workbench step 6.

### House style, then the second document type

Company-wide house style moves out of CHG-53-DEF's presentation into one shared file every definition uses: defined terms "the Contractor" and "the Owner", number style "six (6)", writing as a letter to the Owner, nothing internal on Owner documents.

- **Exit criterion:** CHG-53-DEF reads house style from the shared file with its acceptance cases unchanged, and the second document type adds only its own definition, template, standard language and acceptance cases.
- **Order,** by the brief's test: PCCO, then the PRO-34 selection sheet (its Selection Approval Form; PCOs already reference Owner selections by ID), then the RFI.

## Later

- **Governance documentation.** A new Policy Owner or PM can run the library without help. Done when there is a governance guide (SYS-12, type guide): why every document has a type, layer and owner; how to change a rule value or propose a change; what happens in a conflict; what the checks do and what to do when one fails; one change followed from request to approval. Also procedures for changing a document (once the workbench exists) and configuring a company (once the onboarding questionnaire exists), a documentation map, and a library overview that replaces or regenerates SYS-01 and SYS-04 from front matter (#66). Customer-facing decisions in the decision log get marked with the guide that explains them. Related: #84 (glossary), #92 (SYS-00 fold-in).
- **`governs` front matter field.** Each document lists the rule or decision IDs it controls, and the validator checks that each ID is governed by exactly one document. Start with POL-01, the FCM documents and the PCO path. After the PCO slice (Nov 3; Principle 1).
- **Full conflict audit.** Only about 30 of 171 documents have been read for conflicts. Done when every document is read and each finding is an issue. Related: #46.
- **Pricing data at onboarding.** Each company's pricing database is built at onboarding from its last 30 to 50 contracts and change orders (Product Brief, section 4).
- **Attorney packet,** at the very end: when the first client signs, an attorney reviews the documents before the starter library ships to them (Justin, Nov 10). Covers #30, #34, #37, #20, the five standard clarification texts in CHG-53-DEF and the CON-13 change-order ranking. Until then the texts stay marked pending attorney review, and BHI uses its own language under Justin's review.
- **The article.** At the end of the build, write the long-form article and posts from the Principles and the Build Log. Until then, add a Principles row whenever a review, failed test or PM reaction teaches something.

## Open questions blocking the plan

- None today. The configuration decisions still pending in System Design section 7 are part of the second-company milestone.

## Decisions

Decisions are recorded once, in the decision log of the [System Design](https://claude.ai/artifact/3iEBRhf5uJpBXwf8TsCjG4) doc. This plan only tracks the work.
