---
type: architecture
status: draft
---

# Project name — Architecture

*Optional; needed once there are two or more components. How the parts fit together.
Each component's design.md holds its own internals and decisions; this doc holds what
crosses component boundaries.*

## Terms

| Term | Meaning |
| --- | --- |
| *<term>* | *<definition used everywhere in these docs>* |

## The parts

| Part | Responsibility | Repository |
| --- | --- | --- |
| *<component>* | *<the one job it owns>* | *`<product>-<part>`* |

*A diagram of the parts and what calls what, exported to images/ when it changes.*

## How each capability is delivered

| Capability | Parts involved | Hand-offs |
| --- | --- | --- |
| *[PRJ-CAP-01](product-spec.md#prj-cap-01-capability-name)* | *<components>* | *<what passes between them>* |

## One request, start to finish

1. *<what arrives, and where>*
2. *<each hand-off between parts>*
3. *<what comes out, and who approves it>*

## Boundaries and authority

*What each part may and may not do. Where a human must approve. Which source wins when
two disagree.*

## Product-level decisions

| Date | Decision | Why | What would change it |
| --- | --- | --- | --- |
| *<date>* | *<decision>* | *<reasoning, options considered>* | *<the evidence that would reopen it>* |
