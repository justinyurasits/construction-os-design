> **Synced from Claude Docs. Edit there, not here.**
> Source: [Plan](https://claude.ai/artifact/6FvtBWB9bFMVdzMMTrwi42) · doc revision 105 · synced 2026-11-08

# Construction OS Corpus Cleanup & Change Control Plan

Oct 30, 2026 · @Justin

## Core principle

Put the documents under change control first, not last. Once the raw corpus is in git and tagged, every cleanup step after that is a tracked, reversible diff.

This also solves the baseline problem: you can clean freely, because you can always run the retrieval eval against the untouched original by checking out the `v0-raw` tag.

**Two repos, two jobs:**

- `construction-os-corpus` (private): the documents, the manifest, the conflict register
- `rag-system` (private): the code, the eval set, the eval spec

## The plan

Recalibrated Oct 31 after the design review: build one document type end to end (change orders) before spreading governance work across the whole corpus. Format conversion is mechanical and done corpus-wide; governance metadata is done one domain at a time.

### Phase 0: Freeze — done

- [x] Private repo `construction-os-corpus`, every file committed as found
- [x] Tagged `v0-raw`

### Phase 1: Inventory — done

- [x] `tools/inventory.py` (read-only) and `reports/manifest_draft.csv`
- [x] Counts confirmed: 171 docs, 0 local duplicates, 7 docs without numbered sections
- [ ] Commit the Phase 1 script and report

### Phase 2: Authority scan — done

- [x] `tools/authority_scan.py`: precedence and authority language across the corpus
- [x] Precedence matrix per contract set (prime, subcontract)
- [x] Where the 10 core rules are stated, and by which documents
- [ ] Justin reads SYS-05, SYS-04 (done), SYS-01, EXEC-01

Results: rankings conflict across the subcontract forms and prime-contract documents; core rules 3, 4, and 9 are stricter than their SOPs; spending limits differ across FCM-19, FCM-06, OPS-02. Still to do: commit `tools/` and `reports/`. The 341 numeric values the filter dropped get reviewed for the change-order documents in Phase 5.

### Phase 3: Format conversion and mechanical cleanup — done (v1-clean pushed)

- [x] Pilot Markdown conversion on 10 hard docs (SUB-05, SUB-T01, SUB-A01, CHG-53, FCM-09, COM-80, PRO-22, WF-02, CON-13, STG-B)
- [x] Fidelity check script: same words, tables, and section counts as the inventory
- [x] Bulk conversion `on a markdown-conversion branch, front matter id, title, source_file only; SOPs become Markdown-only, forms, contracts, and templates keep a .docx print master; .xlsx and logos unchanged`
- [x] Archive CON-13 v1 and PRE-05 v1; move the stale index and `example.txt` out of `docs/`; keep one SYS-10a logo
- [x] Restyle SUB-T01's Golden Rules (separate commit after bulk, with manifest correction); escape only blanks that render wrongly; WF-02 keeps its .docx (WF-01's removed: no images)
- [x] Tag `v1-clean`
- [x] Fix SUB-T01's "Section-by-Section PM Guidance" heading level
- [x] Freeze `manifest_draft.csv` as the v0-raw baseline; new runs write `manifest.csv`
- [x] Merge authority-scan, then markdown-conversion; update scan scripts to read Markdown
- [ ] Issue: SYS-02 footer says v2, filename says v1

### Phase 4: POL-01 and SYS-00 — approved, effective 2026-11-01 (pull requests #1 and #2)

- [ ] Governance document built from the System Design doc and the authority scan
- [ ] 10 core rules move into a Level 1 policy; SYS-05 and the project instructions reference it

* [x] POL-01 drafted: 12 rule blocks, all decisions applied
* [x] `POL-01 verified, revised, and merged in pull request #1; set status approved and effective date in a follow-up pull request`
* [x] SYS-00 drafted with role mapping, workday, change checks, and company acceptance testing; merged in pull request #1
* [ ] Approved glossary of acronyms for procedures and definitions
* [ ] Pull requests required for main: enforced by a CLAUDE.md rule for now (GitHub only enforces rulesets on private repos with a paid plan); upgrade to GitHub Pro before a second person or customer joins
* [ ] One rename commit: drop version numbers from filenames, update internal links
* [x] Before merging pull request #1: expand SYS-00 §7.5 with the consistency checks and company acceptance testing; add the role-name mapping (Principal and Operations Lead = Executive) to SYS-00 §2
* [ ] Turn the POL-01 verification into a reusable consistency-check tool
* [x] Library migration: version numbers removed from 192 file names; tools updated (pull request #5)
* [x] SYS-00 2.0: template type, legal\_review field, company profile and {{variables}} (pull request #6)
* [x] BHI extraction: identity to the company profile; market language neutralized; report of every change
* [x] Front matter on all documents (layers mostly core; company layer = profile, SYS-06, SYS-10, SYS-11)
* [x] Remediation report merged (pull request #10, reports/remediation.md): 52 open, 19 resolved, 21 changed, 13 decision questions, 206 new conflicts, 94 not-POL-01 issues, 58 uncounted possibles. Spot-check 4 of 5 real. The report is a dated baseline; GitHub issues track fixes from here.
* [x] POL-01 front matter: owner Product Owner, undefined supersedes field removed; scope\_check.py now covers POL-01 (pull request #11). All 170 core documents now owned by Product Owner.
* [x] Backlog created: GitHub issues #15 to #48 (34 issues; every one of the 432 report rows in exactly one issue). Rule passes #15 to #27, mechanical #28 and #29, attorney packet #30, per-document #31, plan items #32 to #45, possibles #46, closed records #47 and #48. Groups: old core-rules lists (SYS-04 §8, SYS-05 to SYS-08, \~47 rows); one pass per rule (AUTH-WRITTEN first = Phase 5 change-order slice; WAIVER-SEQUENCE after attorney); version stamps and body footers (item 29, 103 footers); SOP-number references to IDs; per-document fixes.
* [x] SYS-05 to SYS-07 rewritten, not retired: rule lists replaced with a pointer to POL-01; SYS-04 §8 and SYS-08 too, with SYS-08's five stale file names fixed (pull request #13; Table 2 rows 161–207). Decision 3 settled: the FCM document owns the control, the PM SOP owns the steps (see decision log). Next: plan issue log item 9 (retire fidelity check; scope check with a declared list of changed documents), then the change-order slice.
* [ ] GitHub tour for Justin, right after the backlog issues are created: Issues tab, labels, how "Closes #N" links a pull request to an issue, reviewing a pull request diff, merging, branches, and where Actions would run checks. Walk through one real issue from open to closed.
* [ ] Document references to IDs (GitHub #29, after #28, before the stage field): replace old numeric references (#51, Doc 51, Document #51, SOP #5) with document IDs. Urgent because GitHub links "#51" to issue or pull request 51 whenever body text is quoted. Code builds a mapping table first and Justin approves it: folder numbers ("#02 -- Drawings") are not documents, and "SOP #N" inside a series means that series' document (SUB-0N). Expand #29's scope from 4 rows to all four styles library-wide.
* [ ] Stage field (mechanical PR after #28): read each document's body stage line into front matter as applies\_to: stage (a list where a document spans stages); compare with SYS-04's stage tables and the STG-A to STG-E guides and report mismatches for Justin to settle; body stage line removed only after the field is confirmed. Rest of applies\_to stays domain by domain.
* [x] Fix SYS-08's two stale file names
* [ ] Generate manifest.csv on the next inventory run
* [ ] Core brand kit definition (logo, letterhead, brand guide) and onboarding check
* [ ] Regenerate .docx print masters from Markdown (listed in the extraction report)

### Issue log: BHI extraction review (pull request #7 merged Nov 1)

Found reviewing reports/bhi\_extraction.md on Nov 1. Numbered for reference; worked top to bottom. These numbers are plan issue log items, not GitHub numbers: in the repo, refer to them as "plan issue log item N". When the backlog moves to GitHub issues, record each item's GitHub number here.

**Before merge**

- [x] \#1 Quality-standard variable: sentences read wrong with the core default; decided: default "the standard required by the Contract Documents", BHI "the standard expected in high-end residential construction" (d8e3714); follow-up commit for list-item openings, SUB-A11 5.1 order, SUB-07 definition
- [x] \#2 "First-class, workmanlike" duplicated where the default repeats the original text
- [x] \#3 Insurance variable circular: fixed (ad8c97f); SUB-A11 9.1 now points to SUB-A04 directly
- [x] \#4 Review company/bhi/profile.yaml and fill empty fields: done by Justin on the branch; added entity\_type for #17
- [x] \#6 WF-01 example used a real client's dollar amounts: replaced with invented figures (b353dd8); "based on" wording fix pending
- [x] \#10 SUB-06 10.8 narrowed: "luxury homes" became "occupied residences"; decided: summary changes to "This level of care is required on every project." (fix pending)
- [x] \#11 SUB-06 10.1 broadened: "high-end residential projects" became "projects"; confirmed: applies to all projects
- [x] \#12 SUB-00 and SUB-A11 5.8 broadened to "every project": confirmed
- [x] \#13 SUB-A11 5.1 restructured contract sentence; check it reads correctly (being fixed with #1: variable moves to end of sentence)

**Soon**

- [ ] \#7 (GitHub #32) CON-13 Word file still holds BHI identity in a core file; regenerate the 5 out-of-date print masters
- [ ] \#9 (part 1 done in pull request #14; rest is GitHub #45) Retire the conversion fidelity check after this pull request; replace with: structure check (front matter, IDs, headings, numbering, links, images) on every pull request; scope check for mechanical pull requests (only the declared kind of change, compared to the previous commit); content rules (no company identity in core, no copied rule values, every variable exists in the profile); output check on generated and regenerated documents; meaning reviews per SYS-00 7.5
- [ ] \#17 (GitHub #35) SUB-A11 19.9: "\[Massachusetts corporation / LLC\]" becomes a profile value; section is mislabeled "Headings"
- [ ] \#18 (GitHub #36) SUB-A03 project block preset to Massachusetts; project location is request input
- [x] \#20 Remove SYS-02 section 10 (Claude Project Connection) in its own pull request after extraction merges; keep the "output location" idea for document definitions
- [ ] \#23 (GitHub #39) SUB-A04 insurance limits are all blank placeholders: make each limit a variable (general liability per occurrence and aggregate, auto, umbrella, employer's liability; workers' compensation statutory) with core defaults and questionnaire questions; get BHI's actual minimums from the insurance broker (subcontractor slice)
- [ ] \#25 (GitHub #40) Release packaging: what ships to other companies is a release build of docs/ only, never reports/, archive/, company/, or git history (the history and v0-raw keep real client details by design)
- [ ] \#26 (GitHub #41) Profile: signatory title and license numbers still empty; CON-13's Massachusetts section prints the Home Improvement Contractor number from the profile
- [x] \#27 WF-01 Appendix A intro reads "sample field set is a sample"; change to "The following is a sample owner-facing Statement of Billings."
- [x] \#28 POL-01 still status draft on main; missed in the approval pull request. Fixed in pull request #9 (63ac410)
- [ ] \#29 (GitHub #28) Version stamps in document bodies ("Version: 2.0" in SYS-02, CON-11, PRE-05, CHG-58 and the footer lines) conflict with front matter; remove in one mechanical pull request with a scope check
- [x] \#30 Converter would wipe governed front matter if rerun; guarded in pull request #9 (b04229e)

**Attorney packet**

- [ ] \#14 (GitHub #30) SUB-A01 states governing law and venue twice (14.4–14.5 and 19.1–19.2)
- [ ] \#15 (GitHub #30) SUB-04 12.2 legal claim about statutory lien waiver forms needs verification
- [ ] \#22 (GitHub #30) SUB-07 takes its definition of Contract Documents from the MSA (SUB-A01), and the MSA incorporates the SOPs, possibly including SUB-07: confirm the circular reference holds
- [ ] \#24 (GitHub #30) SUB-A11 does not incorporate SUB-A04: missing from its contract documents list (3.3) and order of precedence (3.4); SUB-A04 is titled "Schedule 1 — Insurance Requirements" but referenced by a different name

**Later**

- [ ] \#5 Variables print literally until the workbench fills them
- [ ] \#8 (GitHub #33) SYS-08 (and SYS-02) describe the three-Claude-Project setup; rewrite or retire once the workbench exists. SYS-02 still mentions Claude projects at its job-folder naming section and its monthly audit section.
- [ ] \#16 (GitHub #34) CON-13's 18% interest is a configurable rule plus a Massachusetts cap (jurisdiction rule)
- [ ] \#19 (GitHub #37) The 39 Massachusetts items: jurisdiction split and legal review
- [ ] \#21 (GitHub #38) SYS-00 writing rule for variables: a value must read correctly in every sentence it fills; a variable never starts a sentence or list item in prose (form labels such as a signature block are fine); each variable records its expected form
- [ ] \#31 (GitHub #42) EXEC-01 and SYS-03 are policy documents that don't yet meet the policy standards (no change history, acronyms); fix in their domain slices
- [ ] \#32 (GitHub #43) 26 procedures are named like logs or forms (Change Log, Punchlist Log, Prime Agreement); separate their templates during each domain slice
- [ ] \#33 (GitHub #44) SYS-09 (.xlsx) and SYS-10a (.svg) are assets without front matter; design an assets registry

### Workstream: governance documentation

The governance model lives in SYS-00 (the rules), the System Design doc (decisions and reasoning), and the build log (the story). None of them teaches the system to a new Policy Owner or PM.

- [ ] Fold decisions not yet in SYS-00 into a version update: brand kit slot every company fills; variable writing rule (item 21); release packaging, only docs/ ships (item 25); scope check as the standard check for mechanical changes; layer is classification, legal review is validation
- [ ] Governance guide (document\_type: guide): why every document has a type, layer, and owner; how to change a rule value; how to propose a change; what happens in a conflict; what the checks do and what to do when one fails; one change followed from request to approval
- [ ] Procedure: how to change a document (once the workbench exists)
- [ ] Procedure: how to configure a company (once the onboarding questionnaire exists)
- [ ] Documentation map: product overview, governance guide (SYS-12), onboarding guide, workbench user guide, administration procedures; generated references (document catalog, rules and questionnaire); glossary
- [ ] Library overview (raised Nov 2): the authoritative description of what the library is and how it fits together. Each document collection (CHG, FCM, SUB, PRO, CON, BIL, SCH, FLD, CLO, POL, SYS and the rest): what it covers, who uses it, and its type. How collections work together: POL sets rules, FCM owns controls, PM SOPs own steps, definitions and templates produce outputs, contracts bind the parties; how a change order or pay application moves through them across project stages. Likely replaces or regenerates SYS-01 and SYS-04 (the existing navigation documents, now stale) rather than adding a new one. Generated where possible from front matter, so it can't drift.
- [ ] Mark customer-facing decisions in the decision log with the guide that will explain them
- [ ] First snapshot of System Design, build log, and plan into design/ after the remediation report (marked "edit the Claude Doc, not this file")

### Phase 4b: Configuration architecture (started Nov 2; remaining rule passes paused)

Direction and the ten pending decisions are in the System Design doc, section 7. Done Nov 2 before the pause: POL-01 2.0 (#49), AUTH-WRITTEN passes 1 and 2 (#50, #51), body stamps removed (#52, closes GitHub #28), old references to IDs (#53, closes #29), applies\_to stage on every document (#54).

**Top priority, before anything ships (raised Nov 2):**

- [x] **IP and data provenance review.** SYS-09's pricing comes from $656K to $3.8M projects at 13 named Boston addresses, likely former employers' jobs, and much of the library was built while employed at those companies. Closed Nov 2: Justin confirmed no IP agreements restrict the library or data; no attorney review needed.
- [ ] **Remove client references from existing data:** project addresses and names in SYS-09 (sizing guide, source list) and anywhere else in docs/. Mechanical PR. Removes real client details from the product.
- [ ] Pricing database for each company is built at onboarding from its last 30 to 50 contracts and change orders (Product Brief, section 4).

* [ ] Read-only configuration inventory (running): every variable, POL-01 value, procedure value, jurisdiction value, identity and brand item
* [ ] Classify each candidate: constant, configurable parameter, identity, role mapping, conditional rule, jurisdiction constraint, or document or asset selection
* [ ] Decide 1 to 10 in section 7, one at a time, with the inventory in hand
* [ ] Refresh System Design (sections 2, 4 and 5 are stale: eight types, AI configuration, old example values) and fold the decisions into SYS-00 3.0
* [ ] Registry schema and the knowledge compiler, for POL-01, the governing financial control (FCM-03), and one change-order definition (potential change order)
* [ ] Second Massachusetts test company; generate the same document under both configurations; New Hampshire negative test later
* [ ] Success test: change one approved company setting, and every relevant output and validation changes with no core document edited or re-embedded
* [ ] Then resume the rule passes (AUTH-WRITTEN PRs 3 and 4 first), moving values into the registry instead of prose
* [ ] Product brief (Claude Doc, started Nov 2): customer, painful moment, what it replaces, wedge, out of scope, implications for the documents layer. Every architecture decision gets checked against it.
* [ ] Pricing method for the potential change order: define inputs, order of operations, markup structure and base, permits, tax, contingency, and the contract override, as a structured definition. Settle the SYS-06 vs SYS-09 conflicts first (markup base and order, PM rate, overhead). Five questions, starting from how Justin actually priced change orders: (1) markup on self-performed work, rate and base; (2) markup on subcontracted work (CON-16 says subs carry their own overhead and profit); (3) general conditions: always, only when the change extends the schedule (CON-13's more-than-10% rule), or a percentage; (4) tax: in material prices or a separate line; (5) order of application, including permits and the repeat-client discount. Future work, but it blocks the pricing calculations in the potential change order slice.
* [ ] Add SYS-09 to the configuration inventory (it scanned only Markdown). Log SYS-09 data errors (misfiled rows, totals that don't add, line count) for when its company-data future is decided.
* [ ] Add a `governs` front matter field: the rule or decision IDs each document controls (its authority domain). Today no document declares what it controls, so the system can't tell when two sources govern the same decision; authority is traced only through POL-01 rule IDs and definition dependencies. Start with POL-01, the FCM documents and the PCO path; the validator checks that each ID is governed by exactly one document. Future work, after the PCO slice. (Nov 3; Principles #1.)

### Phase 5 (revised Nov 2): Potential change order vertical slice

Replaces the old Phases 5 to 7 below with one end-to-end slice, per the recommended architecture adopted Nov 2 (System Design decision log). Corpus cleanup is no longer a prerequisite; this slice decides which documents get fixed.

- [x] **1. Change order family map** (read-only report): every document a potential change order touches, its type, its role (rule, control, steps, definition, template, contract term, example), its dependencies in both directions, and what's still wrong in it. Becomes the definition's dependency list, the slice's fix list, and the first chapter of the library overview. Done Nov 2 (draft PR #56): 73 documents, top 10 blockers, 29 definition items, 25 pricing inputs (10 with no source), 23 fixes. Decisions taken from it: not-to-exceed checkpoints 70% and 90%; no trade work before client authorization; CON-13 amended so a signed potential change order authorizes work.
- [ ] **2. Fix list:** fix only the documents the map flags (includes AUTH-WRITTEN PRs 3 and 4, the change event clock in STG-D, CON-12 and CON-15, billing alignment to FCM-04). Batch 1 merged Nov 2 (PR #59): 17 documents, authorization wording, change event clock, SCH-72 48 hours, not-to-exceed checkpoints, FCM-14 trade work, billing sentence, WF-02 signature step; closes #15 Table 1 rows 15, 17, 20, 117. Remaining: items waiting on the attorney, the PCO definition (#57), and SUB-02 (Decisions 4 and 5).
- [x] **3. Pricing methodology** (the five questions in Phase 4b). Settled Nov 2 from Justin's practice, in the System Design decision log and GitHub #58. The two small items are settled as defaults (PCO technical design section 11): the 1% application fee applies to every change order; actual permit fees pass through as their own line after markup.
- [x] **4. Technical design:** PCO definition schema (CHG-53-DEF, extracted from CHG-53), registry entries the PCO uses, pricing functions, Word template and deterministic rendering, publish step. The Claude Doc "PCO Slice — Technical Design" is the build spec. The app lives in document-workbench (created Nov 2 as construction-os, renamed Nov 5).
- [ ] **5. Acceptance set:** about 20 realistic potential change order requests (incomplete, conflicting rules, different contract terms, subcontractor quotes, missing costs), graded on the generated document. 5 written (corpus tests/acceptance/cases); none yet extends the schedule enough to add general conditions, so the next batch needs one.
- [ ] **6. Build** (technical design section 10), for Beacon Hill Interiors' package, then a second company:
  - [x] Step 1: examples and the approved pricing method (5 cases with expected totals)
  - [x] Step 2: CHG-53-DEF, registry, company config and the structured draft schema (corpus #61, app #1)
  - [x] Step 3: Word template and renderer, with the PM checklist (corpus #63, app #2)
  - [ ] Step 4: pricing engine and evidence interface. Next; Claude Code prompt written Nov 8.
  - [ ] Step 5: LLM drafting. Also decides where project context is stored, now that it's reused across a project's work (SYS-00 3.0 section 1.3).
  - [ ] Step 6: retrieval and contract term extraction
  - [ ] Step 7: advisor path
  - [ ] Step 8: second-company regression

### Phase 5: Change-order slice (governance)

*Superseded Nov 2 by the revised Phase 5 above, along with Phases 6 and 7.*

- [ ] Resolve conflicts in the change-order domain
- [ ] Extract rules into the registry with IDs, defaults, overridability, and interview questions
- [ ] Write the change-order document definitions (PCO, CCD, PCCO, SCO, T&M)
- [ ] Add `controls` and `applies_to` metadata to every document in the slice
- [ ] Scope: CHG-51 to 60, FCM-03, FCM-19, SUB-02, SUB-A06/A07, relevant CON-12/13 clauses

### Phase 6: Retrieval (`rag-system`)

- [ ] Hybrid search, exact ID lookup, metadata filtering
- [ ] Authority resolution: select what controls, flag conflicts
- [ ] Run the retrieval eval set; record the baseline

### Phase 7: Generation for change orders

- [ ] Pipeline: identify type, load definition, gather inputs, retrieve rules, resolve, generate, validate, render
- [ ] Validation in code against rule IDs
- [ ] Generation eval: missing approval, conflicting requirements, missing facts, superseded policy

### Phase 8: Next domains

- [ ] Repeat Phases 5 and 7 for RFIs, daily reports, meeting minutes

### Ongoing

- [ ] Send CON-13 change-order ranking to an attorney
- [ ] Full conflict audit (only \~30 of 171 docs read so far)
- [ ] Every finding is a GitHub issue; every fix is a pull request
- [ ] Preflight GitHub Action, changelog (Claude Project re-sync retired Nov 2)
- [ ] Keep the Principles doc current: add a row whenever a review, failed test or PM reaction teaches something. At the end of the build, use it with the Build Log to write the long-form article and posts.

## Decisions

Decisions are recorded once, in the decision log of the [System Design](https://claude.ai/artifact/3iEBRhf5uJpBXwf8TsCjG4) doc. This plan only tracks the work.
