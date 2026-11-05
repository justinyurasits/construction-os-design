---
type: spec
status: current
---

# Document workbench — Spec

The workbench's domain is a company's **governed document library**: its policies, procedures, controls, contracts, forms and the structured data that drives generation. The library lives in [`construction-os-corpus`](https://github.com/justinyurasits/construction-os-corpus). Today that repository is Beacon Hill Interiors' package, and it's the starting point every later company copy will be forked from.

This spec names and bounds the domain and points to where each part is defined. It doesn't restate the library's rules. They are written once, in the library, and this file only says where.

## What the library holds

| Part | Where | What it is |
| --- | --- | --- |
| Governed documents | `docs/` | 173 Markdown documents in 23 collections by ID prefix. The largest are SUB (22), FCM (20), PRO (18), PRE (13), CLO (12), SYS (11) and CON (11). Kept `.docx` files sit beside forms, contracts and templates. |
| Parameter definitions | `registry/` | One YAML file per configurable item (24 today), each with type, default, constraints, authority and onboarding question |
| Company values | `company/config.yaml`, `company/bhi/profile.yaml`, `company/pricing/` | This company's values for the registry, its identity, and its rate tables |
| Document definitions | `definitions/` | What a generated document must contain and which rules it depends on. Only `CHG-53-DEF.yaml` (the potential change order) exists so far. |
| Templates | `templates/` | Word masters and brand assets, such as `pco.docx` |
| Sample drafts and expected results | `samples/` | Structured PCO drafts the renderer and acceptance tests read |
| Fork point | `STARTER_RELEASE` | Which starter release this copy came from. This copy is the original. |

## Where the domain's rules are defined

| Question | The authoritative source |
| --- | --- |
| What kinds of document exist, and how each is used | `docs/SYS-00` §3 (nine document types) |
| Which source governs when two disagree | `docs/SYS-00` §4 (authority order and conflicts) |
| How a company configures the library | `docs/SYS-00` §5 (layers, defaults, overrides, company configuration and profile) |
| What every document declares about itself | `docs/SYS-00` §6 (front matter, identifiers, writing rules) |
| How a document changes | `docs/SYS-00` §7 (statuses, versions, releases, checks) |
| The firm-wide rules (authorization, spending limits, billing and others) | `docs/POL-01`, 12 rules with permanent IDs |
| What a PCO must contain and depend on | `definitions/CHG-53-DEF.yaml` and the registry entries it lists |

Why these rules are shaped the way they are is in [design.md](design.md) and its decision log. The universal reasoning behind them is in the project's [principles.md](../principles.md).

## Boundaries

- **In the domain:** knowledge the company governs and maintains: documents, registry values, definitions, templates.
- **Not in the domain:** anything supplied for a single request, such as an executed project contract, PM notes or a subcontractor quote. These are used for that request and never stored as company knowledge (principle 10).
- **Not in the domain:** project records. They stay in Procore or Buildertrend (Product Brief, section 5).
- **Not in the domain:** the application. Code lives in [`document-workbench`](https://github.com/justinyurasits/document-workbench) and holds no company content.

## What the audit found

The library's measured state is in `reports/` in the corpus repository. Each report is a dated baseline; GitHub issues track the fixes.

| Report | What it measures |
| --- | --- |
| `remediation.md` | Every known conflict retested against POL-01: open, resolved, changed, and new |
| `config_inventory.md` | The configurable values found in prose, the source of the registry |
| `pco_family_map.md` | Every document a PCO touches, its role and its dependencies |
| `stage_map.md` | Which project stage each document applies to |
| `doc_references.md` | How old numeric references were mapped to document IDs |
| `document_types.md`, `front_matter.md`, `layer_classification.md` | How each document was classified when governance was added |

## Known gaps in the source

- **SYS-00 §5.1 still describes merging three layers at runtime** ("company first, then jurisdiction, then core"). The adopted model gives each company a complete copy of the library and treats layers as labels only (design.md decision log, Nov 2; principle 6). SYS-00 needs a version update to match. Until it has one, the design decision governs.
- **No document declares what it controls.** A planned `governs` front matter field would list the rule or decision IDs each document owns (plan.md, future work).
- **Only one document definition exists.** Other document types are generated from procedures until their definitions are written.
