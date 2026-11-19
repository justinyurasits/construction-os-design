---
type: brief
status: draft
---

# PCO Generator — Brief

**Draft.** The audience and the purpose of the demo are still open (below and in the
[demos brief](../brief.md)).

## Who uses it, and when

A project manager or owner-operator at a small general contractor, standing on a job
right after something changed: rot under the tile, the owner wants the island 18 inches
longer, the architect revised a window. They have the facts in their head or in a voice
memo, and they need a document the owner will sign before the crew does the work.

## The painful moment

A change order decides whether work that's been done gets paid for. Project managers
write them under time pressure, so change work often gets done before anything is
authorized in writing, and change work is where margin gets lost most often. The
decision itself is quick. Producing the document is what takes the time.

## What it must make possible

The PM types or dictates what changed and, within a minute or two, gets an email with a
Potential Change Order (PCO) as a PDF to send and a Word file to edit. The PCO has
specific scope language, inclusions and exclusions, assumptions, a priced line-item
table with markup, schedule impact, the cause of change, and signature blocks. It's
labelled as a draft for the PM to review.

The prices have to be right. The PM's own numbers come first, and anything they didn't
price is filled from sample rates, labelled as such. Today the model calculates every
amount; the decided design moves that into code (not yet built). See
[design.md](design.md#4-decision-log).

## What it replaces

Starting from a blank Word template or an old change order, re-typing the project
header, writing scope language from scratch, and doing the markup math by hand or in a
spreadsheet.

## Out of scope

- Company-specific rules, rates, templates and approval flow: that's the governed PCO in
  Construction OS ([document workbench](../../construction-os/document-workbench/)).
- Executed change orders (the signed CO that modifies the contract), change event logs,
  and tracking whether the owner approved.
- Accounts, saved projects, or anything stored after the email is sent.
- Integration with Procore or other project management tools.

## Open

- Who uses the public tool today, and what it should lead them to: a conversation about
  Construction OS, a consulting engagement, or just the tool.
- How it relates to the governed PCO in Construction OS: a free way in, or a separate
  product.
