---
type: readme
status: current
---

# Job evaluator

An agent that reads a job posting and rates it. Claude decides which tool to use (rate
it, look up the company, or flag it for a person); Python runs the tools, applies the
hard rules in code, and keeps the conversation. Product-level docs are one folder up.

## Where things stand

Built and live: nine scenarios (five normal runs, four with a failure injected on
purpose) are recorded from real runs and replay step by step on the
[replay page](https://justinyurasits.github.io/agents/job-evaluator/site/).

**Code:** [`agents/job-evaluator`](https://github.com/justinyurasits/agents/tree/main/job-evaluator)

## The docs

| File | What it is |
| --- | --- |
| [brief.md](brief.md) | What it does, for whom, and what v1 covers. |
| [spec.md](spec.md) | What it must do, with acceptance criteria. Draft: the requirements still live in the brief and design. |
| [design.md](design.md) | How the agent works and why, then the decision log (D1–D46 and lettered entries). The agents tests read it. |
| [plan.md](plan.md) | What's left. Draft: open work is tracked as issues in the agents repo. |
| [build-log.md](build-log.md) | Dated log of what was done, what broke, what it taught. |

Moved here from `agents/job-evaluator/docs/` on 2026-11-19 (design #26). `STEPS.md` and
`SCENARIOS.md` stayed in the agents repo: they're generated from code for the replay page.
