> **Synced from Claude Docs. Edit there, not here.**
> Source: [PCO Slice — Technical Design](https://claude.ai/artifact/1xt5wM378qNBtHhy85osmX) · doc revision 32 · synced 2026-11-04

# PCO Slice — Technical Design

Nov 2, 2026 · @Justin

The build design for the first vertical slice: a priced potential change order, reached through the advisor or drafted directly. Built from the Product Brief, the System Design decision log (Nov 2), and the change order family map (reports/pco\_family\_map.md). Working draft for Justin's review.

## 1. Goal, scope and success test

**Product context (Product Brief, the governing reference):** residential builders, about $25M to $250M; an authoring system that sits upstream of Procore and Buildertrend; every output is a draft, with no approval, issuance or workflow enforced.

**Goal:** a PM describes a change in plain words and gets back the company's rules for it and a priced potential change order as an editable Word file, correct on the first draft more often than not.

**In scope:**

- One customer package: Beacon Hill Interiors, built from construction-os-corpus.
- Two entry paths: the advisor ("here's what happened, what do I do?") and direct drafting ("draft a PCO").
- One document type end to end: the potential change order, with pricing.
- Request inputs: the PM's notes, subcontractor quotes, and a project contract if supplied, used for that request only.

**Out of scope for the slice:** other document types, a second customer (comes right after), Procore integration, speech input, pricing extraction from historical documents, any project records.

**Success test:** changing one approved company setting (for example the markup structure or a labor billing rate) changes every relevant PCO total and check, with no core document edited or re-indexed. And the acceptance set (section 9) passes at the agreed bar.

## 2. Components and the two paths

One modular application with two entry paths that meet at the same drafting pipeline.

*The architecture diagram ("PCO slice architecture · two paths, one package") is an interactive embed that doesn't export to Markdown. See it in the [Claude Doc](https://claude.ai/artifact/1xt5wM378qNBtHhy85osmX).*

The advisor answers from rules loaded by ID plus search, then offers the PCO; asking directly for a PCO skips straight to drafting. Only the highlighted result reaches the PM, and every step reads from the published package, never from Git.

**In plain terms:** the corpus repository is the company's binder (its rules, settings, rates, definitions and templates); the construction-os repository is the machine that reads the binder. For a request like "the owner wants six recessed lights, electrician quoted $2,850", the application:

1. Loads the company's published package.
2. Decides whether the PM wants advice or a draft.
3. Gathers what applies: the rules the PCO depends on (by ID), relevant documents (search), and any contract or quote attached.
4. Has Claude draft the content as structured data: scope, reason, inclusions, exclusions, assumptions, proposed cost lines.
5. Prices it with code: rates, quotes, the company's or the contract's markup, permits after markup.
6. Checks it and attaches flags (missing facts, conflicts, signature order, placeholder values), never blocking.
7. Renders the Word file into the company's template and returns it with the flags.

| Module | Job |
| --- | --- |
| package | Load and publish the company's binder |
| registry | The settings: types, defaults, limits, company values |
| definitions | What each document must contain and which rules it depends on |
| retrieval | Search over the company's documents (the RAG part) |
| pricing | Evidence lookup and exact calculation |
| drafting | The Claude calls that produce structured drafts |
| rendering | Output adapters: Word now, others later |
| advisor | The "what do I do" path |
| api | What a web page talks to |

**Rule: the application repository holds no company content.** No company name, rate, rule or template lives in construction-os. Pointed at another company's package, the same code produces that company's documents.

## 3. Customer package and the publish step

Each customer's knowledge is a Git repository; the application only ever reads a published, versioned package built from it.

**Source layout (one repository per customer, forked from the starter library):**

```
docs/                 governed Markdown (policies, procedures, guides)
definitions/          structured document definitions (CHG-53-DEF.yaml)
registry/             parameter definitions: type, default, constraints, owner role
company/config.yaml   this company's values, identity, role-to-person map
company/pricing/      rate tables, later the extracted cost history
templates/            Word masters and brand assets
STARTER_RELEASE       the starter release this copy was forked from
```

The customer's values live in one place, `company/config.yaml`, so each value is stated once. Anything else the customer changes, they change directly in their own copy. Starter releases are offered as optional updates the customer reviews and adopts selectively; STARTER\_RELEASE records where the copy began. Automatic merging is not an MVP requirement.

**Publish step** (a command, run on demand):

1. Validate the generation path (critical, blocks publishing): the PCO definition and every dependency it declares resolve; `company/config.yaml` matches the registry's types and constraints; the PCO template exists and every field is fillable; the pricing functions the definition needs exist.
2. Report quality findings (never block): documents that restate a registry value, unrelated SOP conflicts, clauses awaiting legal review, a contract that doesn't recognize every authorization form the policy accepts. Findings go into a publish report.
3. Build: chunk and index `docs/` for retrieval, load definitions, registry and config, copy templates.
4. Stamp: package version = repository commit + publish time.

The gate certifies the PCO path, not the whole 171-document library. It applies to publishing knowledge, never to a PM downloading a draft.

Runtime reads only the latest published package for the requesting company. Every draft records the package version it used. The publish report lists every quality finding, so the library's known problems stay visible without blocking the slice.

## 4. Registry: schema and the PCO's entries

The registry defines each configurable item once; `company/config.yaml` holds the company's value; the governing document owns what the value means.

**Entry schema:**

```yaml
id: NTE-CHECKPOINTS
kind: parameter            # parameter | identity | role_mapping | module_switch
value_type: object         # duration, money, percent, count, text, role, list, object
schema: {notify_at: percent, stop_at: percent}
default: {notify_at: 70, stop_at: 90}
constraints: {notify_at: {min: 50, max: 95}, rule: notify_at < stop_at}
stricter_is: lower         # declared, never inferred
authority: {document: CHG-60, section: "9"}
change_approver: Policy Owner
onboarding: {group: change_management, found_in: [contracts, change orders],
             question: At what share of a not-to-exceed amount do you warn the client and stop?}
```

**Entries the PCO slice needs (about 20):**

| ID | Kind | Default or BHI value | Owning document |
| --- | --- | --- | --- |
| AUTH-WRITTEN.accepted\_forms | parameter (list) | signed PCO, change order, CCD, T&M authorization | POL-01 |
| AUTH-WRITTEN.exec\_cosign | parameter | required | POL-01 |
| AUTH-WRITTEN.email\_approval | parameter | not accepted | POL-01 |
| CE-OPEN-WINDOW | parameter (duration) | 48 hours | FCM-03 7.1 |
| CE-EMERGENCY-WINDOW | parameter (duration) | 24 hours | FCM-03 10.1 |
| NTE-CHECKPOINTS | parameter (object) | 70% notify, 90% stop | CHG-60 9 |
| LABOR-BILLING-RATES | parameter (table) | carpenter about $90/hour (BHI) | company pricing |
| GC-WEEKLY-RATES | parameter (table) | PM, APM, superintendent weekly | company pricing |
| GC-EXTENSION-THRESHOLD | parameter | more than 10% of duration (default; BHI) | pricing method |
| MARKUP-STRUCTURE | parameter (ordered list) | 1% application fee + 10% overhead + 10% fee (BHI) | pricing method |
| MARKUP-ON-BILLING-LABOR | parameter | yes (BHI) | pricing method |
| MARKUP-ON-SUBCONTRACTORS | parameter | yes (BHI) | pricing method |
| TAX-TREATMENT | parameter | included in material estimates | pricing method |
| REPEAT-CLIENT-DISCOUNT | parameter (optional) | off | pricing method |
| BILLING-GATE | parameter | executed prime contract change order | FCM-04 |
| role.Executive, role.ProjectManager, role.Superintendent | role\_mapping | names from the profile, with fallbacks | SYS-00 §2 |
| company.name, company.signatory, company.licenses | identity | profile | profile |

Values marked BHI are the defaults set Nov 2 (section 11). MARKUP-STRUCTURE is an ordered list whose components each name the cost categories they apply to, which replaces MARKUP-ON-BILLING-LABOR and MARKUP-ON-SUBCONTRACTORS as separate flags. A clear, applicable term in a supplied contract replaces the company value for that request and is cited (section 6).

## 5. PCO definition (CHG-53-DEF)

The definition is the center of generation: it says what the PCO contains, which rules govern it, and what to check. It's extracted from the 29 definition items in the family map, with its 10 conflicts resolved by the decisions already logged (issue #57).

```yaml
id: CHG-53-DEF
document: Potential Change Order
procedure: CHG-53
template: templates/pco.docx
depends_on:                # loaded by ID, never searched
  rules: [AUTH-WRITTEN, APPROVAL-SPEND, BILL-SUPPORTED]
  controls: [FCM-03]
  parameters: [MARKUP-STRUCTURE, LABOR-BILLING-RATES, GC-WEEKLY-RATES,
               GC-EXTENSION-THRESHOLD, TAX-TREATMENT, NTE-CHECKPOINTS, BILLING-GATE]
inputs:
  required: [project, change_description, reason, scope_inclusions]
  asked_if_missing: [scope_exclusions, schedule_extension_days, quotes, quantities]
  optional: [change_event_ref, contract, photos]
sections:                  # in order; each maps to a template region
  - header                 # PCO number, project, date, change event reference
  - description_and_reason
  - scope: {inclusions, exclusions, assumptions}
  - pricing: {lines, subtotal, markup_components, total}
  - schedule_impact        # always stated, zero included
  - terms                  # authorization, billing gate, validity
  - signatures: [client, contractor_pm, executive_cosign]
checks:
  - pricing arithmetic recomputed deterministically
  - schedule_impact present (number of days, zero allowed)
  - every assumption listed; every missing input flagged
  - authorization wording matches AUTH-WRITTEN; no email approval
  - not billable until the prime contract change order is executed
  - contract supplied and conflicts with policy: flagged, not resolved
```

The checks never block the download. They appear on the draft as flags the PM resolves.

**Dependencies apply by condition, not by association.** Each dependency carries an `applies_when`, so a requirement applies because the situation meets it:

```yaml
depends_on:
  - {id: AUTH-WRITTEN, applies_when: always}
  - {id: FCM-03, applies_when: always}
  - {id: NTE-CHECKPOINTS, applies_when: pricing_basis in [CCD, T&M] and nte_present}
  - {id: GC-WEEKLY-RATES, applies_when: schedule_extension_days > threshold}
  - {id: APPROVAL-SPEND, applies_when: subcontractor_commitment, audience: internal}
  - {id: BILLING-GATE, applies_when: always}
```

`audience: internal` means the rule shapes the PM's checklist and flags, not the client-facing document.

## 6. Pricing engine

The LLM proposes scope and quantities; a pricing evidence interface supplies rates and comparable prices with their sources; deterministic, tested functions do every number. Implements the method set Nov 2 (issue #58).

**Cost categories:** labor, materials, subcontractors, equipment, general conditions, permits and fees. Every line has exactly one.

| Category | Price | Evidence source (v1) |
| --- | --- | --- |
| labor | hours × billing rate for the trade | company rate table |
| materials | estimated cost, sized to cover tax | PM's notes or a supplied quote |
| subcontractors | quoted amount | supplied quote |
| equipment | quote, or rate × duration | quote or company rate table |
| general conditions | extension weeks × weekly rate per role, plus time-based items | company rate table; schedule extension |
| permits and fees | actual fee, passed through | actual fee, as its own line after markup |

**Pricing evidence interface:** `find_evidence(item)` returns candidate rates and prices, each with source (rate table, supplied quote, historical record), basis, date and conditions. Version 1 implements rate tables and supplied quotes; extracted history plugs in later through the same interface. Every line in the draft keeps the evidence it used, so a quote, a company rate and an estimate are always distinguishable.

**Markup as ordered steps by category:** the company's markup structure is an ordered list of components, each with a rate, the cost categories it applies to, and whether it shows to the client. "Markup on subcontractors" is not a flag; it's whether subcontractors are in a component's categories.

```yaml
markup_structure:          # Beacon Hill Interiors default
  - {name: Application fee, rate: 1%, applies_to: [all], condition: every change order}
  - {name: Overhead, rate: 10%, applies_to: [all]}
  - {name: Fee, rate: 10%, applies_to: [all]}
```

**Contract terms apply in the calculation.** Before pricing, applicable terms are extracted from a supplied contract with their section references (markup caps, allowed categories, general conditions rules). A clear, applicable term replaces the company value for that request and is cited on the draft; an ambiguous one is shown as an assumption and flagged. This follows SYS-00 4.3: the contract governs what the client pays, and company policy still governs internal conduct.

**Functions:** `price_line`, `general_conditions`, `subtotal`, `apply_markup` (component by component, over each component's categories), `total`. Decimal arithmetic, rounded to cents per line and per component.

**Confirmed vs provisional:** the method (cost lines into one subtotal, the markup structure once at the end, schedule extension always stated, tax carried in material estimates) is confirmed from Justin's practice. The BHI values (rates, the 1% on every change order, permits passed through after markup, the 10% general conditions threshold) are the agreed defaults from section 11, replaced per company at onboarding.

**Worked example (default BHI values):** carpentry 8 h × $90 = $720; electrical quote $850; materials $600; no schedule extension. Subtotal $2,170. Markup 1% + 10% + 10% = $455.70. Total $2,625.70.

## 7. Structured draft and Word rendering

The LLM never writes the Word file. It fills a structured draft that matches the definition; code checks it, prices it, and renders it into the company's template.

1. **Draft (LLM, structured output):** JSON matching CHG-53-DEF's sections: description, reason, inclusions, exclusions, assumptions, proposed cost lines (type, quantity, unit, basis, source), schedule extension, open questions. Unknowns are marked as unknowns, never guessed.
2. **Price (code):** first, applicable terms are extracted from any supplied contract, with section references; then the pricing engine finds evidence for each line, replaces every number with computed amounts, and applies the markup components (contract terms first, company values otherwise).
3. **Check (code, then LLM for wording checks):** runs the definition's checks and attaches flags: missing inputs, assumptions, policy or contract conflicts.
4. **Render (code):** a Word template with named fields and a repeating pricing table (docxtpl on python-docx); company identity and letterhead come from the package. Approved fixed language (terms, authorization, billing gate) comes from the template, never regenerated.
5. **Deliver:** an editable .docx, a preview in the workbench, the flags beside it, and an internal manifest (package version, definition version, parameter values used, sources cited). The client-facing document carries only a short generation reference.

The structured draft is independent of its destination: rendering is an output adapter. Word is the only adapter in the slice; a Procore or Buildertrend adapter can be added later without changing the draft schema. Revision happens by conversation ("add a day of carpentry"), which edits the structured draft and re-runs steps 2 to 5.

## 8. Retrieval and dependency resolution

Mandatory knowledge is loaded by ID from the definition; search only adds supporting context and powers the advisor.

| Need | Mechanism |
| --- | --- |
| The rules and controls a PCO must follow | Deterministic: the definition's `depends_on`, loaded by ID |
| The company's values | Exact lookup in the published config |
| "What do I do when..." questions | Hybrid search over the package's `docs/` |
| A contract or quote the PM supplied | Facts and terms extracted for that request only, with section references, and used in pricing; never indexed |

**Hybrid search:** PostgreSQL full-text search plus pgvector embeddings, merged with reciprocal rank fusion (k = 60). Chunks follow the documents' numbered sections, so a citation is a document ID plus section. Each chunk carries its front matter as metadata.

**Filters and ranking:** only `status: approved`; the company's package only (enforced in the query, not by the prompt); `applies_to.stage` boosts ranking and never filters; policy and control documents rank above guides when they match equally. Retrieval rank is never treated as authority.

**The advisor answer** cites each rule by ID and section, says which document controls and why (SYS-00 4.3), and offers the documents that execute the next step. Where a supplied contract and the policy disagree, it says so and doesn't decide.

## 9. Acceptance tests

The slice is graded on the documents it produces, using about 20 real situations Justin writes from his own jobs.

**Each case holds:** the PM's words, any quotes or contract excerpt, and the expected result: the rules the advice must cite, the flags it must raise, the pricing lines and total within a tolerance, and the schedule impact.

**Mix:** clean changes; missing information; work already started without approval; email approval; subcontractor quotes; unknown conditions (a CCD with a not-to-exceed); schedule extensions; a contract that conflicts with policy; a request that isn't a change at all (a selection within the allowance).

**Graded on:**

| Dimension | Pass means |
| --- | --- |
| Advice | Cites the right rule IDs and sections; names the next steps and documents |
| Pricing | Arithmetic exact; lines match the method; every number has a basis |
| Completeness | Every required section present; schedule impact stated |
| Honesty | Unknowns asked or flagged, never invented |
| Conflicts | Policy vs contract conflicts flagged, not resolved |
| Format | Renders in the template; opens and edits cleanly in Word |

**Two configurations:** the same cases run against BHI and a second test company with a different markup structure and rates; totals change, rules and structure don't. That's the success test from section 1.

Time saved is the headline measure. The Product Brief's story (three change orders, an RFI and two selections due tomorrow) is the real test. For the slice: time from rough notes to a usable PCO draft, against Justin's estimate of doing it by hand, and how much the PM had to fix. The retrieval eval stays as a unit test for search, not the acceptance bar.

## 10. Stack, repository and build order

Justin confirmed Nov 2 that no rag-system repository exists (earlier notes describe one that was never built), so the slice starts in a new repository.

**Stack:** Python 3.12 and FastAPI for the backend; PostgreSQL 16 with pgvector in Docker; OpenAI text-embedding-3-small for embeddings; Claude for advice and drafting, with structured output and tool calls (no agent framework); docxtpl on python-docx for Word rendering; a minimal web page for the slice, Next.js later.

**Repositories:**

- `construction-os-corpus`: stays as is for now and becomes BHI's package. A clean starter library and a separate BHI repository split out when the second company arrives.
- `construction-os` (new, private): the application. Modules: `package` (publish), `registry`, `definitions`, `retrieval`, `pricing`, `drafting`, `rendering`, `advisor`, `api`. Secrets only in `.env`, gitignored, never read by Claude Code.

**Build order (each step testable on its own):**

1. **Examples and approved pricing method.** Pricing defaults are set (section 11) and no past PCOs exist, so this is done when Justin's first 5 scenarios are written; the rest follow.
2. **CHG-53-DEF, minimal config and the structured draft schema.** Done when a hand-written sample draft passes schema validation.
3. **Word template and renderer.** Done when that sample draft produces a professional, editable PCO that looks like what PMs actually send.
4. **Pricing functions and the evidence interface** (rate tables, supplied quotes). Done when known cases calculate exactly, including category rules and contract caps.
5. **LLM drafting.** Done when rough PM notes become a priced Word draft.
6. **Retrieval and contract term extraction.** Done when drafts use the right governing sources and flag conflicts.
7. **Advisor path.** Done when a described situation returns cited advice and can turn into a PCO.
8. **Second-company regression.** Done when the same application produces different, correct company-specific pricing and documents.

The Word document is the product's output, so it's validated early: steps 1 to 3 prove the PCO looks right before pricing and AI are built behind it. These exclusions bound the slice, not the commercial MVP.

## 11. Open questions

- [x] **Template source:** no past PCOs are available. The template is built from CHG-53-DEF's sections and the family map's 29 definition items, then judged by Justin the way a PM reading it would.
- [x] **Billing and weekly rates (default):** SYS-09's Labor Rates sheet, with the carpenter at $90/hour and the updated weekly rates (PM $2,664). Replaced per company at onboarding.
- [x] **1% application fee (default):** applies to every change order, as part of the markup structure.
- [x] **Permit fees (default):** actual fees pass through as their own line after markup, not marked up (SYS-09 and FCM-16 8.3 agree).
- [x] **PCO numbering (default):** PCO-001, PCO-002 and so on per project, assigned by the PM in order.
- [x] **Price validity (default):** 30 days from the PCO date, stated in the terms.
- [x] **General conditions threshold (default):** added only when a change extends the duration by more than 10%, matching CON-13. BHI follows it; configurable per company.
- [ ] Justin's acceptance cases: about 20 situations, starting with 5.
