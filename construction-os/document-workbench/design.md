> **Synced from Claude Docs. Edit there, not here.**
> Source: [Construction OS — Document Workbench Design](https://claude.ai/artifact/NcfkMXfG83Tg4NQpkh77TN) · doc revision 4 · synced 2026-11-19

# Construction OS — Document Workbench Design

Nov 17, 2026 · @Justin

The document workbench lets a construction company understand its own policy and generate the documents its processes require, from governed knowledge plus information the user supplies. This is the living design record: decisions are recorded as they're made.

**Split from the original System Design on Nov 17, 2026.** The corpus became its own component with its own design doc, the [Construction OS Corpus — System Design](https://claude.ai/artifact/3iEBRhf5uJpBXwf8TsCjG4), which keeps the knowledge model, document types, definitions, layers, the company profile, quality checks, configuration architecture and their decisions. This doc keeps the workbench's scope, its open design items and its decisions, moved word for word. Product-level decisions moved to the [Architecture](https://claude.ai/artifact/6UZv2djagWrjbm4AM7MXt9) page. The workbench reads the corpus through its published package and never changes it.

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

## 2. Where the design lives

- **The build spec for the first slice:** [PCO Slice — Technical Design](https://claude.ai/artifact/1xt5wM378qNBtHhy85osmX): components, the PCO definition, the pricing engine, structured drafts and Word rendering, retrieval, acceptance tests, stack and build order.
- **How the workbench fits with the other parts:** the [Architecture](https://claude.ai/artifact/6UZv2djagWrjbm4AM7MXt9) page.
- **What the workbench reads:** the corpus, designed in the [Construction OS Corpus — System Design](https://claude.ai/artifact/3iEBRhf5uJpBXwf8TsCjG4).

## 3. Not yet designed

Moved from the original System Design's section 7, in the order planned:

- [ ] **Retrieval and authority resolution:** exact ID lookup, metadata filtering, hybrid search, and selecting what controls (retrieval rank is not authority rank)
- [ ] **Generation pipeline:** identify the document type, load the definition, gather inputs, retrieve rules, resolve, generate, validate, render
- [ ] **Validation and enforcement:** which rules are checked in code
- [ ] **Evaluation:** retrieval eval (exists) and generation eval scenarios; consistency-check tool and company acceptance suite designed in section 6, not yet built

**First vertical slice:** change orders (CHG-51 to 60, FCM-03, FCM-19, SUB-02, SUB-A06/A07, relevant CON-12/13 clauses), built end to end before other domains.

## 4. Decision log

Newest first. Moved word for word from the original System Design on Nov 17, 2026.

| Date | Decision |
| --- | --- |
| Nov 10, 2026 | Pricing in a draft is a suggestion; the PM decides every price, and a human is always in the loop on pricing (Justin's practice). The aim of AI pricing is a complete, traceable structure the PM can correct quickly, not the right number: every line shows its source (rate table, cost history, quote, the PM, or labeled estimate), and general conditions appear as hours and days at rate so the PM can cut them. Found reviewing the old system's cedar closet PCO (about $54,500), which was high mainly because it carried a full-time PM and site super the job doesn't need. Drafts are revised iteratively: the PM reviews a version and gives feedback in plain words, and the app produces the next version in the same project folder, with the feedback saved as an input and a change summary. An amount the PM gives is a sourced amount; code still computes every total; lines the feedback doesn't mention stay unchanged; feedback that conflicts with company policy is flagged and policy holds. Also adopted Nov 10 from the comparison with that PCO: its layout and organization (branded first page, description with work bullets, grouped assumptions with job-specific exclusions, side-by-side signatures), with all of our correctness rules kept, and pricing presentation as a company setting, PRICING-PRESENTATION (by\_division, flat or summary\_only; BHI uses by\_division), because some contractors want pricing broken down by division. Build order (revised the same day): layout v2 (step 5a), then estimating from cost history (5c), then the revision loop (5b), so the PM's first review is of a fully estimated draft rather than one with blank quantities. The document-workbench repository stays public: without a company's private package it does nothing, and the rule that it holds no company content (names, rates, clause text, client data, fixtures built from real projects) stays enforced by its test and by review, because it is also what lets a second company use the same code. |
| Nov 9, 2026 | A PCO goes to the Owner as a standalone document. Pricing backup (subcontractor and vendor quotes, takeoffs, T&M logs) and the Owner's request correspondence stay internal, on file in the job folder; the PM checklist confirms the backup is on file, and nothing is listed as an Owner exhibit unless it is meant for the Owner, such as a layout or drawing. This holds on cost-plus work too: there the Owner receives cost backup (receipts and invoices) monthly with billing, not with each PCO (Justin's practice). Contract type does change pricing and billing (the contract's fee instead of company markup, limits on subcontract markup, cost backup with each billing), so contract type becomes a project fact set from the executed contract in build step 6; until then PCO pricing assumes fixed price. A contract that explicitly requires backup with a change remains a contract term for step 6. Resolves an ambiguity in CHG-53, which says both "attach backup" and "vendor quotes are backup only"; found when the first live drafts listed the quotes as Owner exhibits. Also adopted with the PCO polish (Nov 9): the PCO uses "Owner", the defined term in CON-13 and SYS-00, never "Client"; the company's standard clarification language (concealed conditions, limited finish, upgrades, permits, hazardous materials) lives in CHG-53-DEF and is used verbatim, pending attorney review (issue #30). The PCO is written as a letter from the Contractor to the Owner, in the contract's defined terms; internal details (who performs the work, how it was estimated, quotes) stay off it and go on the PM checklist. Owner selections are not described in the PCO: it references the Owner Selection Sheet (PRO-34) by selection ID, approved or issued with the PCO for signature. |
| Nov 2, 2026 | PCO slice design revised after an outside review. Pricing is modeled by cost category: each markup component names the categories it applies to, replacing yes/no flags. A pricing evidence interface returns rates and comparable prices with source, basis and date (v1: rate tables and supplied quotes; extracted history later). Clear, applicable contract terms are extracted before pricing and change the calculation, with the clause cited; ambiguous terms become visible assumptions (SYS-00 4.3: the contract governs what the client pays; policy governs internal conduct). Definition dependencies carry applies\_when conditions and an audience (client-facing or internal). Publishing blocks only on defects in the PCO generation path; everything else is a reported finding. Customer copies are changed directly; starter releases are adopted selectively, not merged automatically (supersedes the Nov 2 amendment's override documents; the one-file configuration stays). Build order starts with a real PCO, scenarios and the confirmed pricing values, then definition and schema, then template and renderer, before pricing code. BHI pricing values stay provisional until confirmed, including a conflict: Justin's practice adds general conditions for any extension, CON-13 only past 10% of duration. |
| Nov 2, 2026 | PCO slice technical design drafted (Claude Doc "PCO Slice — Technical Design"), pending Justin's review. No rag-system repository exists, so earlier references to it are superseded: the application starts in a new private repository, construction-os; construction-os-corpus becomes Beacon Hill Interiors' package, with a starter library split out when the second company arrives. Build order starts with the pricing engine (pure code, clear right answers). |
| Oct 31, 2026 | Scope: document-generation workbench; project records and tracking deferred to a separate system |
