---
type: readme
status: current
---

# Agents

Small agents built to learn, and to show, how agent loops work. One component per
agent. The first is the job evaluator: Claude decides which tool to use, and Python runs
the tools, applies the hard rules in code, and keeps the conversation.

**Status:** active, learning project  
**Code:** [`agents`](https://github.com/justinyurasits/agents) ·
[replay page](https://justinyurasits.github.io/agents/job-evaluator/site/)

## Product-level docs

| File | What it is |
| --- | --- |
| [brief.md](brief.md) | Why this repo of agents exists and what it's for. Draft. |
| [principles.md](principles.md) | What building these agents has taught, each lesson tied to where it came from (was `LEARNINGS.md` in the agents repo). |

## Components

| Component | Folder | What it is |
| --- | --- | --- |
| Job evaluator | [job-evaluator/](job-evaluator/) | Reads a job posting and rates it, looks up the company, or flags it for a person. Nine recorded scenarios replay step by step. |

## How these docs work

All files here are written in this repo and edited by pull request; none is synced from
Claude Docs yet. The agents tests read `job-evaluator/design.md` (the error table, the
design principles and the decision log), so a change there can make agents CI fail until
the code matches. That's on purpose: design leads, code follows.
