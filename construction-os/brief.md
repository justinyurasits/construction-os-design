> **Synced from Claude Docs. Edit there, not here.**
> Source: [Product Brief](https://claude.ai/artifact/Jq4zbLUWWcKNfSZaS5XuyP) · doc revision 22 · synced 2026-11-08

# Construction OS — Product Brief

Nov 2, 2026 · @Justin

The governing product reference: every product and architecture decision gets checked against it. Construction OS is a company-specific authoring system that understands construction operations and produces the documents PMs and superintendents need. It is not a chatbot, a project management system or an autonomous estimator. Answers are Justin's.

## 1. Customer

**Who:** residential builders with roughly $25M to $250M or more in revenue, where the client is involved during construction. Mainly custom and high-end residential builders (one-off homes and major renovations, with architects, allowances, condo boards, and client-driven change). Production builders fit too when they work directly with buyers during the build (options, selections, change requests). Not commercial builders.

**What a customer looks like:** roughly 10 to 40 PMs and superintendents running 15 to 60 jobs at once, usually on Buildertrend or Procore already.

**Who uses it:** project managers and superintendents, every day. PMs at a desk for documents like change orders and billing; superintendents on a phone in the field for daily reports, safety, punch lists and RFIs.

**Who buys it (assumption, to confirm):** the COO, VP of Operations, or owner: the person whose problem is that every PM does things their own way and the company leaks margin. This is why configurability matters: the buyer wants their own way followed in every answer and every draft. Construction OS guides content; it does not enforce employee actions, approvals or workflow.

**The common thread:** a client who is part of the build, which means change, communication, and documents that have to hold up later.

## 2. The painful moment

**Justin's story:** a project manager has to write three change orders, an RFI, and two customer selections. He has three hours left in the day, the work is about fifteen hours' worth, and all of it is due tomorrow.

**What that says:** the core pain is time. The PM knows how to do the work; there's just far more documentation than hours. What gets cut under that pressure is exactly what the company's process exists to protect: complete pricing, the right signatures, schedule impact, notice deadlines, filing.

**So the promise is fast and right together.** Speed alone makes careless documents faster. Governance alone makes the backlog worse. Construction OS is worth buying when the documents come out quickly and already follow the company's rules.

**Where the fifteen hours go:** going back through notes, writing the document by hand, formatting it, checking it's right, and making sure it matches the project's existing documents (the contract, earlier change orders, the schedule of values). Pricing and fact-gathering are not the bottleneck; turning notes into a correct, consistent document is.

**What happens when it slips:** missed deadlines, missed payment schedules, and another day lost on the project for every day the paperwork waits. Unbilled changes are cash the company has earned and can't collect; late notices are rights it can lose.

**The buyer's language:** cash flow and schedule. The PM feels the time; the COO feels the money and the days.

**Tension to resolve:** "matches the existing documents" means reading the project's own documents, but project records are out of scope (System Design section 1). Today's answer is that the user supplies them with the request, and they are used for that request only. Whether that is good enough for a PM with fifteen hours of backlog is an open question.

## 3. What it replaces

**Justin's experience at two companies:** both used Procore, and the PM still wrote everything by hand. For a potential change order: write every section, build the estimating spreadsheet, assemble a document, then upload it (or paste its content) into Procore and let Procore generate the formatted version. RFIs and submittals were documents the PM wrote. Some companies may use the Procore or Buildertrend modules more fully; these two did the writing by hand.

**What that says:** Procore and Buildertrend are the container, the workflow and the record. They don't write anything. The authoring (notes into a correct, complete, consistent document) happens in Word, Excel and the PM's head, and that is where the fifteen hours go.

**So Construction OS doesn't replace Procore; it sits upstream of it.** It writes the content that Procore stores, routes and formats. The PM's output today goes into Procore by hand; Construction OS's output should go in the same way at first, then directly.

**What it actually replaces:** blank Word documents, copied old documents, personal spreadsheets, and the senior PM's memory of how the company does things.

**Consequence for scope:** the project-records system in the design may not need to be built at all. For most customers it already exists: it's Procore or Buildertrend. "Matching the existing documents" (section 2) becomes reading from those systems, not building a new one.

## 4. The wedge

**The document: the potential change order.** It's where the cash is, it's the most governed document in the library, and it's the slice already being built.

**The second job, which Justin uses every day: an operating advisor.** Construction OS knows the company's operating principles, not just its templates. Justin's example: the owner walked in and asked to move a wall, the carpenter started, and there was no approval. What now? Construction OS answers with the rules that apply, what to do next, how the process works, what's needed, and which documents execute each step.

**Together, they are one flow:**

1. **Tell it what happened,** in plain words, at the desk or from the field.
2. **It says what the company's rules require,** citing the policy and procedure.
3. **It offers to draft the documents that step needs, and drafts them when asked,** starting with the potential change order, already following those rules.

The advisor is how people arrive; the documents are what they leave with.

**Why it matters to each person:**

- **PM:** the fifteen hours shrink, and the hard calls get a second opinion.
- **Superintendent:** a field question gets a real answer on a phone, which is the use superintendents will actually have.
- **COO:** every PM handles a situation the way the company's best PM would, and it's written down correctly.

**The wedge includes pricing.** A potential change order is a priced document, so Construction OS builds the estimate too, not only the words around it. That needs three kinds of input:

- **Company configuration:** labor rates, markup, overhead and profit, and how they apply by contract type. These are registry parameters.
- **Project terms:** the markup or fee the prime contract allows on changes, which can override the company's defaults for that project.
- **Request input:** subcontractor and supplier quotes, quantities, and hours from the PM's notes, used for that request only.

**Construction OS ships the pricing method and configurable structures, not price data.** Same pattern as contracts: a starter set for a company that has none, company data at the company layer for one that does. Next step: a read-only look at how the current pricing data and estimating logic work, before deciding how it fits the registry.

**What the pricing review found (Nov 2):** the wedge's pricing is its weakest part today.

- **No defined method.** No document gives the formula for pricing a potential change order; CHG-53 and CHG-54 say markup is "per contract", and no contract states a number. The 21% (1% + 10% + 10%) applies only by inference from SYS-09 and SYS-06.
- **The two sources disagree** on the markup base (with or without general conditions), whether permits come before or after markup, the PM rate, and overhead (9–10% vs 10%). Tax and contingency have no rate anywhere.
- **The data is thin and local.** SYS-09 holds 1,258 unit costs from 12+ Boston projects, but 75% rest on one data point, 47% are lump "allowances", there are no labor hours or equipment category, and it never says whether prices are cost or sell. It is Beacon Hill-area, high-end condo data.

**Implication:** the product's value is the pricing method (inputs, order of operations, markup structure, the company's rates and the contract's overrides), applied the same way every time. Core ships the method; unit-cost data is company data.

**Decided (Justin, Nov 2): a company's pricing database is built during onboarding from its last 30 to 50 contracts and change orders.** SYS-09 becomes Beacon Hill Interiors' company data. The same extraction yields the company's labor rates and markup structure, so onboarding fills parameters from real documents instead of asking for them.

## 5. Out of scope, on purpose

| Construction OS does not | Because | What it does instead |
| --- | --- | --- |
| Keep project records or track jobs | The company's system of record already does (Procore, Buildertrend or a job folder) | Reads project documents from them when needed |
| Maintain the schedule | That's the PM's job | Drafts schedule documents (delay notices, time extension requests) |
| Do accounting or payments | Accounting handles it | Drafts billing documents that follow the company's rules |
| Ship a national cost database | Generic prices are confidently wrong | Uses cost data extracted from the client's own bids and contracts |
| Give legal advice | It isn't a lawyer | Flags matters that need legal review |
| Collect e-signatures or run a client portal | Signing happens outside the system | Produces the documents to be signed |

**In scope, as drafts:** bid and preconstruction estimates, built with the same pricing method as change orders, always reviewed by a person before use.

**The principle under all of it:** Construction OS drafts and advises. People review, sign, send and decide.

## 6. What this means for the documents layer (proposed, for Justin's review)

1. **The library serves two jobs, and each needs something different.** The advisor needs authority: current status, citations, one source per decision, so the answer is right. Drafting needs determinism: structured definitions, a registry, and a compiler, so the document is right. The governance work so far serves the first; the configuration architecture serves the second.
2. **Build for the wedge first.** The registry, compiler and checks start with what a priced potential change order uses: AUTH-WRITTEN, the change event clock, the pricing method, labor rates, the markup structure and the contract override. The rest of the 249 parameters wait until a document needs them.
3. **Onboarding is extraction, then confirmation.** Construction OS reads a company's recent bids, contracts and procedures, proposes the values it finds, and the Policy Owner confirms or corrects them. Questions are asked only for gaps. Each registry entry therefore records where the value is usually found, not only the question to ask.
4. **The company layer is first-class, not an exception.** Pricing data, contracts, and often a company's own procedures will be its own. Core is a starter set and a standard to check against. Company content is tenant-isolated.
5. **The project record lives in the company's existing system: Procore, Buildertrend or a job folder (integration is later, not in the first slice).** Some companies keep the job folder as the record even when they use Procore; Beacon Hill Interiors' SYS-01 and SYS-02 say so. Construction OS reads project documents from whichever system holds the record for context (the contract, earlier change orders, the schedule of values), and its drafts go back there. No project database gets built.
6. **Everything generated is a draft for a person to review.** Flags, missing-fact questions and validation matter more than polish.
7. **One pricing method for changes and bids.** Design it once: change orders first, then bid and preconstruction estimates.

**Gap for this customer (found Nov 2):** the starter library assumes "condominium work, residential renovations, and small projects" (STG-B). A $25M to $250M custom builder mostly builds new homes, which brings construction lender draw schedules and inspections, site work and foundations, and new-construction permitting. The wedge doesn't depend on it, since change orders work the same way, but the starter library will look renovation-shaped to this buyer.

**Still to confirm:** nothing for the documents layer. Who signs the check (section 1) is deferred as a go-to-market question; it doesn't block the build.
