---
type: product-spec
status: draft
---

# Project name — Product Spec

*What the product must do for its users, capability by capability, and how anyone can
check that it does. Behavior the user can observe, not implementation. The brief says
why; architecture.md says how the parts deliver each capability; each component's
spec.md says what that part must do. Optional by type; needed once a project has two
or more components.*

## 1. Product scope

*What the product delivers, in a few sentences, and where it stops. Link to the brief's
out-of-scope list rather than repeating it.*

## 2. Users and their goals

| User | What they need to accomplish | Brief goal it serves |
| --- | --- | --- |
| *<role>* | *<the outcome, in their words>* | *<row in brief.md §4>* |

## 3. Capabilities

*One heading per capability, with a stable ID in the heading:
`<PROJECT>-CAP-<nn>: <name>`. Issues, component specs and plans cite the ID, so it
never changes; the name after it can. Don't reuse a retired ID.*

### *PRJ-CAP-01: <Capability name>*

*What the user can do, and what they get back, in one or two sentences.*

**Acceptance criteria**
- *Given <situation>, when <the user does X>, then <what they observe>.*
- *With incomplete or wrong input: what the product asks for, refuses or flags.*

**Delivered by:** *[component spec](component/spec.md#requirement-name) · …*

*Split a capability into its own spec once it's big enough to manage on its own:
several journeys, complicated rules, or its own acceptance-test suite. Until then it
lives here.*

## 4. User journeys

### *<Journey name>*

1. *<what the user does first, and what they see>*
2. *<each step, naming the capability it uses: PRJ-CAP-01>*
3. *<where a person must approve>*

**When it goes wrong:** *missing information, a conflict with company policy, a
failure partway through: what the user sees, and what happens to their work.*

## 5. Cross-cutting requirements

| Requirement | What must hold | How it's checked |
| --- | --- | --- |
| *Security and isolation* | *<e.g. one customer's data never reaches another's request>* | *<test, review, validator>* |
| *Reliability* | *<…>* | *<…>* |
| *Performance* | *<…>* | *<…>* |

## 6. Open product questions

- *<question about how the product should behave> — who decides, and what it blocks.*
