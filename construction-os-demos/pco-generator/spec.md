---
type: spec
status: draft
---

# Construction OS Demos — PCO Generator Spec

**Draft.** Every requirement says whether the live code (v3, June 19, 2026) meets it.
Where it doesn't, the requirement is the decided design
([design.md](design.md#4-decision-log)); no code change is scheduled.

## The domain

| Term | Meaning here | Where its rules come from |
| --- | --- | --- |
| Potential Change Order (PCO) | A priced proposal for a change to the contract, sent to the owner for signature. Work doesn't start until the PCO is signed. It isn't the executed change order. | CHG-51 (Change Event SOP), as written into the generator's prompt |
| Cause of change | Exactly one of: Owner-Requested Change, Design Revision / ASI, Unforeseen Field Condition, Allowance Over/Under, Coordination Conflict, Unit Price Work, Other | CHG-51 taxonomy, `CAUSE_CATEGORIES` in `generator.py` |
| Sample rate | A unit price for labor or material from SYS-09 (e.g. demo crew $1,920/day, 3/4" subfloor material $3.26–3.76/SF). A range is priced at its midpoint. Used only where the PM gave no number, and labelled "sample rate". | SYS-09 (Beacon Hill Interiors estimating schedule), embedded in `generator.py` |
| Markup | 1% application fee + 10% overhead + 10% fee, each taken on the construction subtotal (21% total) | SYS-09 / the prime agreement |
| Validity | 21 days, after which the pricing can be revised | `PCO_VALIDITY_DAYS` |
| Contractor anchors | Optional labor and material totals the PM types into the form | The form |

No product-level spec exists for the demos project, so requirements here don't point to
capability IDs.

## Requirements

### R1 Accept a described change

The API accepts a JSON request from the form and rejects it if required fields are
missing.

**Met today:** yes.

**Acceptance criteria**
- Given email, company name, project name, scope description and cause, the request is
  accepted.
- Given any of those missing, it returns 400 and names the missing fields.
- Given a scope description shorter than 10 characters, it returns 400 and asks for more
  detail.

### R2 Produce every section, in order

The PCO contains, in this order: Scope of Additional Work, Inclusions and Exclusions,
Assumptions and Conditions, Cost Table, Schedule Impact, Cause of Change, Contract
Modification, Proposed Revised Contract Sum, Validity, Authorization, and signature
blocks for contractor and owner.

**Met today:** partly. If the model leaves out or misspells a heading, that section is
silently dropped from the document.

**Acceptance criteria**
- Given any accepted request, every section is present in both the PDF and the Word file.
- Given model output that's missing a section, the request fails with a clear error, or
  the section shows `[TBD]` with a visible flag. A document never goes out with a
  section missing and no sign of it.

### R3 Scope language stays within the input

The scope gives the baseline (what the contract included) and then the change, written
as the GC's scope in formal language. It adds no work that the input doesn't describe.

**Met today:** by instruction to the model only; nothing checks it.

**Acceptance criteria**
- For each case in the evaluation set, a reviewer finds no scope item that isn't in the
  input.

### R4 Every number comes from code

The model may propose line items and quantities. It never states a dollar amount.
Code calculates every amount: each line, the subtotal, each markup component, the
total, the revised contract sum and the validity date.

**Met today:** no. In v3 the model writes every amount and every total, and code prints
them without checking. (v2 did the markup in code.)

**Acceptance criteria**
- Given the same line items and quantities, the totals are identical on every run.
- Every amount equals rate × quantity (or the contractor's input), rounded to cents.
- Subtotal = sum of the lines. Each markup line = its percentage of the subtotal.
  Total = subtotal + markup.
- A test fails if a dollar figure appears anywhere in the model's raw output.

### R5 No number without a source

Every line in the cost table names where its number came from. The PM's own labor and
material totals are used when given. Otherwise a SYS-09 sample rate (midpoint of its
range) × a quantity, labelled as a sample rate. A line that can't be priced shows
`[TBD]` and is left out of the totals, and the totals say they're incomplete.

**Met today:** no. v3 tells the model to cite a basis, but nothing checks the citation.
When the contractor leaves costs blank, the model estimates them. The intended `[TBD]`
behavior (`test_run.py` case 2) was v2's.

**Acceptance criteria**
- Given a labor total from the PM, labor is priced at exactly that amount.
- Given no labor or material total, those lines use sample rates at the midpoint, and
  each says "sample rate".
- Given a line whose rate ID doesn't exist in the rate table, that line is `[TBD]` and
  flagged.
- Given no line items that can be priced, every amount is `[TBD]`.

### R6 Revised contract sum

When the original contract sum is known, the document shows original + this PCO =
proposed revised sum. Otherwise it shows `[To Be Confirmed]`.

**Met today:** no. The form never asks for the original contract sum, so it's always
`[To Be Confirmed]`.

### R7 Validity date

"Valid Through" is 21 days after the PCO's date.

**Met today:** no. It's counted from the day the document is generated, not from the
date on the PCO.

### R8 Fixed contract language comes from code

The Contract Modification, Validity and Authorization paragraphs are fixed text with
the project's values filled in. The model never writes them.

**Met today:** no. The model is told to reproduce them word for word.

**Acceptance criteria**
- The Authorization paragraph is the same in every document.
- It says no work starts before the PCO is signed, and nothing about T&M billing on
  verbal or unsigned direction.

**Met today (T&M clause):** no. v3's Authorization paragraph includes it.

### R9 Deliver and keep nothing

Both files are emailed to the address on the form. Nothing is kept on the server after
the response.

**Met today:** yes. Files go to a temporary directory that's deleted when the request
ends.

### R10 Limit abuse

At most 10 requests per IP per hour and 200 per IP per day.

**Met today:** yes, counted in memory with a single worker, so the count resets
whenever the worker restarts (every 10 requests, per the Procfile).

### R11 Fail without leaking

When generation or email fails, the user sees a plain message. Internal errors and
exception text stay in the server log.

**Met today:** no. The 500 response returns `str(e)`.

## Boundaries

- **Not in the domain:** a company's own rates, templates or contracts; executed change
  orders; approval tracking; anything stored after delivery.

## Known gaps

- **Original contract sum** isn't collected. Add a form field, or drop the section?
