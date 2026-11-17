> **Synced from Claude Docs. Edit there, not here.**
> Source: [System Design](https://claude.ai/artifact/3iEBRhf5uJpBXwf8TsCjG4) · doc revision 81 · synced 2026-11-10

# Construction OS Document Workbench — System Design

Oct 31, 2026 · @Justin

The document workbench lets a construction company understand its own policy and generate the documents its processes require, from governed knowledge plus information the user supplies. This is the living design record: decisions are recorded as they're made.

## 1. Scope and boundaries

The workbench is a **governed, AI-powered construction document-generation system**. It does not manage projects, track status, keep project histories, or act as a system of record. Those are separate systems to be built later.

**Three boundaries:**

- **Knowledge vs. outputs.** The system holds governed knowledge: policies, procedures, definitions, examples. A generated document, such as a finished PCO, is an output. Outputs never flow back into the governed library.
- **Knowledge vs. request input.** Information a user supplies for one request (notes, a sub's quote, a drawing) is used for that request only. It is never indexed or stored as governed knowledge, and one company's input never reaches another request. **Request input is ephemeral.**
- **Future project system.** It will plug into the same input slot and supply facts automatically, without changing the generation engine.

| In scope now | Deferred |
| --- | --- |
| Governance model and document hierarchy | Project database |
| Core, jurisdiction, and company knowledge layers | Project history and status tracking |
| Markdown corpus under version control | Project financial tracking |
| Policies, procedures, and document definitions | Persistent project records |
| Retrieval and source selection | Automated project synchronization |
| Document generation, validation, and export | Long-term repository of issued documents |
| Company configuration and onboarding | Project dashboards |

## 2. Knowledge model

Every governed document, and eventually every rule, answers five questions. Authority is not relevance: a binding policy should only shape a document it actually applies to.

| Question | Dimension | Status |
| --- | --- | --- |
| What is it? | Function (document type) | Decided |
| What does it control? | Authority domain | Partly decided (conflict handling); filled per domain |
| When does it apply? | Applicability: project type, contract type, stage, jurisdiction, party | Partly decided (work type for time entry and billing); full list per domain |
| Is it in force? | Lifecycle: draft, approved, superseded, retired, effective date | Decided |
| Whose is it? | Layer: core, jurisdiction, company | Decided |

### Document types

Eight types. They describe what is inside the system, not what it produces.

| Type | What it is | How generation uses it | Examples |
| --- | --- | --- | --- |
| Policy | What must always be true, and who has authority | Retrieved as evidence; rules enforced by validation | Core rules, EXEC-01, FCM-19, SYS-03 |
| Procedure | When and how a document is created, reviewed, or issued | Retrieved as evidence | FCM-03, process steps in CHG-53 |
| Document definition | What a document needs and must contain | Loaded directly by ID | SUB-A06, PRE-01t, template parts inside SOPs |
| Work instruction | How to do a step in a specific tool | Retrieved when the user asks how | WF-01, WF-02 (Procore) |
| Guide | Training and explanation | Retrieved for questions, not generation | SUB-T01, SYS-08 |
| Reference example | A sample of good output | Guides style only; never supplies facts or overrides rules | None yet |
| Navigation | Maps of the system | Not searched as evidence | SYS-01, SYS-04, STG-A to E |
| AI configuration | How the engine behaves toward policy | Not searched; enforces policy, never originates it | SYS-05, SYS-06, SYS-07 |

## 3. Document definitions

Each document type the workbench generates gets its own definition file. The SOP references it, and existing document IDs are kept. Generation loads the definition directly instead of hoping retrieval finds it.

The corpus already supports this: most SOPs are named after a document (CHG-53 is the PCO, FLD-39 the Daily Report, RFI-44 the RFI, CLO-88 the Certificate of Substantial Completion), giving about 99 document types today. Each SOP currently mixes procedure and definition; the definition part moves into its own file.

**A definition declares:**

- **Inputs:** required and optional fields, and what to ask when one is missing. Every request for a document type goes through the same intake, so every output is equally complete. This is also the slot the future project system fills.
- **Structure:** sections in order, and which are required
- **Required language:** clauses that must appear word for word
- **Approvals:** signature blocks and the role that signs
- **Validation:** checks run before output, referencing rule IDs rather than restating thresholds
- **Output format:** letterhead, branding, file type

### The policy / procedure / definition boundary

SOPs mix all three, so sorting happens at the sentence level, not the document level. Each requirement answers exactly one question.

| Type | The question it answers | Example |
| --- | --- | --- |
| Policy | What must always be true, and who has authority? | "No work proceeds without written authorization" (core rule 1) |
| Procedure | When, who, in what order? | "Issue the PCO after the Change Event is logged, then route it to the owner" |
| Definition | What must the document contain? | "Every PCO states description, cause, cost impact, schedule impact" (CHG-53 §2) |

**Tiebreaker:** would changing it require management approval? If yes, it is policy. If it is how a PM carries out the work, it is procedure.

**Timing rules:** firm-wide, non-negotiable timing (time entry, receipts) is policy. Process-specific timing ("file minutes within 48 hours") is procedure.

**Worked example, CHG-54 §9.3:** stop and notify when T&M work reaches 75% of the not-to-exceed amount. The 75% threshold is policy with a rule ID. The steps (stop, notify, re-authorize) are procedure. The CCD definition references the rule ID in its validation. Thresholds and time limits hiding inside procedures are the most common pattern in the corpus.

## 4. Layers, ownership, and overrides

**Policy is owned by the company.** For BHI that is Justin; for a customer, the person the company designates as **Policy Owner**. What Construction OS ships is a default the company adopts or changes, not the company's policy until adopted.

**Core ships opinionated defaults.** The product works with no configuration on day one, using best-practice values (BHI's as the starting point).

| Layer | Maintained by | Holds |
| --- | --- | --- |
| Core | Construction OS (vendor) | Default policies, procedures, definitions |
| Jurisdiction | Construction OS (vendor) | State-specific requirements, e.g. Massachusetts HIC terms and lien law. Tagged now, built as a layer later. |
| Company | The company's Policy Owner | Adopted defaults plus the company's changes |

At generation time the system resolves **company, then jurisdiction, then core.** The current corpus is mostly core-quality content with BHI-specific pieces (brand, letterhead, some Massachusetts terms) mixed in; BHI becomes the first company layer.

### Rules and overrides

Rules become objects with stable IDs. Companies override **at the rule level, not the document level**: BHI changes one parameter, not its own copy of FCM-11.

- Core: `TIME-ENTRY-001` max delay = 48 hours
- BHI: `TIME-ENTRY-001` max delay = next day 9 AM

Every document that references the rule picks up the company's value.

| Kind of rule | Overridable? | Examples |
| --- | --- | --- |
| Parameters | Yes | Thresholds, time limits, approvers, reminder schedules |
| Process choices | Yes, with a warning | Skipping an optional review step |
| Legal requirements | No, locked | Massachusetts HIC contract terms, statutory lien waiver language |
| Structural requirements | Only by vendor change | Removing a required section from a definition |

### Roles

Rules reference **roles, not people**. The company profile maps each role to a person, so the core library stays generic and a company can reassign a role without touching any rule. Example: APPROVAL-SPEND sets limits by role (Superintendent, Project Manager, Executive), and each company maps those roles to people.

## 5. Company configuration profile

A company configures the workbench by answering the decisions its policies require, through an AI interview or a fillable document it uploads. Both are **generated from the rule registry**, never written by hand, so adding a rule automatically adds its question to onboarding.

**Each overridable rule carries:**

| Field | Example |
| --- | --- |
| Rule ID | `TIME-ENTRY-001` |
| Plain-language question | "How soon after a shift must crew enter their time?" |
| Default | 48 hours |
| Allowed values | 24 hours, next day 9 AM, 48 hours, 72 hours |
| Why it matters | "Late entries break job cost reporting and certified payroll" |
| Overridable | Yes / with warning / locked |
| Jurisdiction | Any / MA |

**The interview:**

1. Company identity: name, license numbers, letterhead, and who fills each role
2. Policy decisions, one business area at a time (money, changes, subcontractors, schedule, safety, closeout), with every default shown
3. The owner may accept all defaults for an area, but must confirm explicitly
4. Locked rules are shown, not asked: "Massachusetts requires these contract terms"
5. The Policy Owner signs off; the profile is versioned and every later change is logged

The answers become the company profile file, the company layer the generator reads at runtime.

**Consequence for the corpus cleanup:** every rule extracted from an SOP feeds both validation and onboarding. Extracting CHG-54's 75% rule also writes its interview question. The cleanup builds the onboarding product.

## 6. Quality assurance

Every relationship between documents is checked, but only where something changed. A full pass happens once per domain, when that domain is first governed; after that, a change triggers checks on the changed document and everything it links to. The links in front matter (carried out by, definition, controls) are what make targeted checking possible.

### 6.1 Consistency checks

| Relationship | The question | How it is checked |
| --- | --- | --- |
| Policy to procedure | Does the procedure actually carry out the rule? | AI-assisted review; Policy Owner approves |
| Procedure to definition | Does the definition require what the procedure says the document must contain? | AI-assisted review |
| Definition to rule | Does every rule ID in its validation exist? | Automatic |
| Any document to rule value | Does it copy a rule's value instead of referencing the rule? | Automatic |
| Form or template to definition | Does the Word form have the fields the definition requires? | AI-assisted review |
| Navigation to library | Does the index list only documents that exist, with current titles? | Automatic |
| System instruction to policy | Does a prompt state policy itself? | AI-assisted review |
| Any document | Front matter complete, IDs unique, statuses valid, no unresolved same-layer conflict | Automatic |

Automatic checks run on every pull request and block the merge when they fail. AI-assisted reviews produce a report, quoted word for word against the sources, that is approved as part of the pull request. The first instance is the POL-01 verification on pull request #1.

### 6.2 Company acceptance testing

Before a company goes live, and again whenever its configuration or the core library changes, a suite runs against that company's configuration. The result is a readiness report the Policy Owner signs off.

| Test | What it confirms |
| --- | --- |
| Configuration completeness | Every required decision is answered, values are within allowed ranges, every role is mapped to a person |
| Override safety | No company value overrides a locked or jurisdiction rule; no override leaves an unresolved conflict |
| Consistency checks | The checks in 6.1, run with the company's layer applied |
| Retrieval evaluation | Policy questions return the right document and section, using the company's values |
| Generation evaluation | Generated documents follow the company's rules, for example a $12,000 commitment requires an Executive; missing facts are asked for; conflicts are flagged |
| Output rendering | Letterhead, branding, naming, and file format are the company's |
| Regression | Results match the previous approved run, apart from intended changes |

### 6.3 When each runs

| Trigger | What runs |
| --- | --- |
| Any pull request | Automatic checks |
| A document or anything it links to changes | AI-assisted reviews for that document |
| A domain is first governed | Full consistency pass for that domain |
| A company is configured or changes its configuration | Company acceptance suite |
| A core release | Company acceptance suite for every company, as regression |

## 7. Not yet designed

In the order we plan to take them:

- [ ] **Authority domains:** what each document and rule controls (`controls` field), and how conflicts are handled. Conflict handling is decided (the Executive resolves; the system flags and does not finalize). The controls field is filled domain by domain, seeded from SYS-04's FCM table.
- [ ] **Applicability:** the `applies_to` dimensions and their allowed values
- [x] **Lifecycle:** decided (see decision log, change control)
- [ ] **Rule registry:** partly decided: firm-wide rules live in POL-01 with permanent IDs; each value has one source that documents reference or render. Domain rules and the registry format come with each slice.
- [x] **Front matter standard:** decided (see decision log, document standards)
- [ ] **Repository structure:** folders, collections, and how core, jurisdiction, and company layers are stored
- [ ] **Retrieval and authority resolution:** exact ID lookup, metadata filtering, hybrid search, and selecting what controls (retrieval rank is not authority rank)
- [ ] **Generation pipeline:** identify the document type, load the definition, gather inputs, retrieve rules, resolve, generate, validate, render
- [ ] **Validation and enforcement:** which rules are checked in code
- [ ] **Evaluation:** retrieval eval (exists) and generation eval scenarios; consistency-check tool and company acceptance suite designed in section 6, not yet built
- [x] **Roles list:** decided: Executive, Project Manager, Superintendent, Accounting; "Owner" means the client
- [ ] **Company contracts:** raised 2026-11-01. Contracts are likely company-specific by default (own MSA, AIA or ConsensusDocs forms, attorney's paper), so SYS-00 §5.3's "replacing a whole document is rare" doesn't hold for them. Direction: core contracts become a starter set for companies with none; a company's own contracts load at the company layer; onboarding asks "Do you have your own contract forms?"; checking a company's contracts against its configured policy becomes a workbench feature (the remediation report, productized). Open question: shrink the attorney packet to the jurisdiction layer plus the core clauses starter-set users rely on most, before paying for review.

**First vertical slice:** change orders (CHG-51 to 60, FCM-03, FCM-19, SUB-02, SUB-A06/A07, relevant CON-12/13 clauses), built end to end before other domains.

### Configuration architecture (direction adopted Nov 2; decisions pending the inventory)

Three kinds of knowledge, each with one job:

| Kind | Owns | How the workbench uses it |
| --- | --- | --- |
| Governing documents | The obligation, its circumstances, and who has authority | Retrieved, or loaded by ID |
| Registry | Each configurable item's identity, type, default, permitted range, override constraints, owning document and section, and onboarding question | Exact lookup; never searched |
| Company configuration | One company's chosen values, identity, role-to-person mapping, brand kit | Exact lookup; versioned and signed off by the Policy Owner |

The registry never defines what a value means or when it applies; the governing rule does. Registry entries carry a kind: parameter, identity, or role\_mapping.

**Update Nov 2 (recommended architecture adopted, see decision log):** decision 3 becomes the publish step; decision 4 becomes one repository per customer, with layer kept as metadata; decision 7 is deferred, with jurisdiction requirements checked at publish time; decision 9 becomes one package and index per customer; decision 10 becomes a second customer fork. Decisions 1, 2, 5, 6, 8, 11, 12 and 13 stand.

Decisions, with the outside review's position:

- [ ] **1. Three-kinds model.** Approve, separating governing-rule meaning from parameter definitions.
- [ ] **2. Registry in YAML.** Approve: stable IDs, typed values, applicability, constraints, ownership. Schema frozen only after the inventory shows the real range of types (durations, money, percentages, approval matrices by role, conditional values by contract or work type, identity, clause selections, jurisdiction constraints).
- [ ] **3. Cite versus render, through a compiler.** Procedures cite rule IDs; only the owning document and templates render values. A knowledge compiler (validate references, resolve values, apply constraints, assemble content) produces a readable company edition on demand and the runtime context for generation. Compiled output is never authoritative or edited.
- [ ] **4. Folders follow layers.** docs/ core, jurisdictions/\<state>/, company/\<slug>/; supports release packaging. SYS-06, SYS-10 and SYS-11 move to company/bhi/.
- [ ] **5. Jurisdiction content.** Clause modules where a clause is whole; not every Massachusetts sentence becomes a fragment.
- [ ] **6. Structured document definitions.** Loaded directly; declare their rule dependencies, so mandatory rules are resolved by ID from the definition, not found by search.
- [ ] **7. Constraint-aware resolution.** Replaces "company, then jurisdiction, then core": core defines purpose, default and whether customization is allowed; jurisdiction sets constraints (lock, minimum, maximum, required clause, prohibition); company applies only permitted values. Legal constraints come from reviewed configuration, never inferred by an LLM. Whole-document overrides remain for company contracts.
- [ ] **8. Audit and provenance.** Company configuration changes are versioned with who, when, old and new value, and approval. Generated documents carry a short client-facing generation reference; a separate internal manifest (core release, configuration version, definition and template versions, effective rule values, jurisdiction module versions, warnings) is exported with the document, since the workbench keeps no project records.
- [ ] **9. Retrieval.** Shared index for core; filtered shared index or direct lookup for jurisdiction; tenant-isolated retrieval for company documents; exact lookup for rules and parameters; direct loading for definitions, templates and brand assets. A user from one company can never retrieve another company's content.
- [ ] **10. Test tenants.** A fictional second Massachusetts contractor first (different limits, roles, contract forms, placeholder brand that deliberately fails the brand-kit readiness check); New Hampshire later as a negative test (the system refuses to assume Massachusetts legal content applies).
- [ ] **11. Three configuration mechanisms, not one** (raised Nov 2 from the customization taxonomy). Parameters for values; module switches for business-model choices (self-performs or not, contract types used, Procore or not); company procedure overrides where a company's process differs in structure, not value. Treating structure as parameters produces a document that's filled in correctly but describes how someone else works. Onboarding by extraction proposes an override where a company's procedure differs structurally.
- [ ] **12. Roles can be missing, not only renamed.** Role mapping needs a fallback chain (no Superintendent, then the Project Manager) and allows one person in several roles, or approvals break for small firms.
- [ ] **13. Every configurable item names the role that approves changing it** (Policy Owner, Accounting, or Product Owner for core), since nothing says who sets procedure-level values today.

Not now: a configuration-management application, a project database, or a generated-document repository. Git-managed configuration and pull-request approval are enough for the first implementation.

## 8. Decision log

Newest first.

| Date | Decision |
| --- | --- |
| Nov 10, 2026 | Pricing in a draft is a suggestion; the PM decides every price, and a human is always in the loop on pricing (Justin's practice). The aim of AI pricing is a complete, traceable structure the PM can correct quickly, not the right number: every line shows its source (rate table, cost history, quote, the PM, or labeled estimate), and general conditions appear as hours and days at rate so the PM can cut them. Found reviewing the old system's cedar closet PCO (about $54,500), which was high mainly because it carried a full-time PM and site super the job doesn't need. Drafts are revised iteratively: the PM reviews a version and gives feedback in plain words, and the app produces the next version in the same project folder, with the feedback saved as an input and a change summary. An amount the PM gives is a sourced amount; code still computes every total; lines the feedback doesn't mention stay unchanged; feedback that conflicts with company policy is flagged and policy holds. Also adopted Nov 10 from the comparison with that PCO: its layout and organization (branded first page, description with work bullets, grouped assumptions with job-specific exclusions, side-by-side signatures), with all of our correctness rules kept, and pricing presentation as a company setting, PRICING-PRESENTATION (by\_division, flat or summary\_only; BHI uses by\_division), because some contractors want pricing broken down by division. Build order (revised the same day): layout v2 (step 5a), then estimating from cost history (5c), then the revision loop (5b), so the PM's first review is of a fully estimated draft rather than one with blank quantities. The document-workbench repository stays public: without a company's private package it does nothing, and the rule that it holds no company content (names, rates, clause text, client data, fixtures built from real projects) stays enforced by its test and by review, because it is also what lets a second company use the same code. |
| Nov 9, 2026 | A PCO goes to the Owner as a standalone document. Pricing backup (subcontractor and vendor quotes, takeoffs, T&M logs) and the Owner's request correspondence stay internal, on file in the job folder; the PM checklist confirms the backup is on file, and nothing is listed as an Owner exhibit unless it is meant for the Owner, such as a layout or drawing. This holds on cost-plus work too: there the Owner receives cost backup (receipts and invoices) monthly with billing, not with each PCO (Justin's practice). Contract type does change pricing and billing (the contract's fee instead of company markup, limits on subcontract markup, cost backup with each billing), so contract type becomes a project fact set from the executed contract in build step 6; until then PCO pricing assumes fixed price. A contract that explicitly requires backup with a change remains a contract term for step 6. Resolves an ambiguity in CHG-53, which says both "attach backup" and "vendor quotes are backup only"; found when the first live drafts listed the quotes as Owner exhibits. Also adopted with the PCO polish (Nov 9): the PCO uses "Owner", the defined term in CON-13 and SYS-00, never "Client"; the company's standard clarification language (concealed conditions, limited finish, upgrades, permits, hazardous materials) lives in CHG-53-DEF and is used verbatim, pending attorney review (issue #30). The PCO is written as a letter from the Contractor to the Owner, in the contract's defined terms; internal details (who performs the work, how it was estimated, quotes) stay off it and go on the PM checklist. Owner selections are not described in the PCO: it references the Owner Selection Sheet (PRO-34) by selection ID, approved or issued with the PCO for signature. |
| Nov 8, 2026 | Request information becomes project context. Inputs supplied for a project (notes, quotes, drawings, an executed contract) and the drafts generated for it may be reused across that project's work, for example the contract supplied for a PCO is used again for the PCCO that follows. Project context never reaches another project, never changes the company's configuration, and never enters the governed library without a deliberate review. Replaces "used for that request only" (Oct 31 scope decision; PCO technical design section 8). Recorded in SYS-00 3.0 section 1.3, which also adopts: drafts are produced even with conflicts, flagged for the PM to resolve; one copy of the library per company with layers as labels; checks listed as running today versus planned; the planned front matter field named governs. |
| Nov 4, 2026 | Design docs get their own private repository, construction-os-design, set up for several projects; the Construction OS docs live in their own folder. The Claude Docs stay the working copy; the repository is the reviewed, versioned record. Changes flow one way: edit the Claude Doc, then sync an export to the repository in a pull request whenever a doc changes in a way that matters. Repository copies are never edited by hand; each file links to its source doc, and a sync manifest records the revision synced. Product design docs leave the corpus because the corpus is one company's package and the template every company copy is forked from; design/ in the corpus moves out in a later PR. Replaces the Nov 1 arrangement of snapshots in the corpus's design/ folder. |
| Nov 2, 2026 | Clients see the markup, itemized by component (BHI default; configurable per company and per component, and a contract can require a specific breakdown). The Executive always co-signs before the client signs: added to POL-01 AUTH-WRITTEN as a rule value (default before the client; configurable), making POL-01 version 3.0. BHI's HIC and CSL numbers are placeholders in the profile until real ones are entered; anything generated with them is marked as such. Allowance selections: a selection within the allowance is not a PCO, but the variance (up or down) is captured as a change event (CHG-51 10.1) and reconciled per the contract (CON-17 10.3: pay application credit or credit change order). Acceptance Test 5 expects this. |
| Nov 2, 2026 | PCO pricing defaults set (BHI follows them; each configurable per company): general conditions added only when a change extends the duration by more than 10%, matching CON-13; the 1% application fee applies to every change order; actual permit fees pass through as their own line after markup, not marked up; billing and weekly rates from SYS-09's Labor Rates sheet (carpenter $90/hour, PM $2,664/week); PCO numbering PCO-001 onward per project, assigned by the PM; price validity 30 days. No past PCOs exist to copy, so the template is built from CHG-53-DEF and the family map's 29 definition items and judged by Justin. |
| Nov 2, 2026 | PCO slice design revised after an outside review. Pricing is modeled by cost category: each markup component names the categories it applies to, replacing yes/no flags. A pricing evidence interface returns rates and comparable prices with source, basis and date (v1: rate tables and supplied quotes; extracted history later). Clear, applicable contract terms are extracted before pricing and change the calculation, with the clause cited; ambiguous terms become visible assumptions (SYS-00 4.3: the contract governs what the client pays; policy governs internal conduct). Definition dependencies carry applies\_when conditions and an audience (client-facing or internal). Publishing blocks only on defects in the PCO generation path; everything else is a reported finding. Customer copies are changed directly; starter releases are adopted selectively, not merged automatically (supersedes the Nov 2 amendment's override documents; the one-file configuration stays). Build order starts with a real PCO, scenarios and the confirmed pricing values, then definition and schema, then template and renderer, before pricing code. BHI pricing values stay provisional until confirmed, including a conflict: Justin's practice adds general conditions for any extension, CON-13 only past 10% of duration. |
| Nov 2, 2026 | PCO slice technical design drafted (Claude Doc "PCO Slice — Technical Design"), pending Justin's review. No rag-system repository exists, so earlier references to it are superseded: the application starts in a new private repository, construction-os; construction-os-corpus becomes Beacon Hill Interiors' package, with a starter library split out when the second company arrives. Build order starts with the pricing engine (pure code, clear right answers). |
| Nov 2, 2026 | Change order pricing method (issue #58; from Justin's practice; settled except where noted). Order: every cost line (labor, materials, subcontractors, equipment, general conditions) goes into one subtotal; the company's markup structure applies once to that subtotal; the result is the total. Tax: a potential change order prices work not yet bought, so material estimates carry enough to cover sales tax; tax is not a separate line (configurable: separate line). Repeat-client discount: not part of the method; an optional configurable component. Self-performed labor: estimated hours × a billing rate (about $90 an hour for carpenters), not cost plus markup. Materials: what was paid, or an estimate if not yet bought. Subcontractors: the quote. Markup goes on everything, once, at the end: labor, materials and subcontractors together. Configurable later: whether markup applies on top of a billing rate that already carries overhead and profit, and whether subcontractor costs are marked up (contracts may limit it, as CON-16 does on cost-plus work). Markup structure is configurable as an ordered list of named components, each with a rate, a base, and whether it shows to the client: one company adds a flat 20%; Beacon Hill Interiors' practice was 1% application fee (the company's permit charge) + 10% overhead + 10% fee. This is a list parameter, not a single value. Still open: whether the 1% application fee applies to every change order or only to changes needing a permit. General conditions: every potential change order states how long it extends the job (resolving the CHG-53 "TBD" vs FCM-03 "calendar days" conflict in favor of always stating it, zero included); when it extends the job, time-based costs are added for the extension: PM, assistant PM and superintendent at their weekly rates, plus general conditions items such as dumpsters and temporary facilities. Practice varied; configurable later, including a threshold (CON-13 uses more than 10% of duration, Justin's practice was any extension). Still open: whether the 1% application fee applies to every change order or only when a permit is involved (a component condition), and how actual permit fees (SYS-09's 1.25% building permit) are passed through. |
| Nov 2, 2026 | Not-to-exceed checkpoints (from the PCO family map): notify the client at 70% of the not-to-exceed amount, with an estimate to complete; stop at 90% unless the client signs an increase. One standard for every Construction Change Directive and time-and-materials authorization, replacing CHG-54's 75% stop and CHG-60's 70–80% warning. A registry parameter in the potential change order slice (core default 70% and 90%), configurable per company later. Trade work on a client change (self-performed or subcontracted) does not start until the client's authorization under AUTH-WRITTEN, except under the emergency exception; FCM-14 7.1 is aligned in the fix list. Contract matches policy: CON-13 §2 is amended so a client-signed potential change order authorizes the work at the stated price, and the change order that follows updates the contract sum (attorney confirms the wording; Table 1 row 14 reopens). Which forms authorize work varies by company (AUTH-WRITTEN is configurable) and by contract, so the publish step checks that a company's contract recognizes every form its policy accepts, and the advisor flags any project contract that doesn't. |
| Nov 2, 2026 | Recommended architecture adopted, with one amendment. Each customer gets a complete, independently versioned copy of the starter library, customized at onboarding; that copy is authoritative for the customer. A publish step validates the customer's source corpus and produces a versioned runtime package (indexes, catalog, resolved configuration); runtime never reads Git. Amendment: customer edits stay concentrated so starter releases (fixes, legal updates) can merge cleanly: values in one configuration file per customer (the registry), structural differences as explicit override documents, and each customer repo records the starter release it forked from. Also adopted: an LLM drafts into structured data and a deterministic renderer produces the Word file; pricing is three parts (reference library with provenance, LLM-assisted development, deterministic calculation); one modular application on PostgreSQL and pgvector; founder-led onboarding first; drafts are always downloadable, with conflicts and missing facts flagged, not blocked (SYS-00 §8 to be updated); acceptance tests grade generated documents (about 20 realistic potential change order requests), not only retrieval; corpus cleanup is no longer a prerequisite, and the potential change order slice decides which documents get fixed. Superseded: runtime shared-core overlays and constraint-aware layer resolution (jurisdiction requirements become checks at publish time); generated self-service onboarding interviews (deferred); validation as an issuance gate. |
| Nov 2, 2026 | Product direction (Product Brief, a separate Claude Doc). Customer: residential builders, roughly $25M to $250M, whose client is involved during the build (mainly custom; production builders that work directly with buyers). Users: PMs and superintendents. Wedge: the priced potential change order, reached through an operating advisor (tell it what happened; it cites the rules and drafts the documents). Construction OS sits upstream of Procore and Buildertrend, which remain the project record; no project database is built. Out of scope: project tracking, schedule maintenance, accounting and payments, a national cost database, legal advice, e-signatures. In scope as reviewed drafts: bid and preconstruction estimates, using the same pricing method as change orders. Pricing data is company data, extracted at onboarding from the company's last year of bids and contracts; SYS-09 becomes Beacon Hill Interiors' data. Onboarding is extraction then Policy Owner confirmation, with questions only for gaps. Everything generated is a draft for a person to review. |
| Nov 2, 2026 | Configuration architecture direction adopted, with an outside review's changes (details in section 7, "Configuration architecture"). Construction OS is a governed document-generation system with deterministic rule and configuration resolution, supported by retrieval where it helps; not an LLM with a large index. Sequence: the remaining rule passes pause (AUTH-WRITTEN PRs 3 and 4 included) so configurable values stop being cemented as prose; a read-only configuration inventory runs first and classifies every candidate; the registry schema is designed from that real list; then a thin vertical slice (POL-01, the governing financial control, one change-order definition) is generated under two Massachusetts company configurations. Success test: changing one approved company setting changes every relevant output and validation result without editing or re-embedding any core document. Decision log rows that later rows replaced are now labeled SUPERSEDED or PARTLY SUPERSEDED, so an older decision is never read as current. Claude Project synchronization is retired. |
| Nov 2, 2026 | Billing a change requires the executed prime contract change order; a signed potential change order authorizes work but is not billed until the contract value changes. FCM-04 owns the control; FCM-03 7.5, CHG-53, CHG-55 and WF-01 align in the BILL-SUPPORTED pass (#25). Prime contract change orders should be executed at least once per billing cycle. Change event clock: FCM-03 7.1 owns it, 48 hours from discovery; CHG-51 refers to it. Body version and effective-date stamps and blank sign-off footers are removed corpus-wide (#28); a document's version and effective date live only in front matter, and effective\_date is set whenever a version changes. |
| Nov 1, 2026 | AUTH-WRITTEN pass decisions (issue #15). (1) A potential change order signed by the client and co-signed by the Executive is an accepted form of authorization; the prime contract change order formalizes it later. (2) A not-to-exceed amount is a ceiling inside a signed Construction Change Directive or time-and-materials authorization, never authorization on its own. (3) CHG-59: client-directed time-and-materials work follows AUTH-WRITTEN; time-and-materials issued to a subcontractor follows APPROVAL-SPEND. (4) SUB-02 keeps its own emergency notice clause, changed from "after performing" to "after commencing" to match SUB-A11 18.3; attorney packet, because the MSA incorporates the SOPs. (5) A Construction Change Directive is signed by the client and co-signed by the Executive, with the architect added where the contract requires. (6) FCM-11 keeps change-exposure tracking, limited to emergency work and recording violations. (7) A fix that changes a requirement is a major version (2.0), including the 48-hour edits. Decisions 1, 2 and 5 change POL-01, so POL-01 2.0 is merged first; the pass runs control owners (FCM), then the change chain (CHG, WF-01), then other PM documents, then the SUB-A11 contract edit; the APPROVAL-SPEND pass (#26) follows. |
| Nov 1, 2026 | Remediation Decisions 4–6 (change-order slice, issue #15). (4) Emergency work: POL-01 AUTH-WRITTEN keeps the principle ("documented and authorized as soon as possible"); FCM-03 owns the clock (change event within 24 hours, client notified same day if possible). No POL-01 change. FCM-06's 2-business-day retroactive commitment is spending (APPROVAL-SPEND, #26). SUB-02 13.2 and SUB-A11 18.3 (subcontractor notifies the company within 24 hours) agree; SUB-02 cites SUB-A11. (5) Subcontractor change requests: 5 calendar days from discovery, with waiver for late submission; SUB-A11 7.2 changes "days" to "calendar days" (attorney confirms). SUB-02 10.4's 5 calendar days from the company's direction to price is a separate deadline and stands. (6) Internal change log (CHG-52) and delay log (SCH-72) entries: within 48 hours of discovery, replacing "24–48 hours". Not a conflict with CON-13's two-business-day notice to the client, which is a separate obligation. |
| Nov 1, 2026 | Remediation Decision 3: FCM procedures and PM-facing SOPs don't outrank each other wholesale; each decision has one owner (SYS-00 §4.1). The FCM document owns the control (thresholds, approvals, required backup, deadlines that exist for financial control). The PM SOP owns the steps (who, in what order, which form) and refers to the FCM document instead of restating the control. Example: BIL-75's pay application review window defers to FCM-04. Recorded in each document's controls field, seeded from SYS-04's FCM table; applied during the rule passes. Replaces SYS-04's contradictory "governs" vs "sits parallel" wording. |
| Nov 1, 2026 | SYS-05 to SYS-07 are rewritten, not retired: they keep their tone, citation, role, and "what you don't do" instructions and point to POL-01 instead of restating rules. SYS-04 §8 and SYS-08 point to POL-01 too. This is an interim hand edit; the Oct 31 decision still stands that SYS-04 and SYS-05 are regenerated from the new structure once the workbench system instruction exists. Scope check and fidelity check fail on intended body edits, so content pull requests need a declared list of changed documents (plan issue log item 9). |
| Nov 1, 2026 | Remediation follow-ups. (1) RECEIPT-CAPTURE: core default stays 24 hours; Beacon Hill Interiors' company value is same day, configured once the company profile has a rule-values section; SYS-02 refers to the rule instead of stating a value. (2) Stop-work: Company stop-work authority stands alongside SAFETY-FIRST; procedures must add the individual right to stop work and protection from reprisal (SUB-06 §14.1A, version 2.0). (3) Scope ambiguity: SUB-03 10.4 (ambiguity presumed included) and SUB-A03 7.3 (ambiguity to change management) are compatible with SCOPE-GC-AUTHORED; SUB-A03 controls and SUB-03 is aligned to it (attorney packet). (4) Reports are dated baselines and are not edited after merge; GitHub issues track fixes. (5) Backlog is grouped by rule pass and document, not one issue per row. |
| Nov 1, 2026 | Every document ends up in the corpus repo; folders decide what ships (docs/ ships, design/, reports/, tools/, archive/ do not; company/\<name>/ ships only to that company). Customer documentation (governance guide, onboarding guide, user guide) lives in docs/ in the SYS series; reference material (catalog, rules and questionnaire) is generated, not written. The System Design doc, build log, and plan stay as Claude Docs for reading and are the working copy; the repo holds snapshots in design/ taken at each milestone, each marked as a snapshot. Changes flow one way, from the Claude Docs into the repo; repo copies are never edited directly. The issue log stays in the plan until backlog work starts, then moves to GitHub issues. Code stays in rag-system. |
| Oct 31, 2026 | Brand kit is a slot: core defines what every company must supply (logo, letterhead template, brand guide); each company fills it. BHI's files (SYS-10, SYS-10a logo, SYS-11) stay in place as company-layer content, referenced from company/bhi/profile.yaml. A core brand kit definition and an onboarding check (no go-live without a complete brand kit) are to be written. SYS-00 1.2 renumbered 2.0 as a major version (new requirement: core documents never contain a company's identity). |
| Oct 31, 2026 | Construction OS is for any general contractor, not a market segment. BHI content is extracted from the library: identity (name, signatory, address, location, tools) moves to a company profile referenced by {{variables}}; market positioning language ("high-end residential", "luxury") is neutralized, keeping any real requirement as an applicability condition. Values (retainage, interest, approval limits) become configurable rules with core defaults and questionnaire questions, extracted domain by domain. Ninth document type added: template (the form, contract, or layout rendered into output), separate from document\_definition. Type name stays system\_instruction. Order: migration pull request (rename and tools only), SYS-00 1.2 (template type, legal\_review field, company profile and variables), BHI extraction pull request, then front matter. |
| Oct 31, 2026 | Layer is classification, review is validation; they are kept separate. Massachusetts-specific documents are classified jurisdiction now, approved as BHI's baseline, and listed as "legal review pending" in the remediation report. A legal\_review field (SYS-00 1.2) gates distribution to other companies before any second company uses them. Documents mixing general and Massachusetts content are classified by dominant content and flagged as possible splits. Mixed core documents with BHI values stay core; their values move to rules and the company profile per slice. |
| Oct 31, 2026 | Library migration rules (SYS-00 1.1): new Product Owner role owns core and jurisdiction content (Executive owns company content), even when one person holds both. New provenance fields: adopted\_date (2026-11-01 for the existing library), legacy\_version (old filename revision), source\_file. Every adopted document starts at version 1.0; effective\_date stays empty unless known. Migration merge is the baseline approval (status approved) with known conflicts recorded in a remediation report. Layers are proposed per document in a classification report and decided by the Product Owner, not defaulted to core. document\_type keeps the SYS-00 name system\_instruction. Order: SYS-00 1.1, then the migration pull request (rename commit, then front matter commit), then layer classification. |
| Oct 31, 2026 | Executive co-signature applies to change orders, Construction Change Directives, and time-and-materials authorizations (configurable). Category spending limits (deposits, expenses, contingency, backcharges, self-performed scopes) stay as separate domain rules using the standard roles, settled in each slice. Older role names map to Executive (Principal, Operations Lead, Ops Lead, Operations/Principal, Ops/PX, Project Executive, Senior Reviewer) and Accounting (Controller, CFO); one person may hold several roles; documented in SYS-00 §2 and renamed in one later commit. BASELINE-LOCKED: no separate re-baseline approval; the baseline is revised only through an executed change order that changes contract time (which already carries the Executive co-signature). Email approval of a PCO is not accepted; a PCO requires a signature. |
| Oct 31, 2026 | POL-01 revised after the verification report. AUTH-WRITTEN: configurable; default accepted forms are a client-signed change order (Executive co-sign required), a signed Construction Change Directive, or a signed time-and-materials authorization; email approval not accepted by default; emergency life/safety/property work allowed, documented after; subcontractor changes follow APPROVAL-SPEND. SCOPE-GC-AUTHORED: minor incidental components excepted, per Exhibit C. WAIVER-SEQUENCE: limited to subcontractors and suppliers with lien rights; retail and card purchases excluded. SAFETY-FIRST: SYS-03 wording (employees and subcontractors, immediate hazard, no reprisal). APPROVAL-SPEND: FCM-19's tiers, configurable (Superintendent none, PM to $2,500, Executive above, legal review above $50,000 if needed); supersedes the earlier $2,500 / $10,000 values. TIME-ENTRY: daily on all work by default (end of shift or 9 AM next day), configurable by work type; supersedes the earlier weekly fixed-price default. A workday is any day work occurs on site, including weekends. BASELINE-LOCKED re-baseline step tabled, to revisit before the change-order slice. |
| Oct 31, 2026 | Every company configuration passes an acceptance suite before go-live and after any configuration change or core release: configuration completeness, override safety, consistency checks, retrieval and generation evaluation, output rendering, and regression. The Policy Owner signs the readiness report. |
| Oct 31, 2026 | Consistency between document types is checked continuously, not by repeated full audits: automatic structural checks block merges; AI-assisted meaning reviews run on what changed and are approved in the pull request. A full pass runs once per domain when it is first governed. The POL-01 verification is the prototype, to become a reusable tool. |
| Oct 31, 2026 | Change control (SYS-00 §7): statuses draft, approved, superseded, retired. Every change is a branch and pull request approved by the document's owner role; jurisdiction content also needs a legal or regulatory reviewer. For now, pull requests are required by a CLAUDE.md rule rather than GitHub enforcement (rulesets on private repos need a paid plan); upgrade to GitHub Pro and add required reviewers once there is a second person. Major version when a requirement or generation behavior changes (including definition fields, sections, validation); minor for wording. effective\_date is chosen at approval. Revisions keep their ID; superseded\_by only when a different document replaces it; retired when there is no replacement. Release tags are protected; every deployment records the core and company versions it runs. The pull-request approval is the audit record; POL documents also keep a readable change history. |
| Oct 31, 2026 | Document standards (SYS-00 §6): required front matter id, title, document\_type, layer, owner, status, version, effective\_date (optional for drafts). controls, applies\_to, related, and definition are added per domain. IDs are permanent, never reused. Definitions default to \<ID>-DEF and link through metadata; a document type may have several. Whole-document overrides (overrides: \<core ID>) are rare; normal overrides happen at the rule level. Version numbers leave filenames (one rename commit that also updates links). Each rule's value lives in one place; documents reference or render it, never keep a second copy. Plain language, one requirement per sentence, sections numbered 1, 1.1, 1.1.1. Automated checks flag two sources that apply at the same time, at the same layer and authority, controlling one decision with no override defined. |
| Oct 31, 2026 | Governing principle: every document has a stable identity, a defined function, an accountable owner, explicit applicability, governed authority, and a traceable release history. Governance applies to the knowledge library, not to project documents. |
| Oct 31, 2026 | Acronyms: none in policy (POL) documents. In procedures and definitions, acronyms are allowed only from an approved glossary and are spelled out on first use. Search matches both forms through aliases. Document and rule IDs are not acronyms. |
| Oct 31, 2026 | POL-01 contents approved: 12 rule blocks. Change orders need client signature plus Executive co-sign; lien waiver exceptions only with Executive approval per FCM-10; daily report required for every site day; only an Executive approves a re-baseline (SUPERSEDED: the baseline is revised only through an executed change order that changes contract time); SAFETY-FIRST locked for all customers; billing support split by contract type; APPROVAL-SPEND included. |
| Oct 31, 2026 | New POL series for Level 1 policy documents. The 10 core rules move into POL-01 Core Operating Policy, the single authoritative copy; SYS-00 covers how documents are governed and stays separate. SYS-04 to SYS-08 reference POL-01 instead of restating the rules. |
| Oct 31, 2026 | The Executive resolves conflicts, including contract vs. policy at generation time. The system flags the conflict and does not produce a final document until it is resolved. |
| Oct 31, 2026 | Standard internal roles: Executive, Project Manager, Superintendent, Accounting. "Owner" always means the client, never an internal role. The Policy Owner is the Executive unless the company designates someone else. |
| Oct 31, 2026 | Client change orders are a contract change, not spending: no spending-approval tiers. The PM prepares and issues; an Executive approves and co-signs; the client agrees and signs before work proceeds. Sub change orders (SCO) commit money and follow APPROVAL-SPEND. |
| Oct 31, 2026 | Filing stays policy: FILE-SAME-DAY. Received documents within 24 hours and minutes within 48 hours are procedure. The workbench supports it by naming outputs per PRO-22 and giving the SYS-02 folder; enforcement belongs to the future project-records system. |
| Oct 31, 2026 | SUPERSEDED by the later Oct 31 POL-01 revision (TIME-ENTRY daily on all work, configurable by work type). Time entry varies by work type (applies\_to), for BHI and as the core default: fixed-price work weekly, submitted by Friday end of day; T&M and cost-plus work daily, because the hours are billing backup. Late and correction windows follow FCM-11 §6.3. |
| Oct 31, 2026 | SUPERSEDED by the later Oct 31 POL-01 revision (FCM-19's tiers: Superintendent none, PM to $2,500, Executive above). Spending approval is one configurable table, owned by FCM-19, defined by role (APPROVAL-SPEND). BHI: Superintendent up to $2,500, Project Manager up to $10,000. Above $10,000: Owner or designated Executive. FCM-19's $50,000 tier dropped for BHI. Applies to committing money (POs, subcontracts, sub change orders), not to client change orders. |
| Oct 31, 2026 | PARTLY SUPERSEDED by Nov 1 (core default 24 hours; BHI company value same day). Receipts are two rules: RECEIPT-CAPTURE within 24 hours of purchase; RECEIPT-CODING by the weekly cutoff. "Same day" stays a training goal, not a rule. Core default and BHI value. |
| Oct 31, 2026 | SYS-04 and SYS-05 are kept as prior design and later regenerated from the new structure, not hand-edited. SYS-05's tone, citation, and "what you do not do" rules stay as AI configuration; its policy content moves out. |
| Oct 31, 2026 | SYS-04's FCM "PM SOPs It Governs" table seeds the controls metadata; its stage tables seed applies\_to: stage. Its domain relationships are kept; its breadth-based ranking is not (safety is Level 1 policy; stage guides are navigation). |
| Oct 31, 2026 | SYS-04 §8 is the canonical source text for the 10 core rules when they move into one Level 1 policy; the 48-hour vs. 9 AM conflict is resolved there |
| Oct 31, 2026 | Three working docs, one job each: System Design holds decisions, the Build Log holds discoveries and the story, the Plan holds the work. Each fact is recorded in one place. |
| Oct 31, 2026 | Every document that can go to Markdown is converted; forms and contracts keep a .docx print master alongside a Markdown copy |
| Oct 31, 2026 | Rules reference roles, not people; the company profile maps roles to people |
| Oct 31, 2026 | Company configuration via an interview or uploaded document, both generated from the rule registry |
| Oct 31, 2026 | Jurisdiction is tagged on rules now; built as a separate layer later |
| Oct 31, 2026 | Core ships opinionated defaults; the product works with no configuration on day one |
| Oct 31, 2026 | Overrides happen at the rule level, not the document level; some rules are locked |
| Oct 31, 2026 | UNDER REVISION Nov 2 (resolution becomes constraint-aware; see configuration architecture). Three layers: core, jurisdiction, company; resolved company first |
| Oct 31, 2026 | PARTLY SUPERSEDED by Oct 31 (SYS-00 1.1): the Product Owner owns core and jurisdiction content; the Policy Owner owns company content. Policy is owned by the company's designated Policy Owner (Justin for BHI) |
| Oct 31, 2026 | Timing rules: firm-wide non-negotiable timing is policy; process-specific timing is procedure |
| Oct 31, 2026 | Policy, procedure, and definition are sorted at the sentence level; tiebreaker is whether a change needs management approval |
| Oct 31, 2026 | Document definitions are separate files referenced by SOPs; existing IDs kept |
| Oct 31, 2026 | SUPERSEDED by Oct 31 (ninth type: template; type name system\_instruction). Eight document types; generated documents are outputs, not a type |
| Oct 31, 2026 | Request input is ephemeral; never stored as governed knowledge |
| Oct 31, 2026 | Scope: document-generation workbench; project records and tracking deferred to a separate system |
| Oct 31, 2026 | PARTLY SUPERSEDED Nov 2: the repo is the source of truth; Claude Project synchronization is retired. The construction-os-corpus repo is the source of truth; the Claude Project and Drive are synced copies |
| Oct 30, 2026 | Corpus frozen as found and tagged v0-raw before any cleanup |
