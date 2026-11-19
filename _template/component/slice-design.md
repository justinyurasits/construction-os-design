---
type: slice-design
status: draft
---

# Project name — Component name <Slice> Design

*The build design for one vertical slice: enough that someone can build it without
asking. Name the file `<slice>-design.md`. One file per slice.*

## What the slice produces

*The output, for which user, from which inputs. One worked example, start to finish.*

## Components

| Part | Responsibility | Module or file |
| --- | --- | --- |
| *<part>* | *<its one job>* | *`<path>`* |

## Data and interfaces

*Schemas, inputs and outputs between parts, and which are deterministic.*

## Acceptance tests

| Case | Input | Expected result |
| --- | --- | --- |
| *<name>* | *<request>* | *<what must come out, or be refused>* |

## Build order

1. *<step> — done when <check>.*
