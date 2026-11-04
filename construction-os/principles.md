> **Synced from Claude Docs. Edit there, not here.**
> Source: [Principles](https://claude.ai/artifact/5cYmZCVFyZYrdjFeor3uRy) · doc revision 42 · synced 2026-11-04

# Construction OS — Principles

Nov 3, 2026 · @Justin

The rules for building a great construction document set and great generated documents, each one learned from a real mistake in this build. Living doc: add a row whenever a review teaches something.

## How to use this doc

Ten universal principles, each with three layers under it: the rules that follow from it, the incidents in this build that taught it, and where it's enforced. A rule belongs under exactly one principle; a lesson is evidence, not a principle of its own.

- **Add to it** whenever a review, a failed test or a PM's reaction teaches something: find the principle it serves, then add the rule or the incident.
- **A new principle is rare.** If a lesson doesn't fit any of the ten, that's worth a conversation.
- **Decisions stay in the System Design decision log;** the Build Log holds the story. This doc holds what they taught.

## The ten principles

### 1. Every document declares what it is

Before anyone reads a word of the body, a document answers five questions about itself: what it is, what it controls, when it applies, whether it's in force, and whose it is. Identity comes before content.

**Rules that follow:**

- **What is it?** Its function: one of nine types, because each is used differently. A policy is enforced, a procedure is followed, a definition is generated from, a guide explains, an example is copied for style only. It has a permanent ID that is never reused; a citation is that ID plus a numbered section.
- **What does it control?** Its authority domain and the specific decisions it governs. *Open gap:* no front matter field declares this yet, so authority is traced indirectly through POL-01 rule IDs and definition dependencies. A `governs` field listing the rule or decision IDs a document controls is planned.
- **When does it apply?** `applies_to`: stage now; project type, contract type, work type and jurisdiction next. Stage boosts retrieval and never filters it.
- **Is it in force?** Lifecycle status (draft, approved, superseded, retired), version and effective date. The version lives in front matter only.
- **Whose is it?** Layer says where the knowledge came from: starter core, jurisdiction or company. Provenance records the source and when it was adopted. In a company's copy, history against the starter release shows what the company changed since the fork.
- Every document also names its owner: a role, never a person.

**Learned from:** version stamps in 139 document bodies contradicted their front matter; 2,526 old references like "#51" pointed at nothing (and GitHub turned them into links to pull requests); the old cross-reference index matched none of the current files.

**Enforced by:** front matter validation; ID checks; body stamps removed; references rewritten to IDs.

### 2. One decision, one source

Every business decision (a limit, a deadline, a required signature, a rate) is stated in exactly one place. Everything else cites it or renders it, never copies it.

**Rules that follow:**

- Rules have permanent IDs, separate from the documents that carry them out.
- Values live in structured configuration, rendered where they're shown and cited everywhere else.
- The control owner sets the control; the procedure owns the steps.
- Firm-wide timing is policy; process timing is procedure.

**Learned from:** the 10 core rules lived in five documents and an AI prompt, drifting apart; 47 report rows were nothing but restated rules; the carpenter rate was $89 in one source and $90 in another, so two systems priced the same change $7.26 apart; FCM and PM procedures set different deadlines for the same step.

**Enforced by:** POL-01; the registry and company config; the restated-value check; Decision 3 (FCM owns the control).

### 3. Authority is explicit, contextual and never inferred from retrieval

Which source governs depends on the decision being made and the situation it applies to, and it never comes from which paragraph ranked highest in a search. Different sources often govern different decisions: a contract sets what the client owes, while policy sets what the PM may do.

**The hierarchy of authority, for when two sources govern the same decision,** highest first. Each level must comply with every level above it.

| Level | What it is | Where it lives | Can a company change it? |
| --- | --- | --- | --- |
| 1. Law and regulation | Statutes, codes, licensing and consumer-protection rules | Jurisdiction layer (e.g. Massachusetts) | No: locked, or a constraint company values must stay within |
| 2. Executed contract | The signed agreement for one project | Supplied with the request; never stored as company knowledge | Only by amending the contract; it governs what the client is owed for that project |
| 3. Policy | What must always be true, and who has authority (POL-01 rules) | Core defaults, company values | Yes, within law; the Policy Owner decides |
| 4. Controls, procedures and definitions | The controls a policy requires (FCM), who does what and when (CHG, BIL, SUB and other SOPs), and what a document must contain (definitions and templates) | Core, company values and overrides | Yes, within policy |

**No authority at all:** guides explain, reference examples show style, navigation maps the library, and system instructions describe how the AI behaves. None of them can be cited as a rule, and none of them can override anything above.

**Within a level:** a company's value beats the core default (that's the point of configuring it), but never escapes the constraints of a level above it. Two sources at the same level that disagree are a conflict to flag, not a tie for search to break.

**Inside level 4, nothing outranks anything wholesale; each decision has one owner** (Decision 3). The FCM document owns the control (thresholds, approvals, required backup, control deadlines); the procedure owns the steps and cites the control; the definition requires what the procedure says a document must contain. When two of them disagree, one gets fixed.

**Rules that follow:**

- The order is law, then the executed contract, then policy, then procedure. The contract governs what the client pays; policy still governs how the company behaves.
- Conflicts are flagged and decided by a person, never silently resolved.
- Retrieval finds; it never decides. Mandatory rules are loaded by ID from the document's definition.
- Navigation documents map the library and are never evidence; examples teach style and are never facts; system instructions describe behavior and never state policy.
- Locked rules (safety, law) can't be configured away.
- Sources that govern different decisions are read together; different requirements aren't automatically a conflict. A real conflict is flagged.

**Learned from:** the core rules were "non-negotiable" but lived only in an AI prompt; policy accepted a signed PCO while BHI's own contract recognized only a change order; the old system's PCO said "Markup per the Contract" when no contract states one.

**Enforced by:** SYS-00 4.3 and 4.4; definitions with declared dependencies; applies\_when conditions; the publish finding when a contract doesn't recognize the policy's accepted forms; document types.

### 4. One document, one job

Each document does one kind of work, and its structure matches that work. A document that is half policy, half procedure and half form can't be maintained, cited or generated from.

**Rules that follow:**

- Sort every requirement sentence by sentence: policy (what must be true, who has authority), procedure (when, who, in what order) or definition (what a document must contain). Tiebreaker: if changing it needs the Policy Owner, it's policy.
- What a document must contain is a definition, kept separate from the procedure that produces it.
- Templates hold the approved fixed language; it's written once, not regenerated.
- Sections are numbered so they can be cited.
- Plain language, one requirement per sentence, acronyms only from a glossary.

**Learned from:** CHG-53 mixed the PCO procedure with what a PCO must contain, and the PCO's content was spread across 13 documents; receipts and time entry were each two rules squeezed into one slogan; 26 procedures are named like the forms they produce.

**Enforced by:** the nine document types; definitions (CHG-53-DEF); the template; SYS-00 3.1 and 6.3.

### 5. Write for two readers

People reason in prose; machines decide from structure. Every document serves both, and each kind of content goes in the form its main reader needs.

**Rules that follow:**

- Structured data (YAML) for what a machine decides: values, the registry, definitions, dependencies.
- Prose for what a person needs to understand: purpose, steps, judgment.
- Dependencies are declared with the conditions they apply under and who they're for (client-facing or internal).
- IDs tell the system which document; labels tell the person what it is. Keep both.
- Front matter is metadata for both: people scan it, retrieval filters and ranks on it.
- Tools check structure; people check meaning.

Different work needs different mechanisms: retrieval finds relevant context; declared dependencies identify required knowledge; the LLM interprets and drafts; code calculates and checks structure; templates control the final format. Not everything is RAG, and not everything is a prompt.

**Learned from:** rates written into sentences couldn't be configured or validated, which surfaced 249 configurable values hiding in prose; a cleanup stripped "PCO" from "PCO CHG-53" and made lines unreadable to a PM.

**Enforced by:** the registry, company config and definitions in YAML; the validator; writing guidance; reviews of meaning in pull requests.

### 6. Separate reusable foundations from company-specific knowledge

Each company gets a complete copy of the starter library, tailored to how it works and maintained as its own. The shared application evolves independently of every company's knowledge.

**Rules that follow:**

- Core, jurisdiction and company label where knowledge came from and where it applies; they don't require a runtime that merges layers. Company values live in one configuration; the application holds no company content.
- Not everything configurable is a value: parameters for values, module switches for business-model choices, company overrides for a process that differs in structure.
- A rule covers only what it covers; don't stretch it to things it doesn't govern.
- Legal requirements are locked or constrained, never preferences.
- The product ships a reusable pricing capability; the company's pricing method, rates, price history and contracts are its own.

**Learned from:** BHI's identity and Boston market language sat in core documents; SYS-09's pricing was one company's Boston condo data; an AI fix banned email for allowance selections that aren't changes; BHI sample drafts slipped into the application repository.

**Enforced by:** the layer field; the company folder; the app test that fails on company names; the three configuration mechanisms; the pricing evidence interface.

### 7. Every change is deliberate, reviewed and traceable

Nothing changes silently and nothing is lost. Anyone can answer who changed what, when, why, and what it said before.

**Rules that follow:**

- Freeze before cleaning: the original is preserved before any fix.
- Every change is a branch and a pull request; the approval is the audit record.
- A change that alters a requirement is marked as one, distinct from a wording change (here: major versus minor version), and records when it takes effect.
- Nothing is deleted: superseded and retired documents move to the archive.
- Mechanical changes are kept apart from content changes and verified by a check, not by reading.
- Reports are dated baselines; issues track the fixes.
- Content needing legal review is marked, and the mark gates distribution.
- One working copy per document; snapshots are dated, and the authoritative version wins, which isn't always the newest copy.

**Learned from:** tagging the raw corpus first made every later fix reversible; 2,526 reference rewrites could only be trusted with a line check; a note about a repository that never existed misled planning twice; two sessions on the same project left one always out of date.

**Enforced by:** the v0-raw tag; CLAUDE.md rules; the scope check and its allow list; GitHub issues; design snapshots and "Before planning".

### 8. Never invent

A generated document states what's known, labels what's estimated and why, marks what's missing, and asks what a seasoned professional would ask. Estimating eight hours of carpentry from a documented basis is the job; presenting it as fact, or inventing a signature or a source, is the failure.

**Rules that follow:**

- Never cite a source that doesn't say it.
- Code does the arithmetic; AI proposes quantities and wording.
- Every number shows its basis: a quote, hours times a rate, a contract clause.
- Never fabricate facts, sources or approvals. Estimates and assumptions are allowed when they're labeled as such and have a defensible basis. Unknown facts are blanks; questions for the PM never go to the client.
- Always propose the protective language a PM would add (exclusions, permit questions), for the PM to confirm.
- Authorization names exactly who authorizes.
- A draft is never blocked; its flags travel with it.
- Marketing stays off contract documents.

**Learned from:** the old system's PCO cited "Markup per the Contract"; the first new draft put "Who is the client?" at the top of page 1 and left exclusions blank; neither draft asked whether six new lights needed an electrical permit until a review did.

**Enforced by:** the pricing engine; the PM checklist file; the clarifications and exclusions section with prompts by trade; the permit check; fixed terms in the template.

### 9. Judge the work by how much it reduces the work

The test is whether the output materially reduces the work of producing a correct, usable document. A draft that saves a PM two hours and needs fifteen minutes of review is a success. Retrieval scores and polish are proxies; completeness, correctness, unsupported claims, revisions needed and time saved are the measures.

**Rules that follow:**

- Write the test before the system, with exact answers where there is one.
- Decide who it's for and what it replaces before designing how it works.
- Build one thing end to end before widening.
- Start from how the work is really done, not from what the documents say.
- AI reviewers over-call, and AI fixes go one step too far: someone who knows the work reads the hard rows.

Validation depth must match actual capability: a document that only had general drafting checks is never presented as thoroughly validated.

**Learned from:** the eval questions exposed the documents before any code ran; four days of governance work without a stated customer nearly led into a hole; of three "most serious" findings, one was real, one misclassified and one not a conflict; the pricing method came from asking how Justin actually priced change orders.

**Enforced by:** acceptance tests graded on documents and time saved; the Product Brief; the vertical slice; review of every content PR.

### 10. Keep knowledge, request context and generated output separate

Governed knowledge, the evidence supplied for one request, and the documents the system generates serve different purposes. Keep them apart, and never promote one into another without an explicit decision.

| Kind | Example | How it's treated |
| --- | --- | --- |
| Governed knowledge | Change order policy, contract templates, pricing rules | Maintained and versioned as the company's authority |
| Request context | An executed project contract, PM notes, a subcontractor quote | Used for that request only; never absorbed into company knowledge |
| Generated output | A PCO drafted by the system | A draft artifact; never a source of policy or pricing unless deliberately reviewed and ingested |

**Rules that follow:**

- A term in a supplied contract applies to that request; it never changes the company's standard.
- Uploaded documents are never indexed into the company's library or reused across requests.
- Generated drafts don't feed future pricing or policy without a deliberate review and ingestion step.

**Learned from:** Test 4's contract set 8% overhead and 5% profit; the system must price that PCO at 13%, and must not learn that the company's markup is 13%. The design kept request inputs ephemeral from the first day of the System Design.

**Enforced by:** request inputs never indexed (technical design section 8); onboarding extraction as the only reviewed route from documents into company data; the package as the only source of governed knowledge.

## How Git and GitHub make it a real corpus

A folder of documents isn't a corpus until every change to it is deliberate, reviewed and recoverable. Git gives the documents the discipline that code already has: history, review, versions and a way to undo. Most of principle 7 is enforced here, and parts of 2 and 6.

| Feature | What it does for us | Where we use it |
| --- | --- | --- |
| Plain text in a repository | Every document is Markdown or YAML, so a change is a readable line-by-line diff instead of an opaque file swap | All 173 documents, the registry, company config, definitions |
| Tags | A permanent, named snapshot to return to | `v0-raw` froze the original corpus before any cleanup, so every later fix is reversible |
| Branches | Work happens apart from the approved version, so nothing half-done reaches main | One branch per change |
| Pull requests | The approval is the audit record: what changed, why, who reviewed it, when | Every change; CLAUDE.md forbids committing to main |
| Automated checks on a PR | Mechanical changes are verified by a check, not by reading 2,526 lines | The line check, `scope_check.py` and its allow list, the validator |
| Issues | Findings become tracked work with an owner, not rows lost in a report | Reports are dated baselines; issues track the fixes (attorney packet #30, co-sign alignment #57, billing #25) |
| History, diff and blame | Anyone can answer who changed a line, when, why and what it said before | Traceability for any requirement; history is never rewritten |
| Separate repositories | Company knowledge and the application evolve independently, with different access | `construction-os-corpus` (the company's package) and `construction-os` (the app, no company content) |
| A copy per company, with a recorded fork point | Each company owns and edits its own library; the starter release it came from is known, so later releases can be compared and adopted selectively | `STARTER_RELEASE` in each company's copy |
| Private repositories and ignored files | Company content and secrets stay out of reach | Private repos; API keys only in `.env`, never committed |

**Planned:** versioned tags for each published runtime package, so every generated document can name the exact corpus version it drew from; required checks that block a merge when the PCO path fails.

**Learned from:** GitHub turned 2,526 old "#51" references into links to unrelated pull requests, which is why references became document IDs; a note about a repository that never existed misled planning twice, while the repositories themselves were never wrong.

## For the article

The article's thesis is already in the Build Log: a RAG project is a document-quality project wearing a code costume. The full argument is broader: trustworthy AI needs organizational knowledge that can be identified, governed, retrieved, interpreted and reliably used. This doc gives it a spine, but the principles tell a stronger story grouped than one per chapter: representing knowledge (1, 4, 5), authority and consistency (2, 3), customization and governance (6, 7), generation and evaluation (8, 9, 10).

- **Long-form piece:** each chapter is one group of principles, opened with the incident that taught it and closed with how it's enforced. The universal principle is what readers take away; the construction story is what makes it believable.
- **Posts:** one principle or one incident is one post. The incident is the hook, the principle is the point, the enforcement is the takeaway.
- **Evidence:** the Build Log has the numbers (171 documents, 2,526 references, 432 report rows, 4 of 5 spot-checked rows real); the two PCO drafts are the before and after.

At the end of the build: reread this doc and the Build Log together, outline from the four groups, using the strongest incident in each.
