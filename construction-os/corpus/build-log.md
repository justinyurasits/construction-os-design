> **Synced from Claude Docs. Edit there, not here.**
> Source: [Build Log](https://claude.ai/artifact/16iv5fjzH4Nvqsgx3aYbo8) · doc revision 21 · synced 2026-11-08

# Construction OS Corpus Audit — Build Log

Oct 31, 2026 · @Justin

A running record of building a hybrid-search RAG system over the Construction OS library, and the corpus audit that turned out to matter more than the code. Raw material for an article.

## Steps so far

Two days, Oct 30–31, 2026. The plan started as a code project and became a document-quality project by step 5.

1. **Picked a learning goal.** Build hybrid search (keyword + semantic) over a real corpus: the Construction OS library of SOPs, forms, and contracts. Stack: Postgres + pgvector, OpenAI embeddings, Reciprocal Rank Fusion, Claude for answers.
2. **Set up the code repo.** Private `rag-system` repo, API keys in a gitignored `.env`, and a `CLAUDE.md` that tells Claude Code to work one milestone at a time and stop when each test passes.
3. **Wrote the eval set before any code.** 35 questions: 10 that use exact doc IDs, 10 paraphrased in plain field language, 10 direct, and 5 the library can't answer. Each names the doc and section that should come back.
4. **Wrote the scoring rules.** Strict hit = right doc and section in the top 5. Lenient = right doc or an accepted alternative. The gap between them measures chunking quality. Each rule quietly put a demand on the documents: one stable ID per file, consistent numbered sections, one correct answer per question.
5. **The scoring rules exposed the documents, before any scoring ran.** Filling in expected sections meant reading the corpus the way a retriever would. The eval spec then needed a list of caveats just to keep scoring fair: duplicates, a truncated FCM-16A, and Q13, whose target (FCM-11's 9 AM rule) contradicts the 48-hour core rule, so its answer can't be graded until someone decides which source wins. Once the scoring spec needs caveats about the documents, the documents are the problem. Added a corpus readiness step ahead of indexing.
6. **Checked the old cross-reference index.** It listed 173 docs and 117 open issues, but used a naming scheme that no longer matched any current file. It was stale.
7. **Interviewed the existing Claude Project.** Six questions to the AI that already used these documents daily: inventory, naming conventions, duplicates, its own instructions, conflicts, and section numbering.
8. **Put the corpus under change control before cleaning it.** New private repo `construction-os-corpus`, every file committed as found, tagged `v0-raw`.
9. **Ran a read-only inventory script.** Claude Code proposed a plan first, flagged that the expected counts were wrong instead of fitting the script to them, then parsed all 171 documents.

10) **Read the inventory results.** 171 documents, zero ID conflicts, zero duplicates locally. The 14 duplicates existed only in the Claude Project, which also held different versions of CON-13 and PRE-05. The local folder, not the Project, became the source of truth.
11) **Found the missing hierarchy.** Precedence conflicts existed because nothing said which document wins. Worse, the 10 "non-negotiable" core rules lived in an AI prompt, not a governed document: the prompt had quietly become a source of policy.
12) **Got an outside design review.** It separated four questions the hierarchy had merged (authority, function, applicability, lifecycle), pointed out that retrieval rank is not authority rank, and argued for building one document type end to end before cleaning the whole corpus.
13) **Set the product scope.** The RAG system is the document workbench inside Construction OS: understand company policy and generate documents. Project records are a separate, later system, and anything a user supplies for a request is ephemeral.
14) **Designed the knowledge model.** Eight document types; document definitions split out of SOPs as their own files; requirements sorted sentence by sentence into policy, procedure, or definition; core, jurisdiction, and company layers; overrides at the rule level; roles instead of people.
15) **Turned configuration into an interview.** Every overridable rule carries a plain-language question and a default, so onboarding is generated from the rule registry. Extracting rules during cleanup also builds the onboarding product.

16. **Surveyed authority language before scanning.** Claude Code ran a read-only survey first and found most hits were noise ("Financial Controls", insurance "policy"). It also found the core rules restated in at least four AI prompt files with drifting wording, the subcontract precedence order restated in about nine documents, and an existing "Governance Hierarchy" section in SYS-04 that may be the original design intent.

17) **Re-read the original design (SYS-04, SYS-05).** Most of the new model was already there, implicitly: SYS-04's FCM table maps which controls document governs which PM SOPs (a ready-made `controls` map), its lifecycle tables assign every document a stage, and SYS-05's role list and drafting rules describe the workbench and document definitions before either had a name. What was missing was structure: the policy lived in prompt prose, the hierarchy ranked by breadth rather than authority, and the core rules existed in five copies.

18. **Ran the full authority scan.** One read-only script across all 171 documents captured 1,033 passages: precedence clauses, authority claims, and numeric rules. Every quote in its summary was checked word for word against the source. The core rules turned out to be stricter than the procedures they cite, the three subcontract forms rank documents differently, and spending limits disagree across three documents. The must/shall filter caught only 70 of 411 numeric values, so the rule list is a start, not a census.

19) **Piloted the Markdown conversion on the 10 hardest documents.** All 10 matched their sources word for word and in order, with every section and table intact. The fidelity check was tested by corrupting a file seven ways and caught all seven. Rule adopted: conversion is not editing. Fixes like restyling SUB-T01's Golden Rules happen afterward as separate, visible commits. Tool guides with annotated screenshots (WF-01, WF-02) keep their Word originals.

20. **Resolved the first policy conflicts, and found most weren't conflicts.** Two of the three core-rule clashes were two separate rules squeezed into one slogan: receipts are capture (24 hours) plus coding (weekly); time entry is a deadline plus a correction window. Real practice also differed from all the documents: BHI enters time weekly on Fridays. The fix was applicability, not a winner: weekly for fixed-price work, daily where hours are billing backup (T&M, cost-plus).

21) **Converted the whole corpus.** All 167 Word documents passed the fidelity check: 227,455 words, 61 tables, 4,354 sections, and 13 images, matching exactly. 146 SOPs, guides, and policies became Markdown-only; 21 forms, contracts, and templates kept their Word print masters. The only content lost was letterhead headers and footers on two documents, and every original remains at the v0-raw tag.

22. **Gave policy one home: POL-01.** The 10 core rules, plus the new spending-approval rule, moved into a single policy document with permanent rule IDs, configurable defaults, and a "carried out by" link to the procedures. Asking the Claude Project about its own instructions revealed one more copy: its custom instructions were a verbatim paste of SYS-05, with nothing keeping the two in sync.
23. **Settled the governance standards with a second outside review.** Front matter, permanent IDs, definitions linked through metadata, one source per rule value (rendered, not copied), and branch-and-pull-request change control. The review caught three real errors: retiring a document is not the same as revising it, layered products legitimately have several documents addressing one decision, and acronyms should be governed, not banned. The result: no acronyms in policy, and an approved glossary for procedures.

24) **Verified the policy against the procedures before approving it.** Of 39 "carried out by" links, only 9 fully held. Some gaps meant the documents were behind; others meant the policy was wrong. The draft banned signed time-and-materials authorizations and emergency work, contradicted a protective clause in the subcontract form, and would have required lien waivers for retail purchases. Fixing the policy first, then queuing the documents, turned 30 discrepancies into four decisions and a backlog. Merged as the first pull request under the new change process.

25. **Removed the company from the product.** Construction OS is for any general contractor, so BHI's identity moved into a company profile and documents now use variables like {{company.name}}. 65 changes across 27 documents. Reviewing the result line by line caught what a search could not: a variable whose default produced broken contract grammar, an insurance clause pointing to itself, a real client's billing figures still in an example, and wording changes that silently narrowed or broadened who a requirement applied to. The lesson: removing words from a contract is a legal edit, not a find-and-replace. The review also surfaced that the insurance schedule every subcontract relies on had no dollar limits at all.

26) **Retested every conflict against the approved policy (PR #10).** The remediation report found 53 known conflicts still open, 19 resolved by POL-01, 21 changed, 13 questions needing a policy call, 206 new conflicts in the documents that carry out each rule, and 95 problems that aren't policy conflicts. A spot-check of 5 random rows found 4 real and 1 over-called, and a close read of the three "most serious" findings found one real (subcontract waivers in the wrong order), one misclassified (stop-work authority isn't reversed, but the individual right to stop work and the protection from reprisal are missing), and one not a conflict at all (ambiguity inside a written scope is different from scope that isn't written). The lesson: AI reviewers over-call, and someone who knows the documents has to read the hard rows. The counts also cluster: about 47 rows come from five old documents restating the rules, and AUTH-WRITTEN alone has 88, so the backlog is about 15 grouped issues, not 300. The report also caught that an earlier fix had missed POL-01's owner field, and that the scope check skipped POL-01, the one document it most needed to protect (both fixed in PR #11).

27. **Started fixing, and the fixes taught the rules.** The backlog went to GitHub as 34 issues, every report row in exactly one. The change-order pass began with the policy itself (POL-01 2.0: a client-signed potential change order authorizes work; a not-to-exceed amount is a ceiling, never authorization), then the financial controls, then the change chain. Each review caught the AI going one step too far: banning email for allowance selections that aren't changes at all, restating a policy value while removing restated values, and stripping labels like "PCO" from "PCO CHG-53" in the name of tidiness. Two lessons became rules. The rule covers only what it covers. And an ID tells the system which document; a label tells the person what it is, so the library needs both. Mechanical cleanups ran beside the content work: 139 documents lost body version stamps that contradicted front matter, and 2,526 old references like "#51" became document IDs, urgent because GitHub was turning them into links to pull request 51.

28) **Gave the PCO a definition and the company a configuration.** Build step 2 turned prose into structured data: CHG-53-DEF says what a potential change order contains and which rules it depends on, 24 registry entries define every value it uses, and one company config file holds Beacon Hill Interiors' answers. A validator checks the package on every change. Writing the values down exposed a policy question: POL-01 3.0 now has the Executive co-sign before the client, as a configurable rule (corpus #61, #62; app #1).
29) **Rendered the first PCO and compared it with the old system's.** Build step 3 produced a Word template and a renderer. Put side by side, the old system wrote better (exclusions, the permit question, a schedule table) and the new one was correct (the $90 rate, terms that follow policy, no "Markup per the Contract" when no contract states one). The first draft also put "Who is the client?" at the top of page one. The template took the old system's protective language, unknowns became bracketed blanks, and the PM's questions moved to a separate checklist that never goes to the client (corpus #63; app #2).
30) **Wrote down the principles, and let a reviewer correct them.** Nine principles, each tied to the incident that taught it. An outside review corrected four: authority is contextual, not a fixed ladder; each company gets its own copy of the library, not merged layers; "never invent" bans fabricated facts, not labeled estimates; and the test is how much a draft reduces the work, not whether a PM would send it unread. It added a tenth: keep knowledge, request context and generated output separate.
31) **Moved the design docs out of the corpus, and found Claude Code planning from stale copies.** The design docs got their own repository, construction-os-design, synced from Claude Docs by pull request and organized as one product with two components, the document workbench and the intake router. The app repository was renamed document-workbench. Checking the repositories against each other showed that both CLAUDE.md files told Claude Code to plan from Nov 1 and 2 snapshots, missing a week of decisions. Both now point to the design repository, the snapshots are gone, and three files whose sync header another session had dropped got it back.
32) **Checked the documents against the design, and the design against the business.** The corpus got a README. SYS-01 turned out to be typed as navigation, which carries no authority, while half of it stated rules; its filing map also duplicated SYS-02 and disagreed with it on unlisted documents (issue #66). The Product Brief said Procore is the project record, but Beacon Hill Interiors' own procedures keep the job folder as the record even when Procore is used. Writing the workbench spec found SYS-00 still describing a runtime that merges layers.
33) **Rewrote SYS-00 to match what was decided, and loosened a rule written too strictly.** SYS-00 3.0 caught the governing document up with the Nov 2 architecture: each company has its own copy, layers are labels, values live in configuration, drafts are never blocked, and the checks section lists only the two that actually run. Justin pushed back on one line: request information "used for that request only" would make a PM re-supply the contract for the change order that follows its PCO. The real boundary is project versus company, so project context is now reusable within its project and never crosses into another project or into company knowledge (corpus #67).
34) **Built the pricing engine; the code asked the right questions.** Build step 4 moved pricing into its own module. Rates come from the company table, general conditions apply only past the 10% threshold, the contract replaces the company markup when it says so, permits pass through, and a price with no source is left blank. Given the spec, Claude Code stopped to ask instead of guessing: it wouldn't match a carpenter by parsing a description (lines now carry a role), and it asked whether general conditions run on calendar days or workdays. Review caught a contract-document problem the tests couldn't: 11/7 weeks charged as $2,828.57 printed as 1.57 × $1,800 = $2,826.00, so weeks now round first and the page multiplies out. A two-page limit on the PCO came out too, replaced by rules that keep the signatures, the pricing header and the total from being stranded. Case 1 prices at $5,614.40; case 4 at $5,737.00 under its contract and $6,129.00 at company pricing (app #4 to #6; corpus #69, #70).

## What the audit found

The file structure is cleaner than expected; the content inside the files is not. The script found zero ID conflicts, but the interview found 14 contradictions between documents and rules.

| Finding | Evidence | Source | Status |
| --- | --- | --- | --- |
| 171 unique documents, consistent filename IDs | 126 headers match the filename ID, 0 conflict, 47 have no ID in the header | Inventory script | Confirmed |
| Duplicates live only in the Claude Project | 14 PRO files uploaded twice there; 0 byte or text matches locally | Interview + script | Fix at next Project sync |
| Local folder and Project hold different files | CON-13 and PRE-05 have v1 and v2 locally; Project has only v2 | Script | Archive v1 |
| Stale files mixed into the corpus | Old cross-reference index and `example.txt` in `docs/` | Script | Move to archive |
| Body text uses four retired reference styles | `#54`, `Doc 54`, `Document #54`, `SOP #5`, all pointing to current IDs | Interview | Add aliases; rewrite later |
| Folder numbers collide with doc numbers | "#02 -- Drawings" is a folder, not PRE-02 | Interview | Rule for the alias resolver |
| 14 conflicts between documents and rules | 4 vs. core rules, 6 doc vs. doc, 4 filing locations | Interview | Conflict register |
| A live contract may rank change orders last | CON-13 §1 puts approved change orders below Exhibit A | Interview | Attorney review |
| No precedence rule | Instructions never say whether a document or a core rule wins | Interview | Decision needed |
| "Exhibit B" means two things | Schedule of Values (prime) vs. Work Order (subcontract) | Interview | Metadata tag |
| Four heading formats | Bold 139, Word styles 26, Markdown 6, none 2 | Script | Chunker handles all four |
| Numbered lists look like sections | 97 numbered lines correctly excluded; SUB-T01 "Golden Rules" still slips through | Script | Restyle SUB-T01 |
| 7 docs have no numbered sections | SUB-00, SUB-T02, SYS-05/06/07, SYS-10, WF-02 | Script | Heading-text fallback |
| The instructions do much of the work | 10 core rules and document pairings live in the prompt, not the docs | Interview | Port to the answer prompt |
| FCM-16A is truncated | Sections 1–3 only | Interview | Complete it |
| Core rules stated in 4+ places, wording drifting | SYS-05, SYS-06, SYS-07, SYS-08 each restate them; SYS-02 cites Core Rule #9; rule 4 cites FCM-11 + OPS-02 in SYS-05 but only FCM-11 in SYS-07 | Authority survey | Move to one Level 1 policy |
| Subcontract precedence restated \~9 times | SUB-A01, SUB-A02, SUB-A11, PRO-28, and each of SUB-03 to SUB-07 carry their own "In the event of conflict" ranking | Authority survey | One clause in the MSA; others reference it |
| Prime contract precedence disagrees | CON-13 v2 ranks the Addendum first; FCM-12 ranks the Prime Contract first "unless the contract explicitly states otherwise" | Authority survey | Precedence matrix, attorney |
| A controls map already exists in part | STG guides repeat "What This Document Controls:" per document; FCM-01 has a "Source of Truth For" table; SYS-04 has a "Governance Hierarchy" | Authority survey | Seed for the controls field |
| Subcontract forms rank documents differently | MSA is 2nd in SUB-A01, 1st in SUB-A02, 4th in SUB-A11; change orders 3rd, 4th, 1st. SUB-A02 §1.3 and §13.1 contradict each other. | Authority scan | One clause in the MSA; attorney |
| Core rules stricter than their SOPs | Receipts same day vs. 24 hours (FCM-16) or weekly (CST-64); time 48 hours vs. 9 AM (FCM-11); filing same day vs. 24 hours (SYS-02, COM-83). Five full copies, no master. | Authority scan | Policy decision per rule |
| Spending approval limits disagree | FCM-19 tiers $2,500 / $10,000 / $50,000; FCM-06 single $10,000; OPS-02 $5,000 for self-performed work | Authority scan | Resolve in change-order slice |
| SYS-04 hierarchy can't settle conflicts | "Top" never defined as authority; contradicts its own "sits parallel" FCM text; lists a SUB-08 that doesn't exist | Authority scan | Keep domains, drop ranking |
| Consistent values ready as defaults | 5% retainage, 18% late interest, 24-hour minutes, 48-hour mobilization | Authority scan | Rule registry defaults |
| The Claude Project's instructions are another unsynced copy | Project custom instructions are a verbatim copy of SYS-05; editing either leaves the other stale. SYS-05 still says \~158 SOPs (actual: 171). | Claude Project | Rewrite after the workbench design settles |

## Decisions

**Made**

- The `construction-os-corpus` repo is the source of truth; the Claude Project and Drive are copies synced from it.
- Freeze first, clean second: `v0-raw` preserves the corpus as found.
- Archive, never delete: retired files move to `archive/`.
- No document rewrites before the retrieval baseline runs, so the eval measures the corpus as it was.
- Prompt files (SYS-05/06/07) go in the answer prompt, not the search index.
- Scripts propose; a person decides document status, role, and merges.
- Every finding becomes a GitHub issue; every fix is a pull request that closes one.

**Open**

- [ ] Source format: Markdown for SOPs, or keep `.docx`
- [ ] Precedence: does a document or a core rule win? Includes 48 hours vs. 9 AM for time entry.
- [ ] Which CON-13 version went out to clients, then attorney review of its change order ranking
- [ ] Merge candidates (SCH-68/PRO-25, CLO-91–94, SUB-09/CHG-58), decided after the eval

## Article angles

The strongest thesis: a RAG project is a document-quality project wearing a code costume. The rest support it.

- **Write the test before the system.** 35 questions with known answers defined success before a line of code existed.
- **Interview the AI you already have.** The existing Claude Project knew the naming history, the conflicts, and where its own instructions were doing the work.
- **Your index is lying.** The cross-reference spreadsheet looked authoritative and matched none of the current files.
- **Version control before cleanup.** Tagging the raw corpus made every later fix reversible and kept the baseline honest.
- **The good AI pushed back.** Claude Code refused to tune its script toward expected counts that were wrong.
- **Scripts find structure; people find contradictions.** The script found zero ID conflicts. Reading the documents found 14 policy conflicts, one in a live client contract.
- **Corpus readiness is a product.** Most companies skip it and blame the model later.

* **Policy was hiding in the prompt.** The rules called non-negotiable lived in AI instructions and contradicted the documents they cited.
* **Authority is not relevance.** The most similar passage is not the one that controls; the system has to decide that from metadata, not search rank.
* **The cleanup builds the onboarding.** Every rule pulled out of an SOP becomes both a validation check and an interview question for the next customer.
* **Your document numbering was a product spec.** Naming SOPs after documents, not processes, handed the workbench about 99 document types for free.
