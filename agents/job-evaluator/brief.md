---
type: brief
status: current
---

# job-evaluator — Product brief

One page. Every milestone and issue should trace back to a line here. If it doesn't, it's post-v1.

## What it is

A learning and demonstration tool: an interface where you watch a simple agent work, step by step.

It runs nine prepared scenarios in two groups, each chosen to show a different agent behavior (D21; the list is `scenarios/scenarios.json`, shown in [SCENARIOS.md](https://github.com/justinyurasits/agents/blob/main/job-evaluator/docs/SCENARIOS.md)):

**Normal runs**

1. **Clean run** — complete posting, one tool, done.
2. **Missing info** — no comp listed; Claude picks a different tool.
3. **Multi-tool** — a tool's result changes what the agent does next.
4. **Two tools at once** — Claude asks for two tools in one reply; both results go back together.
5. **Hard screen in code** — code rejects the posting before the grader is ever asked.

**Break the agent** (a fault is injected on purpose and labeled on the page)

6. **A tool fails** — the error goes back to Claude, and the agent recovers.
7. **Unknown tool** — Claude asks for a tool that doesn't exist; Python answers with the real ones.
8. **Runaway loop stopped** — a tool keeps failing and the loop cap stops the run.
9. **Reply cut off** — Claude's reply runs out of room; the run stops with a clear message.

Scenario 6, a tool fails (numbered 4 when D16 was written), was built end to end first (D16, page v0 #57), then the rest.

Each run plays out at a readable pace, with a short pause between major steps. Every step shows what's happening in plain English, the line of code running, and the data at that moment.

The job evaluation is the scenario. The product is visibility into how an agent works.

## Who it's for

- **People learning how agents work** — anyone who wants to see a real agent loop, not a diagram of one.
- **People evaluating my work** — hiring managers, recruiters, potential clients. They should come away thinking "that's actually really cool," and be able to follow the link from any step to the code, the issue, or the decision behind it.
- **Me** — building it is how I learn this properly.

## The moment that matters

When I walk someone through it — in an interview, a client conversation, or a training class — and the page carries the explanation: what the agent decided, why the run took the path it did, and how it handled the error.

## What's on the page

One long page in eight sections (D36). A header bar links to each one, by the
names below. Every claim the page makes can be watched: "Watch it" buttons
load the matching scenario into the run view at step 1, paused, and scroll to
it.

1. **Inside the agent loop** (the hero) — one line on what this is, my name,
   and a **Watch it run** button that jumps to the run.
2. **What's an agent** — three sentences and a small loop diagram: the model
   decides, code runs the tool, the result goes back, repeat until done.
   "Claude decides; Python executes" lives here.
3. **How this agent works** — the four parts (Python, Claude, the tools, the
   grader), the loop, and the tools, each with a line on when it's used.
   Watch it buttons for scenarios 1, 3 and 4.
4. **Scenarios** — nine cards in two groups (Normal runs / Break the agent),
   each with its setup line and the tools the run calls, worked out from its
   recording (D39). Clicking a card loads that run.
5. **The run** — the Execution Explorer: a scenario chooser in the same two
   groups, playback that starts paused, an intro before the run (the setup,
   without the ending, and what to watch for), and a summary card on the last
   step saying what happened and why it matters (D37). Both are labelled
   "Written for this page".
6. **Design principles** — seven, as one table: the principle, the part of
   the agent that applies it, and Watch it (#80). Every guard is listed under
   the principle it serves (D40): watch the ones a scenario shows; the rest
   are marked "Tested, not demonstrated" with the test that proves them.
   1. The model for judgment, code for rules (scenario 5)
   2. Tool choice is intent classification, so state precedence (scenario 2)
   3. Errors go back to the model as information (scenario 6)
   4. Fail closed on the unknown (scenario 7)
   5. Bound the loop (scenario 8)
   6. Smaller questions get more reliable answers (scenario 1)
   7. The conversation is the memory (scenario 1)
7. **How it was built** — for people evaluating the work: I wrote the first
   version by hand to learn the loop, then Claude Code wrote the code from my
   issues while I made the decisions and reviewed every change. The workflow,
   numbers counted from the repo (tests, scenarios, guards, decisions, merged
   pull requests; D41), "Show what happened; label everything else", and
   links to the repo, CLAUDE.md, DECISIONS.md and LEARNINGS.md.
8. **About** (the footer) — my name, one line, and the repo. A contact link
   comes later.

## The four questions (page design rule)

At every step, a viewer can answer four questions: Who is executing? What information do they have? What caused this? What happens next?

## Truthfulness rule

The page shows what actually happened and labels everything else.

- Recorded data (requests, responses, tool calls, results, errors, Claude's returned thinking) comes only from real runs.
- Teaching explanations are written separately and labeled "written for this page." The page never presents its own explanation as Claude's.
- Simulated failures are labeled on the page.

## Non-goals (v1)

- Not a job-search or resume-evaluation tool.
- Visitors can't enter their own job, profile, or data. It runs the prepared scenarios only.
- No accounts, no saved data.
- No rich evaluation output (THE_METHOD-style). The evaluation only needs to be believable.
- No multi-agent.

## How we'll know it worked

- I use it to explain how an agent works to a hiring manager or potential client.
- I can use it as a demo in a training class.
- A first-time visitor can say who decides, who executes, and how information moves after watching one run. (Test on two people before publishing.)

## Constraints

- **Time box:** two weeks from M2 start to public link.
- **Must never fail in a live demo.** No dependence on an API call succeeding while someone is watching.
- **Near-zero running cost.**
- **Free hosting** (GitHub Pages, D12).
- **Every recorded run is real:** produced by the actual agent, with the trace file linked.
- **Fictional companies only** in scenarios; no real company paired with an invented posting.

## Decided

- Recorded runs only; static page (D12).
- Seven scenarios; failures forced with labeled switches (D13, superseded by D21).
- research_company uses stored company data (D14).
- Run view: Execution Explorer, linear map (D15).
- Scenario 4 first (D16); now scenario 6, after renumbering.
- Tests use the standard library's unittest (D17).
- A tool's exception goes back to Claude as an `is_error` tool result (D18).
- An unknown tool name gets an error listing the real tools (D19).
- Several tool requests in one reply run in order, with one result message (D20).
- Nine scenarios: 5 normal runs + 4 break-the-agent runs (D21).
- A cut-off reply is never acted on (D22).
- Code references come from `# STEP:` markers, never hand-written line numbers (D23).
- Trace format: one flat event per step, every key always present (D24).
- Every guard check is recorded; "caught" means something went wrong (D25).
- A failed call to Claude stops the run, naming only the error type (D26).
- Faults are injected into real runs and labeled; the cap is lowered for the runaway demo (D27).
- Hard rules in code; the grader answers one yes/no question (D28).
- A stop reason the agent doesn't handle stops the run (D29).
- Recordings are checked against each scenario's `expect` (D30).
- Page v0 lives in `job-evaluator/site/`, ships its fonts, and shows Claude's words only under "Claude's response" (D31).
- Page steps: passing checks aren't steps; caught checks and "Claude says it's done" are (D32).
- One page, a "Watch it" button on every claim (D33; its section list superseded by D36).
- Researched pay: code recognises pay that research_company found and labels it "base estimated from stored company data"; evaluate_job's inputs don't change (D34).
- The page's scenario chooser is a drop-down in two groups; each pick is a browser history entry, and `?scenario=N` opens a scenario (D35).
- Each run has an intro before it (setup, watch for, never the outcome) and a summary card on its last step, both tested against the recordings (D37).
- Page structure: eight sections, with principles after the run; "Watch it" loads a scenario at step 1, paused, and scrolls to the run (D36).
- Scenario cards show each run's full tool path, worked out from its recording; a card's own words never state the rating (D39).
- Each guard is listed once, under the principle it serves: errors go back to the model (E1, E5, E8), fail closed on the unknown (E2, E3, E6, E7, E9), bound the loop (E4) (D40).
- Every number in How it was built is counted from the repo by `build_numbers.py`, never typed; the page links to this repo on GitHub (D41).
- Tool precedence goes in the description of the tool that should wait: `flag_for_review` says to try `research_company` first when pay is missing (D42).
- Browser tests check the page's rules in Chromium (Playwright, a dev-only requirement) and skip when it isn't installed. Claude's words are searched in every tab but its own; the only exemption is tool_result content in Payload (D38).
- The design docs live only in the design repo; agents finds it with one lookup, `design_path()`, beside the main checkout, so worktrees find it too (D47).
- Without the design repo, the doc tests fail with "clone justinyurasits/design next to agents"; they never skip (D48).
- The page's doc links are checked where they point: at least 3 into agents, at least 2 into design (D49).
