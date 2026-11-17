---
type: readme
status: current
---

# Agents

Small agents built to learn, and to show, how agent loops work. The first is the job
evaluator: Claude reads a job posting and decides which tool to use, and Python runs
the tools, applies the hard rules in code, and keeps the conversation.

**Status:** active, learning project  
**Code and docs:** [`agents`](https://github.com/justinyurasits/agents)

This is a linked project. Its docs live next to its code, because every pull request
updates them: the design doc has to match `agent.py` on `main`, and each PR writes its
own build-log and decision-log entries.

## Job evaluator — read in this order

| Concept | File | What it answers |
| --- | --- | --- |
| Brief | [`docs/BRIEF.md`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/docs/BRIEF.md) | What it does, for whom, and what v1 covers |
| Design | [`docs/SPEC.md`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/docs/SPEC.md) | How the agent works and why; kept in step with the code |
| Decisions | [`docs/DECISIONS.md`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/docs/DECISIONS.md) | Every design decision, with the options and the reasoning |
| Plan | [GitHub issues](https://github.com/justinyurasits/agents/issues) | What's left; each change starts as an issue |
| Build log | [`docs/BUILD_LOG.md`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/docs/BUILD_LOG.md) | What happened, what broke, and what it taught |
| Learnings | [`LEARNINGS.md`](https://github.com/justinyurasits/agents/blob/main/LEARNINGS.md) | What building these agents has taught, across agents |

`SCENARIOS.md` and `STEPS.md` in the same folder are generated from code and drive the
replay page. They aren't design docs.
