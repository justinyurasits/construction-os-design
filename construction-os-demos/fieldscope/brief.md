---
type: brief
status: current
---

# Fieldscope — product concept
*Working name. Sub safety compliance, scoped and verified — not a binder of boilerplate.*

## Positioning

Every sub on a large GC's jobsite is required to have a safety protocol, a training record, and daily PPE compliance. In practice, all three degrade into paperwork nobody trusts. Fieldscope replaces the paperwork with three things that are actually true: a protocol scoped to the task being performed, a review record with a real timestamp, and a compliance status backed by a photo — for every sub, on every site, every day.

## The problem

The same three gaps show up across sites and subs, at every scale:

| Gap | What actually happens today |
|---|---|
| **Documentation** | Protocols aren't scoped to the work being performed. Subs default to generic boilerplate instead of a protocol matched to the actual task, so it gets ignored. |
| **Training & review** | No reliable way to confirm initial safety reviews happened — or that ongoing reviews are running on schedule, not just checked off a list. |
| **Verification** | No fast way to confirm PPE and site conditions match the requirement, on any given day, across dozens of subs and sites. |

None of these are training problems. They're the predictable result of compliance running on paper and memory at a scale that doesn't support either.

## Who it's for

- **Buyer**: Corporate EH&S / Risk Management — holds budget and cares about a defensible record across the whole portfolio, not one site.
- **Champion & pilot validator**: Project Safety Manager, embedded on one active site — the daily user whose trust the pilot has to earn.
- **Site user**: Superintendent — reviews and routes flagged status, spot-checks the record, doesn't want a new system to babysit.
- **Field user**: Subcontractor's competent person / safety representative — describes the task and submits the daily photo. This has to work in under a couple of minutes with zero training, or the entire compliance record downstream is fiction.

*(Full reasoning in [personas.md](#personas).)*

## How it works

1. **Describe** — before work starts, a foreman or superintendent describes the task in plain language. No form.
2. **Generate** — the system returns a protocol scoped to that task, grounded in the applicable OSHA 1926 sections — not a generic template.
3. **Track** — an initial review and ongoing review cadence are set automatically, with a training curriculum matched to the task. Completion is tracked as real state, so "did this happen" has an actual answer.
4. **Validate** — a daily jobsite photo is checked against that protocol's required PPE and equipment. Compliant or flagged status returns same-day.
5. **Roll up** — safety leadership sees status across every sub, site, and trade in one view — and every status is backed by the specific protocol and photo behind it, not a checkbox.

## Why this, why now

- A protocol scoped to the actual task is the difference between something a foreman reads and something a foreman ignores.
- "Did the review happen" stops being a memory problem when it's timestamped, tracked state instead of a form in a binder.
- Verification only scales if checking PPE across dozens of subs is a photo-pipeline problem, not a walk-the-site problem for one safety manager.

## Non-goals (v1)

- **Not a system of record for OSHA recordkeeping** (300 logs, incident reporting). Complements existing EHS/compliance systems, doesn't replace them.
- **Not a substitute for accredited safety training providers.** Curriculum guidance and tracking, not certified course delivery.
- **Not continuous monitoring.** Daily photo-based spot verification, not live video surveillance — a deliberately different (and more defensible) claim.
- **Not full-corpus OSHA 1926 coverage on day one.** Scoped to the trades in the pilot; expands deliberately, the same way the original concept frames it.
- **Not multi-language in v1.** Photo verification is visual and language-agnostic already; protocol text starts English-only, with translated summaries as a fast-follow rather than a pilot blocker.

## Pilot scope

Not a build-first pitch — a scoping conversation, then a narrow pilot:

1. **Confirm the gap** — which of the three (documentation, training, verification) is costing the client the most today, and on which sites. This is the client's call, not ours.
2. **Pilot narrow** — one site, 1–2 trades, real protocols, real photo validation. Suggested starting point: electrical and scaffolding — both show up disproportionately in OSHA's most-cited standards, so the gap is easy to make visible fast.
3. **Expand deliberately** — extend across subs and sites once the pilot shows the compliance record holds up under the safety manager's own spot-check.

**Draft pilot success criteria** (refine with client):
- A protocol generated for 100% of task types started on-site during the pilot window
- ≥90% of daily verification photos returning a same-day status
- The safety manager independently confirms the record matches what they'd find walking the site themselves

## Working assumptions (to validate with Turner, not blockers)

| Question | Assumption |
|---|---|
| Which trade/site to start with | Electrical and scaffolding on one active project — structurally different hazard profiles (Subpart K vs. L/M), and both show up disproportionately in OSHA's most-cited standards, so the gap is fast to demonstrate. |
| Foreman-driven or superintendent-driven photo submission | Submission sits with the sub's competent person/safety rep — they're on-site with the work daily. Superintendent gets rollup visibility, not submission duty. |
| Do compliance records need to live inside Turner's existing systems | Standalone for the pilot, deliberately — reduces integration risk and timeline. Integration with whatever Turner runs today (Procore, HammerTech, or otherwise) becomes a real conversation only once the pilot earns the right to expand. |
| Non-English-primary crews | Not a pilot blocker — see non-goals above. |
| Does a flagged status need an escalation/notification workflow | Yes, at minimum a notification to the Project Safety Manager. A flag nobody sees isn't a same-day answer, it's a log entry. |
| Who marks a flagged status resolved | The Project Safety Manager, after a corrected photo or a documented override — not the sub. Self-clearing would undercut the record's whole reason for existing. |
| Internal terminology | Use "competent person" and "safety representative" — OSHA-standard terms Turner already uses — rather than inventing new labels. |
| Who holds budget | Corporate EH&S/Risk, with the Project Safety Manager as the on-the-ground champion making the case upward. |

---

*This concept is deliberately narrow. The three non-negotiables for a credible pilot: protocols that visibly reflect the actual task (not templated), a review cadence with real timestamps, and photo verification with a same-day answer. Everything else — the dashboard, the rollup, the polish — supports those three and shouldn't be allowed to become the point.*

---

## Personas

*Moved here from `docs/personas.md`, unchanged below its title: Fieldscope — personas, pains, gains.*
*Confidence key: 🟢 confirmed by research · 🟡 reasonable inference · 🔴 open, needs a real Turner conversation*

### Context that changes the earlier concept doc

🟢 Turner already runs a real safety program: project-embedded "Project Safety Manager" roles under a corporate EH&S department; subs with 5+ workers submit OSHA outreach training cards; supervisory/competent-person staff hold OSHA-30; crews over 30 require a dedicated full-time safety supervisor; weekly toolbox talks and site-specific orientations are standard.

🟢 Turner carries real legal exposure here, not just an efficiency problem: under OSHA's multi-employer citation policy, a general contractor can be cited as the "controlling employer" for a subcontractor's violation if it knew, or reasonably should have known, and failed to act. An outdated or unchecked written protocol is a liability record, not paperwork.

🟡 This means Fieldscope's honest pitch is "documentation and verification layer under your existing program," not "we'll bring you a safety program." A Project Safety Manager who's actually run OSHA-30 orientations will see through anything that implies otherwise immediately.

---

### Persona 1 — Project Safety Manager (primary champion, day-to-day user)

🟢 Real, project-embedded role: enforces site compliance with company EH&S programs and regulations, trains subs and Turner trade staff on safe work practices, maintains relationships with subcontractor safety representatives, drives corrective action on unsafe conditions, develops and enforces the project safety program. Reports functionally into corporate EH&S. Bachelor's degree typical, ~4+ years experience, salaried.

🟡 **A day in their life**: splits time between walking the site, reviewing sub safety documentation, running or coordinating the weekly toolbox talk, chasing down corrective actions, and fielding whatever just went wrong. With dozens of subs active on a large job simultaneously, verifying that each sub's protocol is actually scoped to their current task — not the boilerplate submitted at bid time — is a manual document-review problem that doesn't scale with headcount.

🟡 **Pain**: confirming PPE and site-condition compliance across every crew, every day, means physically walking the whole site or trusting whatever the sub self-reports. Neither one gives a timestamped record that holds up later.

🟡 **Gain**: a same-day, photo-backed answer to "is this crew compliant right now" across the whole site, without becoming a full-time inspector — and a protocol library that's visibly scoped to the actual work, so subs stop treating it as a box to check.

🟡 **JTBD**: *When a new task or a new sub starts on my site, I need a protocol that's genuinely scoped to that work and daily evidence that it's being followed, so that if there's ever a citation hearing or a claim, I have a real record instead of a signature on a generic form.*

🔴 **What earns trust**: almost certainly needs to review and approve an AI-generated protocol before it's "official," not have it go live automatically — worth confirming directly, but no safety professional signs off on something they haven't seen first.

---

### Persona 2 — Superintendent (secondary user, escalation point)

🟡 Owns schedule and site operations; accountable for what happens on the site day to day, but safety is one responsibility among many, not the primary credential. Less likely to be OSHA-30/CHST-certified than the Project Safety Manager.

🟡 **Pain**: gets pulled into safety issues reactively — an incident, a stop-work, an OSHA visit — rather than having a standing read on compliance status. Doesn't want another system to babysit; wants a status they can glance at and act on.

🟡 **JTBD**: *When I'm deciding whether a sub can start or keep working, I need a fast, trustworthy read on whether they're actually compliant, so I'm not choosing blind between holding the schedule and taking on risk I can't see.*

---

### Persona 3 — Corporate EH&S / Risk Management (likely actual buyer)

🟡 Sets company-wide EH&S policy that Project Safety Managers execute at the project level. For a tool meant to work the same way across multiple projects, this is probably the real budget owner — the Project Safety Manager is the champion and daily user, not necessarily who signs off on a company-wide rollout.

🟡 **Pain**: safety documentation currently lives project-by-project, sub-by-sub. No portfolio-level view of which subs across active projects have stale protocols, overdue reviews, or unresolved flags. Every incident or OSHA inspection turns into an ad hoc document hunt across whichever project it happened on.

🟡 **Gain**: a defensible, consistent record across every active project — turning "controlling employer" exposure into something actively managed rather than discovered after an incident.

🟡 **JTBD**: *When I need to demonstrate a consistent, defensible safety record across our whole portfolio, I need one place where every sub's protocol, training, and verification status is visible, so our liability exposure is something we manage, not something we find out about.*

🔴 **Open**: is this actually one role, or does it split between EH&S (program) and Risk/Legal (liability, insurance, claims)? Worth asking directly — the pitch may need two buyer-side messages, not one.

---

### Persona 4 — Subcontractor Safety Representative / Competent Person (field user, makes-or-breaks adoption)

🟢 Every trade on a Turner site is required to have a designated competent person; per OSHA rules, that person must be capable of identifying hazards and has authority to correct them.

🟡 On smaller subs, this is very often the foreman wearing a second hat, not a dedicated safety hire — meaning zero appetite for anything that takes real time away from running the crew.

🟡 **Pain**: safety paperwork competes directly with getting the actual work done. If it's not fast, it gets skipped or backfilled after the fact — which quietly defeats the entire point of a timestamped record.

🟡 **JTBD**: *When I start a task or a new day on site, I need to satisfy Turner's safety requirement without it eating real time from running my crew, so my guys stay compliant without me becoming a paperwork person.*

🟡 **What earns adoption**: this persona's tolerance for friction is close to zero. If describing a task or uploading a photo takes more than a couple of minutes, this is the persona that determines whether Fieldscope's entire compliance record is real or fiction — they're the one generating the data everyone else depends on.

---

### What this changes about who we pitch first

🟡 The original concept doc treated "the client" as one undifferentiated buyer. It's probably at least two conversations: **Corporate EH&S/Risk** for the portfolio-level case and budget, **a Project Safety Manager** on one active site for the actual pilot validation. Pitching only the corporate side risks a tool nobody on the ground trusts; pitching only the project side risks a pilot that never gets budget to expand.

### Working assumptions (resolved, not left open — validate with Turner when there's a real conversation)

| Question | Assumption | Persona it affects |
|---|---|---|
| Internal terminology | "Competent person" and "safety representative" — Turner's own OSHA-standard language, not invented product terms | All |
| What they use today | Assume a mix: Procore or similar for project management broadly, likely a point solution or paper for sub-level safety documentation specifically. Fieldscope launches standalone; integration is a post-pilot conversation | Sets scope, not blocking |
| Who holds budget | Corporate EH&S/Risk — the Project Safety Manager is the on-the-ground champion who makes the case upward, not the buyer | Determines who we pitch first |
| Flagged photo check — notify or stay passive | Notify the Project Safety Manager. A flag nobody sees isn't a same-day answer | Project Safety Manager, Superintendent |
| Who clears a flagged status | The Project Safety Manager, after a corrected photo or documented override — not the sub itself | Project Safety Manager, Sub Safety Rep |

---

### How this works across many subs on one large job

A large Turner job doesn't have one sub to track — it has dozens, overlapping, mobilizing and demobilizing on different schedules, several doing more than one distinct scope of work over the life of the project. The model has to hold up at that scale, not just for the one sub in a demo.

**The unit of record is a task, not a sub.** An electrical sub doing rough-in in month two and trim-out in month eight has two different hazard profiles and two different protocols — not one static "electrical protocol" that goes stale the moment the actual work changes. A sub can have several active protocols at once if they're running more than one scope of work simultaneously.

**The roster is a state, not a list.** Subs mobilize and demobilize continuously. The dashboard's default view is "active on site today," not every sub Turner has ever worked with — a demobilized sub's history stays in the record but drops out of daily triage.

**Triage, not a feed.** With 30+ subs checking in daily, a Project Safety Manager cannot read 30 photo results every morning, and won't. Compliant checks clear quietly into the record. The default dashboard view surfaces only what needs a human: flagged checks, overdue reviews, and tasks with no check yet today. This is the same shape as any ops tool at scale — exception-based review, not a log to page through.

**Shared equipment stays attached to the sub that owns it.** A scaffold erected by the masonry sub but used by three other trades isn't modeled as a shared object in v1 — that's real complexity better earned later. The erecting sub's protocol covers erection and inspection; any sub whose own task depends on that scaffold has "access to a compliant structure" as one of their own required-equipment items, checked in their own daily photo. Simpler to build, and it keeps accountability where OSHA already puts it — with the employer controlling that specific hazard.

**Recurring subs are a v2 idea, not a v1 feature.** Turner works with the same subs across many jobs. A sub profile that carries training history and compliance record from site to site is the obvious next step once there's more than one active project — but building that before there's a second pilot site to prove it against is solving a problem we don't have data for yet.

**What this means for the dashboard, concretely**: grouped by trade or by "needs attention today," not a flat alphabetical list of every sub. A Project Safety Manager should be able to open it in the morning and see, in order: overdue reviews, flagged checks from yesterday, tasks with no check yet — then everything else quietly compliant underneath.
