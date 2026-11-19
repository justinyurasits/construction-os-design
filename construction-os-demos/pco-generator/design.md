---
type: design
status: draft
---

# PCO Generator — Design

**Draft.** Section 2 describes v3 as it runs today. Section 2b is the pricing design
decided on 2026-11-19. It isn't built, and no code change is scheduled: the live app
stays as it is. Decisions dated 2026-06-19 were reconstructed from the commit history on
2026-11-19.

## 1. Scope and boundaries

| In scope now | Deferred |
| --- | --- |
| One document type: the Potential Change Order | Executed change orders, change event logs: not planned for the demo |
| One fixed rate table (SYS-09) and markup (21%) | A user's own rates and markup: that's Construction OS |
| PDF and Word, delivered by email | Download in the browser, saved drafts: only if the demo's audience needs them |
| Typed or dictated field notes | Photos, attachments, quotes as input |

## 2. How it works (v3, live)

```
index.html (GitHub Pages, draftconstructionchangeorder.com)
  │  POST JSON: email, company, project, address, PCO no., contract date,
  │             cause, scope notes, labor $, material $, schedule days
  ▼
app.py (Flask on Render, pco-generator.onrender.com)
  │  check required fields · rate limit 10/hr/IP · temp dir
  ▼
generator.generate()
  1. generate_pco_text: one Claude call (claude-sonnet-4-6, temperature 0,
     max_tokens 1500). The system prompt holds CHG-51 structure, the cause
     taxonomy, the full SYS-09 rate sheet as text, the fixed legal paragraphs,
     and the output format: plain text under ten fixed headings. The model
     writes everything, including every cost line, subtotal, markup and total.
  2. parse_sections: split the text on exact heading matches.
  3. parse_cost_table: split cost lines on "|".
  4. build_pdf (reportlab) and build_word (python-docx): letterhead, header
     block (validity = today + 21 days), sections, cost table, signatures.
  ▼
app.py: Resend email with both files attached → 200 {"success": true}
```

Nothing is stored. Gunicorn runs one worker that restarts every ~10 requests to keep
memory down on Render.

## 2b. Pricing in code (decided, not built)

The same split the governed PCO in Construction OS uses
([pco-design.md §6](../../construction-os/document-workbench/pco-design.md)),
cut down for a standalone tool: **the model proposes scope and quantities, code works
out every number, and the fixed language comes from a template.**

1. **Rates as data.** SYS-09 moves out of the prompt string into a data file. Each rate
   gets a stable ID, a description, a unit, a low and a high value, and a division
   (e.g. `DIV06-SUBFLOOR-MAT`, SF, 3.26, 3.76). The prompt is built from that file, so
   the model and the code see the same table.
2. **Structured output.** The model returns JSON (tool use or a JSON schema):
   - the narrative: scope baseline, scope change, inclusions, exclusions, assumptions,
     schedule impact explanation, cause category and explanation;
   - `line_items`: each one a description, a `source` (a rate ID, `contractor_labor` or
     `contractor_material`) and a quantity in that rate's unit.

   No dollar amounts. A line uses `contractor_labor` or `contractor_material` when the
   PM gave that total. SYS-09 rates are used only for what the PM didn't price.
3. **Validate (code).** The cause is in the taxonomy. Every rate ID exists. Every
   quantity is a positive number. Every required narrative field is present. A line
   that fails becomes `[TBD]` with a flag. A missing narrative field fails the request.
4. **Price (code).** The PM's own labor and material totals are used as given. Every
   other line is priced at the **midpoint** of its SYS-09 range. Decimal arithmetic:
   line = rate × quantity, rounded to cents.
   Subtotal. The three markup components, each on the subtotal. Total. Revised
   contract sum if the original was given. Valid-through = PCO date + 21 days.
5. **Render (code).** Contract Modification, Validity and Authorization are fixed
   templates with values filled in. The cost table is built from the priced lines, and
   each line's basis text says where its number came from: "Contractor estimate", or a
   sample rate such as "Sample rate: $3.51/SF × 60 SF". SYS-09 prices are always
   labelled as **sample rates**, never presented as the user's own.
6. **Tests.** Unit tests for every pricing function. Golden tests for the three
   `test_run.py` cases with the model response stubbed. A test that fails if the raw
   model output contains a dollar figure.

The model still decides how to break down the work and the quantities. That's judgment
the PM reviews, and the draft labels it as an estimate. What changes is that the
arithmetic can no longer be wrong, and every number can be traced to a rate.

## 3. Constraints

- **Code for numbers, the model for language** (decided, not built). No dollar amount
  reaches the document unless code calculated it.
- **The user's numbers come first.** SYS-09 fills only the gaps, and is labelled as sample
  rates.
- **Draft only.** Every document says "DRAFT — FOR PM REVIEW ONLY". The tool never
  sends anything to an owner.
- **No work before signature.** The Authorization section says so, and that text is
  fixed. It gives no other instruction contractual weight: no T&M clause.
- **Keep nothing.** No database. Files exist only in a request's temporary directory.
- **Secrets** (`ANTHROPIC_API_KEY`, `RESEND_API_KEY`) come only from environment
  variables on Render.
- **No user data in logs** beyond what an error needs.

## 4. Decision log

Newest at the top.

| Date | Decision | Options considered | Why | What would change it |
| --- | --- | --- | --- | --- |
| 2026-11-19 | Drop the Authorization clause saying verbal or written direction without a signed PCO authorizes T&M billing. | Keep it. | It gave an unsigned instruction contractual weight, which contradicts "no work until signed". | A contract-specific need, which belongs in Construction OS, not the demo. |
| 2026-11-19 | SYS-09 prices are labelled "sample rates" in the document. | Present them as standard pricing; let users enter their own rate table. | They're one Boston-area firm's rates, applied to every public user. Labelling them keeps the draft honest. The user's own numbers already take precedence (next entry). | Users asking to load their own rate table. |
| 2026-11-19 | The PM's own labor and material numbers are the price when given. SYS-09 is used only where the PM gave none. | Rate-sheet itemization with the PM's totals shown as a check; rate sheet always. | The PM knows the job. The rate sheet is a fallback, not a second opinion. | Evidence that PMs' typed totals are routinely wrong. |
| 2026-11-19 | A SYS-09 range is priced at its midpoint. | Low end; high end; show the range. | One number per line, with no bias up or down. | PM feedback that sample prices run consistently high or low. |
| 2026-11-19 | Move all pricing arithmetic into code. Not built, not scheduled: the live app is unchanged. The model returns structured line items (rate ID + quantity) and the narrative. Code validates, prices, applies markup and renders the fixed language (§2b). | (a) Keep v3: the model does the math. (b) Keep v3 but have code recompute and reject a mismatch. (c) Go back to v2: contractor totals only, markup in code, no itemization. (d) Structured line items priced by code. | (a) has no check, and the public brief already claims prices are never generated by the model. (b) catches bad sums but still lets the model invent unit prices. (c) is safe but drops the itemized table that was the reason for v3. (d) keeps the itemization and makes every number traceable. It follows "code for rules and numbers, the model for language" from the [demos brief](../brief.md) and the governed PCO's pricing engine. | Structured output that measurably makes scope worse, or the demo moving onto the workbench's pricing engine instead. |
| 2026-06-19 | Rate limit: 10 per IP per hour, 200 per day, held in memory. | No limit; a store shared across workers (Redis). | A public form that makes a paid model call every time it's submitted. One worker, so an in-memory count works. | More than one worker, or abuse that gets through. |
| 2026-06-19 | One gunicorn worker that restarts every 10 requests (±5); max_tokens cut from 2500 to 1500. | A bigger Render instance. | Memory pressure on the Render instance (commit b2df6d9). | A paid instance, or output being cut off at 1500 tokens. |
| 2026-06-19 | v3: the model builds an itemized cost table from the SYS-09 rates in its prompt, with the contractor's numbers as anchors. Markup moved from code to the model. | Keep v2's labor + material totals with markup in code. | A line-item table with a cost basis for each line looks like a real GC's PCO. | Superseded by the 2026-11-19 decision once it's built. |
| 2026-06-19 | Deliver by email (Resend) from a verified domain, not as a download. | Download in the browser. | Captures an email address. Nothing has to be hosted or stored. | A need to see the result instantly, or deliverability problems. |
| 2026-06-19 | Static front end on GitHub Pages; Flask API on Render, CORS open. | A single Flask app serving both. | Free hosting for the page and a custom domain through CNAME. | Merging into a `construction-os-demos` repository. |
| 2026-06-19 | v2: the document is a PCO, not a change order. Scope follows CHG-51 (baseline → change). Cause categories from the CHG-51 taxonomy. 21-day validity. Markup 1% + 10% + 10% calculated in code. | v1's generic "change order". | The document a GC sends for owner approval is the PCO. The executed CO comes after. | — |
