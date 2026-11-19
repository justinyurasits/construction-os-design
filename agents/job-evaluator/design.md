---
type: design
status: current
---

# job-evaluator — Design doc

How the agent works and why. Every statement here should match [`agent.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/agent.py) as it is on `main`, and the agents tests check parts of it (the error table, the design principles, the decisions the replay page cites). Design leads: a change to behavior, tools or prompts is made here first, then in the code. If the two disagree, say so; one of them has a bug.

Issue links point to [the repo's issues](https://github.com/justinyurasits/agents/issues). Decisions (D17, D18, …) are in the [decision log](#decision-log) at the end of this doc.

---

## Design principles

The seven principles the page demonstrates (#80, D36), the part of the agent that applies each one, and the guards that serve it. The page's Design principles table lists the same seven, guards and Watch it scenarios; `test_site.PrinciplesTest` fails if the two drift. Two earlier principles moved: "Claude decides; Python executes" is in the page's What's an agent section, and "Show what happened; label everything else" goes in How it was built (#81).

| Principle | In this agent | Guards | Watch it |
|---|---|---|---|
| **The model for judgment, code for rules** | `hard_screens` checks `REQUIRE_REMOTE` and `MIN_BASE` in code before the grader is asked; `RATING_FOR_ANSWER` turns the grader's yes/no into a rating (section 6, D28) | none | Scenario 5: a rule in code rejects the posting before the grader is asked |
| **Tool choice is intent classification, so state precedence** | Each tool's `description` in `tools` says when to use it (section 4). `research_company` and `flag_for_review` both cover a posting with no pay, so the tool that should wait says so: `flag_for_review`'s description ends "If compensation is missing, try research_company first; flag only if research finds no pay." (#91, D42) | none | Scenario 2: no pay listed, so Claude researches the company first, and flags the posting only when research finds no pay |
| **Errors go back to the model as information** | The `try / except` around each tool in `run_agent` sends the error back as an `is_error` tool result (section 5, D18) | E1 `tool_failed` (scenario 6); E5 `grader_cut_off`, E8 `invalid_grade` (tested, not demonstrated) | Scenario 6: the grader's reply is broken, the error goes back to Claude, and Claude retries |
| **Fail closed on the unknown** | An unknown tool gets an error listing the real tools (D19); a cut-off reply or an unhandled stop reason ends the run instead of being acted on (D22, D29) | E2 `unknown_tool` (scenario 7), E3 `reply_cut_off` (scenario 9); E9 `unexpected_stop`, E6 `api_call_failed`, E7 `no_final_answer` (tested, not demonstrated) | Scenario 7: Python answers a request for a tool that doesn't exist |
| **Bound the loop** | `MAX_PASSES` caps the outer calls to Claude; scenario 8 lowers it to 2 (D27) | E4 `pass_cap` (scenario 8) | Scenario 8: the tool always fails and the cap ends the run |
| **Smaller questions get more reliable answers** | The grader's `RUBRIC` asks one yes/no question about the work; pay and location are checked in code (D28) | none | Scenario 1: the grader's one question and its answer |
| **The conversation is the memory** | `messages` in `run_agent`: sent whole on every call (`send_to_claude`), and appended at `save_turn` and `results_back` (section 3) | none | Scenario 1: messages grows from 1 to 3 between the two calls |

---

## 1. Overview

Given one job posting as text, the agent returns a short written verdict:

- a **rating** (STRONG / WORTH REVIEWING / IGNORE) with reasons, when the posting has enough information, or
- a **flag for manual review**, when key information (compensation, remote status) is missing or unclear.

How a posting is rated (#26). Fixed rules are checked in code, and only the one question that needs judgment goes to the grader:

| Rating | Meaning | Decided by |
|---|---|---|
| IGNORE | not remote, **or** lowest base below $180K | code (`hard_screens`), before any rating call |
| STRONG | passes both, and the grader answers **yes** to "does this role build hands-on AI experience?" | the grader's answer, mapped in code |
| WORTH REVIEWING | passes both, and the grader answers **no** | the grader's answer, mapped in code |

A screen that can't be checked (remote status not given, or pay that isn't a readable yearly salary, like "competitive") is skipped, never failed, and the trace says so.

It's a small, deliberately visible agent. It was built to learn and demonstrate the agent loop, so every step prints a line to the terminal.

**Run it:** `python agent.py` from `job-evaluator/` (setup in [README.md](https://github.com/justinyurasits/agents/blob/main/job-evaluator/README.md)). It evaluates a built-in sample posting (Northwind Labs, remote, $200K–$240K), prints each step and the final answer, and writes a trace file to `traces/` (section 7).

Other ways to run it: `python agent.py --scenario <id>` runs a scenario from `scenarios/scenarios.json` (its posting, and its fault if it has one), and `python agent.py --fault <name>` forces one failure on purpose (see [Faults injected on purpose](#faults-injected-on-purpose)).

**Cost of a typical run:** 3 API calls when the posting gets rated (2 outer + 1 inside `evaluate_job`), 2 when it's flagged (`flag_for_review` makes no API call) or screened out by a hard rule (no grader call). Researching the company first (`research_company`, no API call) adds one outer call: 4 for a researched rating, 3 for research then a flag.

**What `run_agent` can return.** It always returns a string, one of the six kinds below, and callers can only tell them apart by the text:

| Case | Returned string |
|---|---|
| Claude finished (`end_turn`) | Claude's final answer (the reply's first text block) |
| Claude finished but wrote no text (e.g. only a thinking block) | `"Claude finished without writing a final answer."` |
| Claude's reply hit the token limit | `"Claude's reply was cut off (hit the max_tokens limit of 2000)."` |
| 10 passes without finishing | `"Stopped after 10 passes without finishing."` |
| The call to Claude itself failed (network, rate limit, overloaded, bad key) | `"Couldn't get a reply from Claude: <ErrorType> (status <code>). The run stopped."` (no status for network errors) |
| Claude stopped for a reason the agent doesn't handle (e.g. `refusal`) | `"Claude stopped for a reason this agent doesn't handle (stop_reason 'refusal'). The run stopped."` |

What it doesn't handle is in [Known limits](#9-known-limits).

---

## 2. Components

Everything is in one file, [`agent.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/agent.py). Top to bottom:

| Piece | What it is |
|---|---|
| `client`, `MODEL` | The Anthropic client (key from `.env`, loaded with `override=True`) and the model, `claude-sonnet-5-5`. |
| `MAX_PASSES = 10` | Most outer API calls per run. See the loop cap guard. |
| `MAX_TOKENS = 2000` | Longest reply Claude may write. Used by **both** API calls. |
| `tools` | The three tool definitions (name, description, input schema) sent to Claude on every outer call. The descriptions are how Claude decides which tool to use. |
| `MIN_BASE = 180_000`, `REQUIRE_REMOTE = True` | The hard rules, as named constants. |
| `lowest_base(text)`, `hard_screens(remote, compensation)` | Pure functions. `lowest_base` reads the lowest yearly base from Claude's compensation text (`"$140,000–$165,000"` → 140000; `"180-220k"` → 180000; `"competitive"`, `"$90/hr"` → `None`). `hard_screens` returns one result per rule: passed, failed, or skipped. |
| `RUBRIC` | System prompt for the grader call inside `evaluate_job`: the one judgment question, plus "Respond with JSON only: `{"answer": "yes" or "no", "reasons": [...]}`". It doesn't mention pay or location. |
| `RATING_FOR_ANSWER` | `{"yes": "STRONG", "no": "WORTH REVIEWING"}`: code, not the grader, turns the answer into the rating. |
| `strip_json_fences(text)` | Removes a surrounding ```` ``` ```` / ```` ```json ```` fence from the grader's reply. Pure string function. |
| `grade_problem(grade)` | A pure function that says what's wrong with the grader's parsed JSON (or `None`). A rule in code, not the prompt. |
| `evaluate_job(...)` | Tool. If the pay is researched (below), uses it and adds `"base estimated from stored company data"` to the reasons. Runs the hard screens first; if one fails, returns `{"rating": "IGNORE", "reasons": [...]}` with no API call. Otherwise makes its **own** Claude call with `RUBRIC` (no tools, no loop), parses the JSON reply, checks it with `grade_problem`, and returns `{"rating", "reasons"}` (or raises `ValueError` naming the problem). |
| `flag_for_review(...)` | Tool. Plain Python, no API call. Returns `{"status": "flagged", "company", "role_title", "missing_info"}`. |
| `research_company(company, role_level)`, `COMPANIES_FILE` | Tool (#65). Plain Python, no API call. Looks the company up in [`data/companies.json`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/data/companies.json), stored demo data (D14), ignoring case. Known: `{"found": true, "company", "size", "stage", "role_level", "typical_base_for_level", "note", "source": "stored demo data"}`; `typical_base_for_level` is the pay for the stored level whose word appears in `role_level` ("principal" in "Principal Product Manager"), or `null` with `levels_on_file`. Unknown: `{"found": false, "source": "stored demo data"}`, a normal result, not an error. |
| `SYSTEM_PROMPT` | Claude #1's system prompt, a constant so the call and the trace use the same text. |
| `run_agent(job_text, recorder=None, fault=None)` | The agent loop (next section). With a `Recorder`, it writes a trace (section 7). With a `Fault`, it fails on purpose in one way. |
| `SAMPLE_JOB`, `choose_run(argv)` | The built-in posting, and the command line (`--scenario`, `--fault`) turned into what to run. |
| `scenario_job_text(scenario)` | A scenario's posting, or its postings joined with a `---` line (`POSTING_SEPARATOR`). Used by `choose_run` and `record.py`. |
| `if __name__ == "__main__"` | Runs `choose_run`, then `run_agent`, and writes the trace. |

Next to it, [`code_refs.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/code_refs.py) finds the code each step points to. `agent.py` carries a `# STEP: <step_id>` comment directly above the code for each step in [STEPS.md](https://github.com/justinyurasits/agents/blob/main/job-evaluator/docs/STEPS.md), and `code_ref(step_id, source)` returns that code's current line number and full statement (D23). Nothing stores line numbers by hand, so editing `agent.py` can't make a reference go stale.

There are two Claude roles, and they never mix:

- **Claude #1, the agent** (outer calls in `run_agent`): sees the posting and the tools, and decides what to do.
- **Claude #2, the grader** (inner call in `evaluate_job`): sees one job summary and the rubric, and answers yes or no. Only postings that pass the hard screens get this far. Its conversation is thrown away when the tool returns.

Tests live in [`tests/`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/tests) (standard-library `unittest`, D17). Run them from `job-evaluator/` with `python -m unittest discover -s tests -v`. They use a fake Claude client, so they make no API calls and need no key. The page's browser tests ([`test_browser.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/tests/test_browser.py), #84, D38) also need Playwright and Chromium (`requirements-dev.txt`); without them they're skipped.

---

## 3. The loop

The step-by-step walkthrough, written for someone who has never seen an agent, is in **[STEPS.md](https://github.com/justinyurasits/agents/blob/main/job-evaluator/docs/STEPS.md)**. This section is the short technical version.

`run_agent` starts with one user message ("Evaluate this job posting: …") and then makes up to `MAX_PASSES` **passes**. A pass is one outer API call plus what follows it:

1. Send the system prompt, `tools`, and the **whole** `messages` list to Claude. Claude keeps no memory between calls; this list is the memory. If the call itself fails with an API error, return a message naming the error. **Done.**
2. Read the reply's `stop_reason`:
   - `end_turn` → return the reply's first **text** block (found by type, because a thinking block can come first), or the no-answer message if it has none. **Done.**
   - `max_tokens` → return the cut-off message. Nothing in the reply is acted on. **Done.**
   - `tool_use` → go on to step 3.
   - anything else (`refusal`, `pause_turn`, …) → return the unhandled-stop message. Nothing in the reply is acted on (D29). **Done.**
3. Append Claude's full reply to `messages` as the assistant turn.
4. Run **every** `tool_use` block in the reply, in order, each inside its own `try / except`.
5. Append **one** user message holding one `tool_result` per request, each carrying that request's `tool_use_id`.
6. Start the next pass.

If all 10 passes are used without `end_turn`, `run_agent` returns the cap message.

Tools run in order, not in parallel. The dispatch is an `if / elif` on the tool name inside the loop (D20).

---

## 4. What Claude sees

| | Claude #1: agent (outer call) | Claude #2: grader (inside `evaluate_job`) |
|---|---|---|
| **System prompt** | `"You help Justin triage job postings. Use the tools provided."` | `RUBRIC` (the one question + "Respond with JSON only: `{"answer": "yes" or "no", "reasons": [...]}`") |
| **Tools** | `evaluate_job`, `flag_for_review`, `research_company` (names, descriptions, input schemas) | none |
| **Messages** | The posting, then every assistant turn and tool result so far | One user message: `Company / Role` lines, then the description. Remote status and pay aren't sent separately: the hard screens already used them (#26). |
| **Limit** | `max_tokens = MAX_TOKENS` (2000) | `max_tokens = MAX_TOKENS` (2000) |

Claude #1 never sees `RUBRIC`. Claude #2 never sees the tool descriptions or the outer conversation.

**Tools as Claude #1 sees them:**

| Tool | Description (when to use it) | Inputs |
|---|---|---|
| `evaluate_job` | "Rate a job posting against Justin's criteria. Use when the posting has enough information to rate: company, role, location/remote status, and compensation." | `company`, `role_title`, `job_description` (required); `location`, `remote` (boolean), `compensation` |
| `flag_for_review` | "Flag a posting for manual review. Use when key information (compensation, remote status) is missing or ambiguous, so the job can't be rated reliably. If compensation is missing, try research_company first; flag only if research finds no pay." (the last sentence: #91, D42) | `company`, `role_title`, `missing_info` (all required) |
| `research_company` | "Look up stored facts about a company: size, stage, and typical base pay for a role level. Use when a posting doesn't list compensation." | `company`, `role_level` (both required) |

**Tool results as Claude #1 sees them:**

- Success: `content` is the tool's return value as JSON. There's no `is_error` field.
- Failure: `content` is `"<ExceptionType>: <message>"` and `is_error: true`. For example, `JSONDecodeError: Expecting value: line 1 column 1 (char 0)` or `ValueError: Unknown tool 'search_web'. Available tools: evaluate_job, flag_for_review, research_company.`

What Claude does after an error (retry, switch tools, or explain the failure) is Claude's decision, not the code's (D18). In live runs it has retried once and then explained the failure without inventing a rating. That's observed behavior, not a guarantee.

---

## 5. Guards and error handling

A **guard** catches a failure: a crash, a hang, or bad data. Each one is labelled `GUARD (E<n> <step_id>)` in agent.py and has an error step in STEPS.md (E1–E9). In order of their error steps:

| Guard | Step (`GUARD` label in agent.py) | Catches | Does | Issue | Test |
|---|---|---|---|---|---|
| **Tool errors** (`try / except Exception` around each tool) | E1 `tool_failed` | Any exception from a tool: bad JSON from the grader, bad arguments, the grader's own API call failing | Sends `"<Type>: <message>"` back as a `tool_result` with `is_error: true`; the run continues. Ctrl-C still stops the script. | [#8](https://github.com/justinyurasits/agents/issues/8), D18 | [`test_tool_errors.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/tests/test_tool_errors.py): `ToolErrorTest` |
| **Unknown tool** (`else` branch of the dispatch) | E2 `unknown_tool` | Claude asks for a tool name that isn't defined | Raises `ValueError("Unknown tool '<name>'. Available tools: …")`, which the tool-errors guard (E1) turns into `is_error`. The list comes from `tools`, so it stays in sync. | [#11](https://github.com/justinyurasits/agents/issues/11), D19 | [`test_tool_errors.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/tests/test_tool_errors.py): `UnknownToolTest` |
| **Cut-off reply, main loop** (`stop_reason == "max_tokens"` in `run_agent`) | E3 `reply_cut_off` | Claude #1's reply hit `MAX_TOKENS` | Returns `"Claude's reply was cut off (hit the max_tokens limit of 2000)."` Nothing in the reply runs, not even a tool request. | [#18](https://github.com/justinyurasits/agents/issues/18), D22 | [`test_max_tokens.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/tests/test_max_tokens.py): `test_cut_off_main_loop_reply_*` |
| **Loop cap** (`for … in range(1, MAX_PASSES + 1)`) | E4 `pass_cap` | Claude never says `end_turn`, e.g. it keeps retrying a tool that keeps failing | Stops after 10 outer calls and returns `"Stopped after 10 passes without finishing."` The grader's call doesn't count toward the 10. | [#15](https://github.com/justinyurasits/agents/issues/15) | [`test_loop_cap.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/tests/test_loop_cap.py): `LoopCapTest` |
| **Cut-off reply, grader** (`stop_reason == "max_tokens"` in `evaluate_job`) | E5 `grader_cut_off` | The grader's reply hit `MAX_TOKENS` | Raises `RuntimeError("The grader's reply was cut off …")` **before** parsing, so Claude gets "cut off" as an `is_error` result, not "invalid JSON". | [#18](https://github.com/justinyurasits/agents/issues/18), D22 | [`test_max_tokens.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/tests/test_max_tokens.py): `test_cut_off_grader_reply_is_reported_as_cut_off_not_invalid_json` |
| **Outer API call fails** (`try / except anthropic.APIError` around the call in `run_agent`) | E6 `api_call_failed` | Network error, timeout, rate limit (429), overloaded (529), server error, bad key (401) on Claude #1's call | Returns `"Couldn't get a reply from Claude: <ErrorType> (status <code>). The run stopped."` Only the error's type and status go in the message, never the error text, request, or headers. (The grader's own API errors are already tool errors, #8.) | [#30](https://github.com/justinyurasits/agents/issues/30), D26 | [`test_api_errors.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/tests/test_api_errors.py): `OuterApiErrorTest`, `TraceOfApiErrorTest` |
| **No final answer** (`if answer is None` after `end_turn` in `run_agent`) | E7 `no_final_answer` | Claude says `end_turn` but the reply has no text block (only thinking, or empty) | Returns `"Claude finished without writing a final answer."` instead of crashing with `StopIteration`. Several text blocks still return the first. | [#31](https://github.com/justinyurasits/agents/issues/31) | [`test_final_text.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/tests/test_final_text.py): `NoTextBlockTest`, `TraceTest` |
| **Grade check** (`grade_problem` + `if problem: raise` in `evaluate_job`) | E8 `invalid_grade` | Grader JSON that parses but isn't an answer: not an object, `answer` missing or not yes / no (any case is accepted), `reasons` missing or not a list of strings | Raises `ValueError` naming exactly what's wrong, which goes back to Claude as an `is_error` tool result (#8). A valid answer becomes `{"rating", "reasons"}`; other keys aren't passed on. | [#32](https://github.com/justinyurasits/agents/issues/32), [#42](https://github.com/justinyurasits/agents/issues/42), [#26](https://github.com/justinyurasits/agents/issues/26) | [`test_grade_validation.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/tests/test_grade_validation.py) |
| **Unhandled stop reason** (`if response.stop_reason != "tool_use"` in `run_agent`, after the cut-off check) | E9 `unexpected_stop` | A reply whose `stop_reason` isn't `end_turn`, `max_tokens` or `tool_use`: `refusal`, `stop_sequence`, `pause_turn`, `model_context_window_exceeded` | Returns `"Claude stopped for a reason this agent doesn't handle (stop_reason 'refusal'). The run stopped."` Nothing in the reply runs, not even a tool request, and no further request is sent. Before this, the reply went on to the dispatch, which sent a user message with empty `content` that the API rejects. | [#21](https://github.com/justinyurasits/agents/issues/21), D29 | [`test_unexpected_stop.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/tests/test_unexpected_stop.py) |

### Defensive handling (always on, not guards)

These never catch a failure; they prevent one. They run on every reply, the same way whether or not anything was wrong, so they have no `GUARD` label, no error step, and no guard event in the trace.

| Handling | Prevents | Does | Issue | Test |
|---|---|---|---|---|
| **Fence stripping** (`strip_json_fences`, in `evaluate_job`) | A `JSONDecodeError` when the grader wraps its JSON in ```` ``` ```` or ```` ```json ```` fences | Strips the fence before `json.loads` | [#2](https://github.com/justinyurasits/agents/issues/2) | [`test_fences.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/tests/test_fences.py): `StripJsonFencesTest`, `EvaluateJobTest` |
| **Find text by type** (`evaluate_job` and the `end_turn` return) | A crash when a thinking block comes before the text block | Picks the first block with `type == "text"`, never `content[0]` | [#4](https://github.com/justinyurasits/agents/issues/4) (exit check). The `evaluate_job` fix came earlier, before issues were used (commit `3fbd8e6`). | [`test_fences.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/tests/test_fences.py): `test_each_reply_shape_with_thinking_block_first`. The fake replies in the other test files also put a thinking block first, so every test that checks `run_agent`'s final answer covers the exit check too. |
| **Every tool request answered** (loop over `tool_use` blocks) | The API rejecting the next call when Claude asks for several tools in one reply and one goes unanswered | Runs each one and returns all results in **one** user message with matching `tool_use_id`s. The API rejects the next call if any request goes unanswered. | [#7](https://github.com/justinyurasits/agents/issues/7), D20 | [`test_multiple_tools.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/tests/test_multiple_tools.py): `MultipleToolUseTest` |

The tests for fence stripping (#5) and for #7, #8, #11, #15, #18, #30, #31, #32 and #21 were each also run against the code from before the guard or handling existed, to confirm they fail without it. The PRs that added them show that run.

---

## 6. Rules in code vs prompt

The repo's rule (CLAUDE.md) is that **deterministic rules belong in code, not prompts.** A prompt can be ignored or misread; code can't. Judgment calls belong to Claude.

| Rule | Lives in | Should live in | Notes |
|---|---|---|---|
| $180K base floor | Code (`MIN_BASE`, `hard_screens`) | Code | Moved from the prompt in #26. |
| Must be remote | Code (`REQUIRE_REMOTE`, `hard_screens`) | Code | Moved from the prompt in #26. Claude #1 still reads remote status from the posting; code applies the rule. |
| Builds hands-on AI experience | Prompt (`RUBRIC`) | Prompt | Needs judgment. The grader answers yes or no. |
| Answer → rating (yes: STRONG, no: WORTH REVIEWING) | Code (`RATING_FOR_ANSWER`) | Code | #26. |
| Rate vs flag (is enough info present?) | Tool descriptions, decided by Claude #1 | Prompt | Judgment about an unstructured posting. |
| Grader reply format (JSON) | Prompt (`RUBRIC`), parsed and checked in code | Both | The prompt asks for JSON; code strips fences, parses it, and checks the rating and reasons (`grade_problem`, #32). |
| The yes/no answer values | Prompt (`RUBRIC`) **and** code (`RATING_FOR_ANSWER`) | Both | The prompt tells the grader what to answer; the code rejects anything else. |
| Max passes, max tokens | Code (`MAX_PASSES`, `MAX_TOKENS`) | Code | |
| Which tool names exist | Code (`tools` + the dispatch) | Code | |

The floor and remote rules were moved into code by [#26](https://github.com/justinyurasits/agents/issues/26) (D28), which closes D6.

**Researched pay (#65, D34).** When a posting lists no pay, Claude can call `research_company` and pass the stored typical base on to `evaluate_job`. Code, not Claude, decides whether the pay `evaluate_job` received is researched. `run_agent` remembers the pay each `research_company` call found in this run, by company. `evaluate_job` treats its pay as researched when research found pay for the same company and Claude passed that pay (same lowest base) or no readable pay at all; then the hard rules use the researched pay as usual, and the reasons end with `"base estimated from stored company data"`, on IGNORE and on a rating alike. Pay Claude read from the posting is never labelled, and research on one company never labels another's pay.

**Rules are not guards.** A guard (section 5) catches a failure: a crash, a hang, or bad data. A rule applies one of Justin's decisions, and a posting that fails one is the agent working as intended. So the hard screens are a normal step, `hard_screen` (STEPS.md 7a), not an E-step; agent.py labels them `RULE (hard_screen)`, not `GUARD`; and the trace records them as rule events, never as caught guards (section 7).

| Rule | Fails when | Then | Can't be checked when | Test |
|---|---|---|---|---|
| **Remote** (`REQUIRE_REMOTE`) | Claude #1 sent `remote: false` | `evaluate_job` returns `{"rating": "IGNORE", "reasons": ["not remote"]}` with no grader call | `remote` wasn't sent, or isn't true/false: skipped | [`test_hard_screens.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/tests/test_hard_screens.py) |
| **Base floor** (`MIN_BASE`) | the lowest base in the range is under $180,000 | same, with `"base below $180K floor"`; both reasons when both fail | the pay isn't a readable yearly salary ("competitive", "$90/hr"): skipped | [`test_hard_screens.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/tests/test_hard_screens.py) |

---

## 7. Trace format

Every recorded run writes a **trace**: one JSON event per step, which the page (D15) replays. Built for [#1](https://github.com/justinyurasits/agents/issues/1) in three parts: step markers ([#27](https://github.com/justinyurasits/agents/issues/27)), the recorder and core events ([#28](https://github.com/justinyurasits/agents/issues/28)), and inner calls plus guard events ([#29](https://github.com/justinyurasits/agents/issues/29)). Format decisions: D24 (events), D25 (guards).

### How a trace is made

[`tracing.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/tracing.py) has a `Recorder`. `run_agent(job_text, recorder=None, fault=None)` calls it at each step. With no recorder it uses `NullRecorder`, which records nothing, so the agent behaves exactly the same. `python agent.py` records the sample run as scenario `clean` and writes **`traces/<scenario>-<YYYYMMDD-HHMMSS>.json`**. `traces/` is gitignored. Runs used on the page are made by `record.py` and saved to `recordings/`, which is committed (see [Recording scenarios](#recording-scenarios-recordpy)).

### The file

| Key | What |
|---|---|
| `trace_version` | `1` |
| `scenario`, `started_at` | Scenario name; UTC start time |
| `git_commit`, `git_dirty` | The commit that ran, and whether `job-evaluator/` had uncommitted changes. Lets the page link code references to the exact version. `git_dirty` doesn't count the files `record.py` writes itself, `recordings/` and `docs/SCENARIOS.md`: they don't change the code that ran (#99). |
| `fault` | The injected fault's name, or `null` |
| `model`, `limits` | `claude-sonnet-5-5`; `{"max_passes": 10, "max_tokens": 2000}` |
| `tools` | The full tool definitions, stored once |
| `events` | One per step, in order (below) |
| `result` | `{"ended_by": "end_turn" \| "max_tokens" \| "pass_cap" \| "api_error" \| "no_text" \| "unexpected_stop", "text": …}`: what `run_agent` returned |

### Events

**Every event has every key**, `null` when it doesn't apply: `id` (`e1`, `e2`, …), `seq`, `pass` (`0` = before the loop), `step_id` (from [STEPS.md](https://github.com/justinyurasits/agents/blob/main/job-evaluator/docs/STEPS.md)), `actor` (`python`, `claude`, or `tool`), `crossing` (`{from, to, kind}` or `null`), `payload`, `messages_before`, `messages_after`, `code` (`{file, marker, line, lines}` from `code_refs.py`; `null` for `claude_decides`), `parent` (the `tool_call` event an event happened inside, else `null`), `tokens`, `guard`, `injected` (`true` only for what an injected fault did or caused; see below).

| Step | `crossing.kind` | `payload` |
|---|---|---|
| `agent_starts` | — | `job_text` |
| `conversation_setup`, `save_turn`, `results_back` | — | `null`; `messages_before` / `messages_after` hold the conversation before and after (each adds exactly one message) |
| `send_to_claude` | `api_request` (python → claude) | `model`, `max_tokens`, `system`, `tools` (names only), `messages` (as sent) |
| `claude_decides` | `api_response` (claude → python) | `stop_reason`, `content` (every block: thinking, text, tool_use); `tokens` = `{input, output}` |
| `run_tools` | `tool_call` (python → tool) | `tool`, `tool_use_id`, `arguments`. Only for a tool that exists. |
| `inner_grader` | `inner_api_request` (tool → claude) | Same shape as `api_request`, with `system` = `RUBRIC` and `tools` = `[]`. `parent` = the `evaluate_job` tool_call. |
| `inner_grader` | `inner_api_response` (claude → tool) | Same shape as `api_response`, with `tokens`. `parent` = the `evaluate_job` tool_call. |
| `research_company` | — (`actor` = `tool`) | `company`, `role_level`, `found`, `typical_base_for_level`, `source`: the lookup in the stored data. `parent` = the `research_company` tool_call. A company that isn't on file is `found: false`, never a caught guard. |
| `run_tools` | `tool_result` (tool → python) | `tool`, `tool_use_id`, `is_error`, `content`. For an unknown tool, `actor` is `python` and `crossing` is `null`: no tool ran, Python itself answers. |
| `answer_returned` / `reply_cut_off` / `pass_cap` / `api_call_failed` / `no_final_answer` / `unexpected_stop` | — | `ended_by`, `text`: the last event, in the step that matches how the run ended |

Content blocks are stored exactly as the API returned them (`model_dump()`), except that thinking blocks drop their opaque `signature`. Data is converted when the event is recorded, so later changes to `messages` can't alter it.

### Guard events

Every check the loop or a tool makes records a **guard event**, whether or not it caught anything: `actor` = `python`, `crossing` = `null`, and

```json
"guard": {"name": "…", "checked": "…", "value": …, "caught": false, "action": null, "message": null}
```

**`caught` is `true` only when something went wrong.** A caught guard always uses its error-case step from STEPS.md (E1–E9) and says what happened next (`action`) and the message. An uncaught guard uses the step where the check runs.

| Guard | When it's recorded | Step (not caught → caught) | `value` | When caught: `action`, `message` |
|---|---|---|---|---|
| `pass_count` | Start of every pass; and once after the last pass if the cap is hit | `send_to_claude` → `pass_cap` | pass number (11 when caught) | `run_stopped`, the cap message |
| `stop_reason` | Every reply | `check_reply`, or `claude_done` on `end_turn` (never caught; `action: "finish"` on `end_turn`) | the stop reason | — |
| `max_tokens` (main loop) | Every reply that isn't `end_turn` | `check_reply` → `reply_cut_off` | the stop reason | `run_stopped`, the cut-off message |
| `stop_reason_known` | Every reply that isn't `end_turn` or `max_tokens` | `check_reply` → `unexpected_stop` | the stop reason | `run_stopped`, the unhandled-stop message |
| `tool_exists` | Every tool request | `run_tools` → `unknown_tool` | the tool name | `error_sent_to_claude`, the `ValueError` text |
| `max_tokens` (grader) | Every grader reply, with `parent` | `inner_grader` → `grader_cut_off` | the stop reason | `error_raised`, the cut-off text |
| `api_call_succeeded` | Every outer call to Claude | `send_to_claude` → `api_call_failed` | error type when caught | `run_stopped`, the API-error message |
| `tool_succeeded` | Every tool that ran | `run_tools` → `tool_failed` | exception type when caught | `error_sent_to_claude`, `"<Type>: <message>"` |
| `final_text_present` | Every `end_turn` reply | `answer_returned` → `no_final_answer` | `"text"`, or `null` when caught | `run_stopped`, the no-answer message |
| `grade_valid` | Every parsed grader reply, with `parent` | `inner_grader` → `invalid_grade` | the problem when caught | `error_raised`, the problem text |

**Rule events** (#26, D28). A hard rule isn't a guard, so it's never a caught guard: each rule records one normal event at step `hard_screen`, `actor` = `python`, `guard` = `null`, `parent` = the `evaluate_job` tool call, with the outcome in the payload:

```json
"payload": {"rule": "comp_floor", "checked": "lowest base >= MIN_BASE (180000)",
            "value": 140000, "outcome": "failed", "note": "base below $180K floor"}
```

`rule` is `remote` or `comp_floor`; `outcome` is `passed`, `failed` or `skipped`. A skipped rule's `value` is what it couldn't read (e.g. `"competitive"`), and its `note` says it was skipped. When a rule fails, no `inner_grader` events follow.

So a grader that's cut off shows two caught guards in order: `max_tokens` (`grader_cut_off`), then `tool_succeeded` (`tool_failed`) with the same text. An unknown tool shows only `tool_exists`, because no tool ran. A run that hits a guarded stop ends with the caught guard, then the final event.

`evaluate_job` records its grader call through `tracing.active()`, the recorder `run_agent` set for this run. Called outside a run, it records nothing.

**No secrets:** the recorder never sees the API client, request headers, or environment variables, and `write()` refuses to write a trace that contains `sk-ant` anywhere.

### Faults injected on purpose

[`faults.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/faults.py) makes the agent fail in one specific way, so the "break the agent" scenarios (6–9) can be recorded on demand (#46, D27). It's off unless asked for: `--fault <name>`, or a scenario whose `fault` field names one. With no fault the agent behaves exactly as normal.

| Fault | What it forces | Caught by |
|---|---|---|
| `tool_fails` | The grader's reply is replaced with broken JSON, **once** | `tool_succeeded` (E1); Claude can retry and succeed |
| `unknown_tool` | Claude's first tool request is renamed to `rate_posting`, **once**, before it's saved, so the conversation stays consistent | `tool_exists` (E2) |
| `runaway_loop` | The grader's reply is broken **every** time, and the pass cap is lowered to **2** | `pass_count` (E4): "Stopped after 2 passes without finishing." |
| `reply_cut_off` | The main call's token limit is lowered to **30** | `max_tokens` (E3), whose message gives the limit actually used |

**Why the cap is lowered for `runaway_loop`:** in every live run where a tool kept failing, real Claude retried once and then stopped on its own. With the cap at 10 it would explain the failure long before reaching the cap; at 2, the cap stops the run right after the retry.

**How it shows in the trace:**
- A **`fault_injected`** event where the fault acts, with `payload: {"fault": …, <what changed>: {"real": …, "injected": …}}` (or `{"normal": …, "injected": …}` for a limit).
- **Tool faults** (`tool_fails`, `unknown_tool`, the grader part of `runaway_loop`): the events the fault causes are `injected: true`. That's the caught guard, the error result, and the `results_back` that adds it to the conversation. Claude's later reactions are real, so they're `false`.
- **Limit faults:** every event made under the lowered limit is `injected: true`. For `reply_cut_off` that's the request, Claude's response, the checks and the end. For `runaway_loop` it's the pass-count checks and the end.
- **Real API responses are recorded as they came back,** never altered: a swapped grader reply shows its real text in `inner_api_response`, and the injected text only in `fault_injected`.

### Recording scenarios (record.py)

[`record.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/record.py) makes the runs the page plays (#53, D30): `python record.py <id>` or `python record.py --all`. Each is a **real run** of the scenario's posting(s) and fault exactly as written in `scenarios/scenarios.json`, saved to **`recordings/scenario-<id>.json`** (two digits, e.g. `scenario-05.json`), replacing the previous recording. A scenario id that doesn't exist prints the valid ids and exits (code 2) before anything runs.

The file is the trace (format above) plus two keys:

```json
"mismatch": false,
"check": {"expected": {"tools": ["evaluate_job"], "outcome": "STRONG"},
          "actual":   {"tools": ["evaluate_job"], "outcome": ["STRONG"]},
          "mismatch": false, "differences": []}
```

**What's compared** is the scenario's `expect`, never Claude's wording:

- **Tools:** every tool Claude asked for, in order, including an unknown one, with back-to-back repeats counted once, so a retry doesn't change the path.
- **Outcome:** `stopped` if a guard stopped the run; otherwise one entry per tool that succeeded with a verdict (`evaluate_job`'s rating, or `flagged` for `flag_for_review`), or `no rating` if there was none.
- `expect` can be a list of acceptable results; matching any one is a PASS (scenario 6: a rating after Claude's retry, or no rating after it explains the failure).

It prints PASS, or MISMATCH with each difference (e.g. `tools: expected evaluate_job; got flag_for_review`), and exits 1 if any run mismatched. A mismatched run is still saved, with every step and error, so it's visible rather than lost. Every run also regenerates `docs/SCENARIOS.md` from the JSON, including a "Checked by record.py" line per scenario; a test fails if the committed doc and the JSON ever disagree.

### Terminal output

The terminal lines are still there for following a run live, one line per event. Each starts with the **step id** and **where that step's code is**, in brackets: `[send_to_claude agent.py:<line>] pass 1: sending 1 message(s)` (#44, #120). The id is the same as STEPS.md, the `# STEP:` markers and the trace. In `agent.py` every line goes through `say(step_id, text)`, tagged `# (terminal only)`: it shows what's happening and changes nothing.

- **The line number** is the first line of the step's code, just below its `# STEP:` marker: the same line the page's Code tab and `code_refs.code_ref` use. `code_refs.terminal_labels` looks every label up from agent.py's source when the agent starts, so no number is ever typed in, and adding a line anywhere moves them all. `claude_done` shares `check_reply`'s code; `claude_decides`, which has no code, points at `send_to_claude`'s call, whose reply its lines describe (D46).
- **`file:line`** is the form VS Code's terminal turns into a link; Cmd/Ctrl-click it to open agent.py at that line. It's relative, so it resolves when you run from `job-evaluator/`.
- **Every non-blank line** carries a label, including each line of a multi-line text (Claude's reply, the final answer). Blank lines stay blank to space out the passes. `main`'s own lines (`Fault: …`, `FINAL ANSWER:`, `Trace written to …`) are labelled `agent_starts`.

The table leaves out the `agent.py:<line>` part of each label.

| Line | When |
|---|---|
| `[conversation_setup] messages has 1 item` | Start |
| `[send_to_claude] pass N: sending N message(s)` | Each outer call |
| `[claude_decides] stop_reason = …`, then one indented `text:` or `tool_use: id=… name=…` line per text or tool_use block | Each reply (thinking blocks aren't printed) |
| `[claude_done] end_turn → done. Outer calls: N …` | Normal finish |
| `[save_turn] appended assistant turn …` | Before dispatch |
| `[run_tools] dispatching <tool>(**{…})` | Each tool |
| `  [hard_screen] <rule>: <note>` (indented) | Each hard rule, inside `evaluate_job`; first, `pay '<pay>': base estimated from stored company data` when the pay is researched |
| `  [research_company] '<company>', '<role level>': found` / `not on file` (indented) | Each lookup, inside `research_company` |
| `[tool_failed] <tool> raised → <Type>: <message>` | A tool failed (E1) |
| `  [inner_grader] …` (indented) | Inside `evaluate_job`'s grader call |
| `[results_back] appended N tool_result(s) (ids: …[ is_error]) …` | After the tools run |
| `[reply_cut_off] …` / `[pass_cap] …` / `[api_call_failed] …` / `[unexpected_stop] …` | Guarded stops (E3, E4, E6, E9). E7 (no final answer) prints no line of its own. |
| `[agent_starts] Fault: …`, `[agent_starts] FINAL ANSWER:` and each line of the answer, `[agent_starts] Trace written to …` | `python agent.py` itself, before and after the run |

---

## 8. The page (site/)

Page v0 ([#57](https://github.com/justinyurasits/agents/issues/57)) replays a recorded run in the Execution Explorer layout (D15). Since [#71](https://github.com/justinyurasits/agents/issues/71) a visitor can pick any of the nine scenarios. It's plain HTML, CSS and JavaScript in [`site/`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/site): no framework, no build step, no API calls, no key. The design reference is [`design/explorer-d1-mockup.html`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/design/explorer-d1-mockup.html).

**Page structure** ([#78](https://github.com/justinyurasits/agents/issues/78), D36). One page, eight sections, in this order:
1. Hero, with **Watch it run**.
2. What's an agent.
3. How this agent works.
4. Scenarios: nine cards (#79, D39).
5. The run view: everything below in this section.
6. Design principles: seven principles, each guard under one (#80).
7. How it was built: the workflow, numbers counted from the repo, and links (#81, D41).
8. Footer: name, one line, the repo (#81). A contact link comes later.

A header bar links to each section. It's sticky on wide screens, and scrolls away on phones, where it wraps to three lines. The text in sections 1–3 is written for the page and labelled so.

- **The tool list** in How this agent works is read from scenario 1's recording: the tools Python offered Claude in its first request. Each tool gets a line from `TOOL_LINES` in `app.js`. Tests fail if `TOOL_LINES`, any recording's tool list, or a tool name in the page's text differs from `agent.py`'s `tools`.
- **Scenario cards** (#79, D39): one per scenario, in D21's two groups. Each card has the name, the `setup` line, a "Simulated failure" tag for scenarios 6–9, and the tool path, worked out from the recording: each pass's tool results in order, `+` within a pass, `→` between passes, and `→ error` after a tool that failed. A card's own words (the setup line and the tag) never state the rating; the path may end in `flag_for_review`, and a break-the-agent scenario's name states its failure (D39). Clicking a card works like a "Watch it" button. The card for the scenario now shown is marked, on load and on Back / Forward too, and no card is marked for an unknown id. The drop-down stays. The page fetches each recording once; the cards and the run share it.
- **The numbers in How it was built** come from `site/numbers.json`, which `build_numbers.py` counts from the repo (D41). `build_steps.py` runs it too. The counts are test cases in `tests/`; scenarios by group; decisions by Status line; E-steps, and how many a recording shows caught; and `Merge pull request #` commits before this PR (on main, HEAD's own merge isn't counted; on a branch it is, #108). The page fills each `data-number` slot from the file, and no digit is typed into the section. Tests fail if the committed file differs from a fresh count, or if the page shows a different number.
- **Link previews** (#105, D43): a meta description and Open Graph tags (`og:title`, `og:description`, `og:type`, `og:url`, `og:image`, its size and alt text) plus `twitter:card` = `summary_large_image`. They control what LinkedIn and other sites show when the link is shared. The image, `site/preview.png` (1200×630), is made by `make_preview.py`: scenario 6's run view at the step where the tool's error goes back to Python. Crawlers need absolute URLs, so `og:url` and `og:image` name the published GitHub Pages address. Tests check the tags, that the description and `og:description` match, and that the image is a committed 1200×630 PNG.
- **Links out:** the page may link to this repo on GitHub (`<a href>` only), to a file that exists in the repo; tests check both. The `og:url` and `og:image` meta tags may name the page's own Pages address (#105). It still requests nothing but its own files (D31). The repo is private for now (D2), so these links work for visitors once it's public.
- **A "Watch it" button** loads its scenario at step 1, paused, adds a history entry like the chooser does, and scrolls to the run view.
- **Back over a nav link** leaves the run where it was. Only a change of `?scenario=` reloads it.
- **The arrow keys and Space** drive the run only while the run view is on screen, so Space scrolls the page everywhere else.

**Run it:** from `job-evaluator/`, `python -m http.server 8000`, then open `localhost:8000/site/`. It has to be served (browsers won't `fetch` from a `file://` page), and it's served from `job-evaluator/` so the page can read `../recordings/` and `../scenarios/` without copies.

**What it loads, and nothing else** (a test checks the source has no URLs):

| File | Used for |
|---|---|
| `recordings/scenario-0N.json` | The chosen scenario's events: the map, the four questions, the timeline, the inspector. Fetched when the scenario is picked |
| `site/steps.json` | Each step's title and explanation, each guard check's and rule's wording, generated from [STEPS.md](https://github.com/justinyurasits/agents/blob/main/job-evaluator/docs/STEPS.md), and each guard's and rule's code, from agent.py's markers, by [`build_steps.py`](https://github.com/justinyurasits/agents/blob/main/job-evaluator/build_steps.py) |
| `scenarios/scenarios.json` | The chooser (each scenario's id, name and group), the intro (`setup`, `watch_for`) and the summary card (`summary`) |
| `site/fonts/` | Inter and JetBrains Mono (SIL Open Font License; the licenses are next to the files) |

**steps.json has one source.** `python build_steps.py` reads STEPS.md and writes `steps` (per step id: `{number, title, text, error}`, the text being the paragraph(s) between `Step id:` and `Code:`) `checks` (one row per guard check and the step it runs at, from STEPS.md's Checks table: `{check, runs_at, caught_as, text, passed, on_catch}`, `caught_as` being the E-step or `null`), `rules` (per rule: `{name, code_at, text, fails}`, from the Rules table) (#115, D44), and `code` (per caught-as step, or a routing check's first runs-at step, and per rule's `code_at`: `{file, marker, line, lines}` from `code_refs.code_ref`, #118, D45). Edit STEPS.md or agent.py, rerun the script; a test fails if the two disagree, or if any step or guard in the code or a recording has no explanation, or any check in tracing.py or a recording, or any recorded rule, has no row, or any check or rule has no `# STEP:` marker.

**Choosing a scenario** (#71, D35). A drop-down in the header lists all nine by name, in two groups (D21): the five normal runs, then the four break-the-agent runs. Picking one fetches its recording, rebuilds the steps, timeline and guard badges, and starts paused at step 1, with no page reload. The URL carries the choice: `?scenario=3` opens scenario 3, and no `scenario` opens scenario 1. Each pick adds a browser history entry, so Back and Forward step through the scenarios you picked. An id that isn't in `scenarios.json` (`?scenario=42`), or a scenario whose recording is missing, shows a one-line message in place of the run; the chooser stays usable.

| Scenario | Page steps |
|---|---|
| 1. Clean run | 14 |
| 2. Missing info | 19 |
| 3. Multi-tool | 21 |
| 4. Two tools at once | 23 |
| 5. Hard screen in code | 13 |
| 6. A tool fails | 23 |
| 7. Unknown tool | 21 |
| 8. Runaway loop stopped | 23 |
| 9. Reply cut off | 7 |

**Intro and summary card** (#75, D37). Under the title, an intro panel shows the scenario's `setup` (what's different about this input) and `watch_for` (the moment worth noticing). An intro never states the outcome. Break-the-agent intros add a "Simulated:" sentence saying what is injected and how. On the last step only, a summary card ("What happened") shows `summary`: what the recording shows happened, the outcome, and why it matters. Both are labelled "Written for this page · not Claude's output", like the step explanations. Tests check that every scenario has all three; that no intro uses an outcome word (a rating, flag, stop, retry); that scenarios with a `fault` say "Simulated:"; and that each summary names its recording's tools and outcome, as `record.actual()` reads them, and no other outcome.

**Events become page steps.** A run has more events than a visitor should step through (47 in scenario 6), so the page groups them (23 steps for scenario 6):

- A guard check that **passes** isn't a step. It's attached to the step after it (the pass count to the request, the reply checks to saving the turn), or, for a check inside a tool, to the tool's step before it (the grader's checks to the grader call). While that step is shown, the guard's badge flashes and its row's text from `checks` appears in the Python box.
- A guard check that **catches** something is a step of its own, with its E-step explanation.
- Step 9, **Claude says it's done** (`claude_done`), is always a step, though it's recorded as a passing `stop_reason` check: Python reading Claude's "I'm done" is routing, not a check, and it's why the loop ends.
- One hard screen's rule events are one step, and evaluate_job's own call to Claude (request, reply, and a simulated failure if there is one) is one step.
- Everything else is one step per event.

**How each part is driven by the recording:**

- **Execution map.** The box for the step's `actor` is highlighted. The four arrows show only what crosses at this step: the request (message count; on hover, what it carries), Claude's reply (stop reason, tool ID and name), the tool call (tool and first argument), and the tool's result (`result · ` and evaluate_job's rating, flag_for_review's status, or whether research_company found the company; or the error type in red). evaluate_job's own call is drawn only during that call, dashed purple, from Tools through Python to Claude (the call goes out through Python's client), labelled as a separate conversation; its reply tag turns red, labelled "Simulated failure", when a fault replaced the grader's reply. The header counts API calls so far, main and inner.
- **Guard badges** in the Python box: one per guard the run checks. The checks that passed at this step flash, with their one-line explanations; a caught guard stays lit red for the rest of its pass.
- **The four questions** are plain sentences, never code: Executing (the component), Has (what it holds, e.g. "1 message to send", "the stored facts for Marrowstone Logistics", "the 2 results, to add to the conversation in one message"), Because (what the step before did), Next (the next step's title, or where a tool's result goes).
- **Timeline:** every page step, grouped by pass (`START` = pass 0); steps inside a tool are indented; injected ones are tagged "simulated". Click any one to jump.
- **Explanation:** `steps[step_id]` from steps.json, labelled "Written for this page · not Claude's output". On a step that calls Claude, a line built from the request's payload follows it, labelled "from the recording": "This request carries: the system prompt, 2 tools (evaluate_job, flag_for_review), 1 message."
- **Inspector tabs**, each with a one-line description under the tab bar: State change (the messages list before and after; new messages highlighted), Code (the step's `code` and the commit it ran at), Payload (each event's payload and tokens, and a card for each guard check or rule at that step), Claude's response. A request to Claude records its tools by name; under it, Payload shows the full definitions Claude received (name, description, input_schema), taken from the recording's top-level `tools`, behind a "Show tool definitions (N)" toggle that's collapsed by default (#114). A focused toggle or button keeps Space for itself instead of playing the run. **Check cards** (#115, #118, D44, D45): one per guard check or rule at the step. The heading is the guard's E-number and title from STEPS.md ("E6 · The call to Claude fails · guard passed"; a check that only routes, `stop_reason`, says "routing check"), then one line: the row's "Passed means", or for a caught guard its message and "If it catches something". A rule's heading is its name and "rule passed" or "rule rejected the posting" (never failed), with the recording's note. A collapsed "Details" drop-down holds: what it protects against (the E-step's text), when it runs (the step and pass), where it lives (the code from steps.json's `code`, drawn like the Code tab), what happens if it catches something, the check and value, "Watch it fail (scenario N)" when Design principles links one, and the raw data. Event ids appear only there and in Payload's event headers, always labelled "event".
- **Claude's own words** (text and thinking blocks, the final answer, the grader's real reply) appear only under Claude's response. In Payload they're replaced with a pointer to that tab. Tool requests (names, IDs, arguments) are data and show in both.

**Playback:** starts paused at the first step, and again whenever a scenario is picked; Play / Pause, Back, Next, and 1× / 2× (2.5 s per step at 1×). Arrow keys step, space plays or pauses.

## 9. Known limits

What the code does **not** handle today. Each item is checked against the code, and linked where an issue exists.

- **Reading pay is a heuristic** (`lowest_base`, #26). It assumes US dollars and a yearly salary; it skips hourly, daily, weekly and monthly pay rather than compare it, and ignores numbers under 10,000 (bonus percentages, weeks of leave). A posting quoted in another currency would be compared as if it were dollars.
- **Remote status comes from Claude #1.** The remote screen trusts the `remote` boolean Claude fills in; if Claude leaves it out, the screen is skipped.
- **No retry with a bigger token limit** when a reply is cut off. Out of scope for #18.
- **The cap is fixed in code**, not configurable from outside, and it counts passes, not tokens or dollars. Out of scope for #15.
- **Return values are plain strings.** A caller can only tell "finished", "cut off", and "stopped at the cap" apart by comparing the text (see [Overview](#1-overview)).
- **Tools run one at a time**, in order (D20). Fine with three tools; slow if several grader calls ever happen in one turn.
- **Researched pay is matched by its lowest base** (D34). If a posting's own pay happened to equal the stored figure for that company, after Claude had researched it anyway, it would be labelled estimated. Role levels are matched by one stored word per level ("principal"); a level not on file gets no pay.
- **Stored company data covers only Marrowstone Logistics**, the company scenario 3 needs (#65). Every other company is `found: false`.

---

# Decision log
One entry per decision. Newest at the bottom. Format: decision, options considered, reasoning, what would change it.

---

## D1 — One repo for all agents, one folder per agent

**Date:** 2026-11-11
**Options:** separate repo per agent · one `agents` repo with a folder per agent
**Decision:** one repo, folder per agent.
**Reasoning:** I'll build many small agents; a new folder costs nothing, and the root README becomes an index that tells one story.
**What would change it:** an agent becomes a flagship piece that needs its own README, releases, and issues — then it moves to its own repo.

## D2 — Repo private until the first README is solid

**Date:** 2026-11-11
**Options:** public from day one · private, flip later
**Decision:** private for now.
**Reasoning:** the public version should read as finished work. Flipping is one click.
**What would change it:** job-evaluator README, spec, and one sample trace are done.

## D3 — One virtual environment per agent

**Date:** 2026-11-11
**Options:** one shared environment at the repo root · one per agent folder
**Decision:** one per agent (`job-evaluator/.venv`).
**Reasoning:** agents will need different packages; isolating them avoids version clashes.
**What would change it:** agents end up sharing nearly all dependencies.

## D4 — Track work on a GitHub Projects board, issue → branch → PR

**Date:** 2026-11-11
**Options:** TODO comments in code · issues only · issues on a board with automation
**Decision:** board with Backlog / Todo / In Progress / Done; issues auto-added; merged PRs move cards to Done.
**Reasoning:** makes the way I work visible, and every change gets acceptance criteria before it gets code.
**What would change it:** —

## D5 — `evaluate_job` uses its own Claude call (inherited, under review)

**Date:** 2026-11-11
**Options:** grade inside the outer Claude call (no tool) · separate focused Claude call inside the tool · deterministic scoring in Python
**Decision:** keep the separate call for now.
**Reasoning:** focused prompt, more reliable JSON, reusable outside the loop. But in a one-job run it adds a call without adding information.
**What would change it:** issue #6 (hard screens into code) may shrink what's left for the model to judge to one criterion.

## D6 — Hard rules currently live in the prompt (open)

**Date:** 2026-11-11
**Status:** closed by D28 (issue #26). ("#6" was a PR, not an issue; #26 is the issue.)
**Context:** the $180K floor and remote requirement are deterministic but sit in `RUBRIC`. A model can misapply a rule that code can't.

## D8 — Primary audience: people evaluating my work

**Date:** 2026-11-12
**Options:** job seekers as primary users · hiring managers/clients as primary viewers
**Decision:** built for people evaluating me; the working tool is the hook.
**Reasoning:** the point is showing how an agent works. The trace view stays central;
it stays a demo I don't have to maintain as a consumer product.
**What would change it:** real organic usage from job seekers.

## D9 — Candidate profile is a form, not a resume upload

**Date:** 2026-11-12
**Decision:** fields for target titles, comp floor, work mode, must-haves, deal-breakers,
top strengths; a sample profile preloaded.
**Reasoning:** no document parsing, no storing personal data.
**What would change it:** users consistently want resume-level matching.

## D10 — Live runs on a capped demo key; data stays in the session

**Date:** 2026-11-12
**Decision:** a separate API key with a hard monthly spend cap, a per-visitor run limit,
and an optional field for visitors to use their own key. Nothing a visitor enters
is saved or logged.
**Reasoning:** anyone can try it; worst-case cost is the cap.
**What would change it:** cap hit regularly → raise it or require own keys.

## D11a — Streamlit, hosted on Streamlit Community Cloud

**Date:** 2026-11-12
**Options:** Streamlit · Gradio on Hugging Face Spaces · custom web app
**Decision:** Streamlit.
**Reasoning:** pure Python on top of the existing agent; free hosting from the
GitHub repo; built-in status and expander components fit a step-by-step trace.
**What would change it:** a UI need Streamlit can't meet.

## D11 — FastAPI server + custom web page

**Date:** 2026-11-12
**Supersedes:** D11a (Streamlit), the same day. The two entries were both
numbered D11 until #93; the Streamlit one became D11a so D12's reference to
"D11 (FastAPI)" still holds.
**Options:** Streamlit · Gradio on Hugging Face Spaces · FastAPI + custom HTML/JS page
**Decision:** FastAPI + custom page.
**Reasoning:** the audience is people judging my work, so the step-by-step view has
to look deliberate. The agent stays in Python; FastAPI streams step events to a page
that renders each one live with an explanation, the real line of code, and the data.
**What would change it:** hosting cost or complexity outweighs the polish.

## D12 — Recorded scenarios only; static page on GitHub Pages

**Date:** 2026-11-12
**Supersedes:** D9 (profile form), D10 (capped live key), D11 (FastAPI)
**Decision:** v1 runs only prepared scenarios. Each is run for real locally,
its step events saved, and played back by a static page hosted on GitHub Pages.
**Reasoning:** the brief says no visitor input and must never fail in a live
demo. Recorded real runs give zero cost, no failure risk, and pacing control.
**What would change it:** a strong reason to let visitors run live — then
add a FastAPI live mode post-v1.

## D13 — Seven scenarios, error handling forced with labeled switches

**Date:** 2026-11-12
**Decision:** clean run, missing info, multi-tool, tool fails and recovers,
two tools in one reply, hard screen in code, runaway loop stopped. Failures
are triggered by a visible "simulated failure" switch, never hidden.
**Reasoning:** each M2/M3 fix becomes something a visitor can watch, and
links back to the issue that built it.
**What would change it:** the page feels like a test suite → cut to five.

## D14 — research_company uses stored company data

**Date:** 2026-11-12
**Decision:** company facts are pulled once and stored in the repo; the tool
reads from that file. Labeled on the page as stored data.
**Reasoning:** recorded runs must be repeatable; no live web dependency.
**What would change it:** a live mode post-v1 could use real search.

## D15 — Run view: Execution Explorer, linear map

**Date:** 2026-11-12
**Options:** A Instrument · B Lanes · C Ledger · D1 Explorer linear · D2 Explorer triangle
**Decision:** D1. Claude | Python | Tools across the top; data shown on every
arrow; a tool's own Claude call drawn as a separate path underneath; compact
four questions; timeline; inspector with State change / Code / Payload /
Claude's response.
**Reasoning:** keeps the architecture visible the whole run, and makes the
boundary crossings the thing you watch. Three boxes read cleaner than the
triangle or a fourth box.
**What would change it:** first-time viewers can't explain who decides and
who executes after one run.

## D16 — Build scenario 4 end to end before the other six

**Date:** 2026-11-12
**Decision:** one vertical slice first (record → trace → page) on the
tool-failure scenario, then add the rest.
**Reasoning:** proves the trace format and the page on the hardest case
before multiplying it by seven.

## D17 — Tests use the standard library's unittest, not pytest

**Status:** **Approved** (issue #5, PR #9)
**Date:** 2026-11-12
**Options:** `pytest` · `unittest` (standard library)
**Decision:** `unittest`. Run from `job-evaluator/` with
`python -m unittest discover -s tests -v`.
**Reasoning:** no new dependency, so nothing to add to requirements.txt and
no approval needed. For a handful of tests the two are about equal; `subTest`
covers the "same check, several inputs" case that pytest's parametrize would.
Tests swap `agent.client` for a fake and skip the `.env` load, so they make no
API calls and run without a key.
**What would change it:** enough tests that pytest's fixtures, parametrize,
or clearer failure output start saving real time. pytest also runs
unittest-style tests unchanged, so switching later costs little.

## D18 — Tool exceptions go back to Claude as is_error tool_results

**Status:** **Approved** (issue #8, PR #12)
**Date:** 2026-11-12
**Options:** let the exception crash the run · catch it and stop the run with
an error message · catch it and send it to Claude as an `is_error` tool_result
**Decision:** send it to Claude. `run_agent` wraps the tool call in
`try / except Exception`; on failure the tool_result content is
`"<ExceptionType>: <message>"` with `is_error: true`.
**Reasoning:** what to do after a failure (retry, switch tools, tell the user)
is a judgment call, so it belongs to Claude. Python's job is to report the
failure faithfully. `except Exception` catches every tool failure but still
lets Ctrl-C (`KeyboardInterrupt`) stop the script. The exception type is
included because it says what kind of failure it was (`JSONDecodeError` vs
`TypeError` for bad arguments) at almost no cost.
**What would change it:** a tool whose error messages could contain something
Claude shouldn't see (a key, a visitor's input), in which case send a generic
message and log the detail locally. Or retries running away, which a loop
cap (out of scope for #8) would handle.

## D19 — Unknown tool: raise inside the dispatch, list the real tools

**Status:** **Approved** (issue #11, PR #13)
**Date:** 2026-11-12
**Options:** add an `else` that raises · switch to a name → function dict ·
check the name before the `try`
**Decision:** an `else` branch that raises
`ValueError("Unknown tool '<name>'. Available tools: <names>.")`. It's inside
the `try` from #8 (D18), so it becomes an `is_error` tool_result with no new
error-handling code.
**Reasoning:** smallest change that fixes both cases in #11. `result` can
never be left unset or stale, because every branch either sets it or raises.
Listing the available tools tells Claude what it _can_ call, so it can recover
on the next turn. The names come from the `tools` list, so adding a tool
updates the message automatically.
**What would change it:** more tools, at which point a name → function dict
replaces the `if / elif` chain and the `else` becomes a dict lookup miss.

## D20 — Several tool_use blocks: run in order, inline, one result message

**Status:** **Approved** (issue #7, PR #14)
**Date:** 2026-11-12
**Options:** run tools in parallel · run them in order · move dispatch into a
`run_tool()` helper · keep it inline in `run_agent`
**Decision:** a `for` loop in `run_agent` over every `tool_use` block, run in
order. Each block gets its own `try / except` (D18), and all results go back
in one user message, each with its `tool_use_id`.
**Reasoning:** in order is simpler to read and to trace, and the issue says
it's enough. Parallel only pays off when tools are slow and independent.
Keeping it inline means the step page still points at one block of code in
the loop. Per-block error handling means one failing tool can't stop the
others from getting a result, which the API requires.
**What would change it:** slow tools (several inner Claude calls per turn)
making runs noticeably slow → run them in parallel. The dispatch growing
past a screenful → move it into a helper.

## D21 — Scenario set: 5 normal runs + 4 "break the agent" runs

**Date:** 2026-11-12
**Supersedes:** D13
**Decision:** normal runs (clean, missing info, multi-tool, two tools at once,
hard screen) and break-the-agent runs (tool fails, unknown tool, runaway loop,
reply cut off). Faults are injected and labeled. The page explains each
guard as it exists in the app and why it's there; no before/after comparison.
**Reasoning:** error handling is the most convincing part of the demo, and
each break scenario maps to a guard already built (#8, #11, loop cap, max_tokens).
**What would change it:** time pressure → cut normal runs 4 and 5 first.

## D22 — A cut-off reply is never acted on

**Status:** **Approved** (issue #18, PR #22)
**Date:** 2026-11-12
**Options:** dispatch any complete-looking tool requests in a cut-off reply ·
stop and act on nothing
**Decision:** stop. In the main loop, a `max_tokens` reply ends the run with
"Claude's reply was cut off (hit the max_tokens limit of 2000)." In
`evaluate_job`, a `max_tokens` grader reply raises a "cut off" error *before*
parsing, so it reaches Claude as an `is_error` tool_result (D18).
**Reasoning:** a reply that hit the limit is unfinished by definition, and
there's no reliable way to tell whether a tool request in it was finished.
Running a tool on half-written input is worse than stopping. Checking
`stop_reason` before parsing names the real cause; parsing first would report
"invalid JSON" and hide it.
**What would change it:** cut-offs happening in normal use. Then raise
`MAX_TOKENS` or retry with a bigger limit (out of scope for #18).

## D23 — Code references come from step markers, found with `ast`

**Status:** **Approved** (issue #27, PR #34)
**Date:** 2026-11-13
**Options:** hand-written line numbers in STEPS.md · a start and end marker
around each block · one marker above the code, with the code's extent found
by parsing
**Decision:** one `# STEP: <step_id>` comment directly above the code.
`code_refs.py` reads the source, finds the marker, and uses Python's `ast`
module to take the outermost statement (or `except` clause) starting on the
next line, so a multi-line call or a whole `if` / `for` block comes back
complete. Step 9 (`claude_done`) shares step 5's marker, and step 4
(`claude_decides`) has no code. A missing or duplicated marker, or a marker
not directly above code, raises an error.
**Reasoning:** hand-written line numbers in STEPS.md went stale on almost
every PR. One marker per step is the least to maintain, and `ast` knows where
a statement ends better than a hand-placed end marker would. Failing loudly
on a broken marker means a wrong reference shows up as a test failure, not
on the page.
**What would change it:** a step that needs to point at part of a statement,
or at code spread over several places. Then add an explicit end marker.

## D24 — Trace format: one flat event per step, every key always present

**Status:** **Approved** (issue #28, PRs #35 and #37)
**Date:** 2026-11-13
**Options:** nested events (a pass containing its steps) · flat list of events
· only the keys that apply on each event · every key on every event
**Decision:** a flat, ordered list of events. Each event has every key
(`id, seq, pass, step_id, actor, crossing, payload, messages_before,
messages_after, code, parent, tokens, guard, injected`), `null` where one
doesn't apply. Grouping (by pass, or under a tool call) comes from `pass` and
`parent`. Run-level facts (model, limits, full tool definitions, git commit)
are stored once at the top. SDK blocks are stored via `model_dump()`; thinking
keeps its text and drops `signature`. Data is serialized when the event is
recorded. `run_agent` takes an optional recorder; `NullRecorder` makes
recording a no-op.
**Reasoning:** a flat list is what the page replays step by step, and the
timeline can group it however it likes. Fixed keys mean the page never checks
whether a key exists. Storing `git_commit` lets code references link to the
exact version that ran. The full `messages[]` is repeated in each request and
before/after copy (decision F on #1): simple, and still small at 10 passes.
**What would change it:** traces getting slow to load on the page. Then store
each message once and refer to it by index.

## D25 — Guard events: every check recorded, "caught" means something went wrong

**Status:** **Approved** (issue #29, PRs #36 and #37)
**Date:** 2026-11-13
**Options:** record only guards that catch something · record every check
**Decision:** every check records a guard event,
`{name, checked, value, caught, action, message}`. `caught` is `true` only
when something went wrong; then the event uses the guard's own error-case
step (STEPS.md E1–E5). The stop_reason check is never "caught": it records
`action: "finish"` on `end_turn`. An unknown tool is caught by `tool_exists`
alone: no `tool_call` or `tool_succeeded` event, because no tool ran, and its
`tool_result` has `actor: python` and no crossing. The grader's own
max_tokens check got its own step (E5 `grader_cut_off`). `evaluate_job` finds
the run's recorder through `tracing.active()`.
**Reasoning:** the page should show that each check happened, not only when
it fired. That's the point of D21's "break the agent" runs. Reserving
`caught` for failures keeps "Claude finished" from reading like an error.
Recording an unknown tool without a tool crossing keeps the trace truthful:
nothing reached a tool. A module-level active recorder avoids adding a
recorder parameter to every tool function.
**What would change it:** tools that run in parallel (D20), where one global
"active recorder" and "current tool call" no longer work; then pass the
recorder and parent explicitly.

## D26 — A failed call to Claude stops the run with the error's type only

**Status:** **Approved** (issue #30, PR #38)
**Date:** 2026-11-13
**Options:** let the exception crash the run · retry · stop and return a
message (with the error's text, or with only its type and status)
**Decision:** catch `anthropic.APIError` around Claude #1's call. Stop the
run and return `"Couldn't get a reply from Claude: <ErrorType> (status
<code>). The run stopped."` No retries beyond the SDK's own. The trace
records an `api_call_succeeded` guard on every call (caught on failure, step
E6 `api_call_failed`) and ends with `ended_by: "api_error"`.
**Reasoning:** with no reply there's nothing for Claude to decide, so unlike
a tool error (D18) it can't go back to Claude: stopping with a clear message
is the only safe move. The SDK already retries connection errors, 429s and
5xx twice by default (`max_retries=2`), so the agent adds none (out of scope
for #30). The message leaves out the error's text because it comes from
outside the program; the type and status say what happened without risking
an echoed key or header.
**What would change it:** failures that a retry after a longer wait would fix
in practice (e.g. repeated 529s during a demo). Then add a retry with backoff,
which is a separate decision.

## D27 — Fault injection: real responses kept, injected effects labelled, cap lowered for the runaway demo

**Status:** **Approved** (issue #46, PR #47)
**Date:** 2026-11-13
**Options:** fake the failures in a test client · inject them into real runs ·
for the runaway loop: keep the cap at 10, nudge Claude with "temporary,
retry" errors, override Claude's end_turn, or lower the cap
**Decision:** inject into real runs, from `faults.py`, only when asked
(`--fault`, or a scenario's `fault`). Record every change as a
`fault_injected` event showing the real and the injected value, keep real API
responses unaltered, and mark `injected: true` exactly on what the fault does
or causes (tool faults: until the error is back in the conversation; limit
faults: everything made under the lowered limit). `unknown_tool` renames the
request before it's saved, so the conversation stays consistent.
`runaway_loop` lowers the cap to 2 for that run. All four choices made in chat
on #46.
**Reasoning:** BRIEF's truthfulness rule: recorded runs are real and
simulated failures are labelled. Real Claude retries a failing tool once and
then stops on its own (#8, #18, #29 live runs), so a cap of 10 would never be
reached; overriding its end_turn would replace a real decision, and nudging
might still not reach 10. Lowering the cap keeps every Claude decision real
and the cap demo reliable.
**What would change it:** Claude starting to retry more than once, which
would make the lowered cap unnecessary or need to be higher.

## D28 — Hard screens in code; the grader answers one yes/no question

**Status:** **Approved** (issue #26, PR #51)
**Date:** 2026-11-13
**Options:** screen in `run_agent` before Claude is called · screen inside
`evaluate_job` after Claude #1 extracts the details · keep the rules in the
prompt
**Decision:** screen inside `evaluate_job`, before the rating call (as #26
asks). `remote: false` fails the remote screen; a lowest base below
`MIN_BASE` fails the comp screen. A screen that can't be checked (remote not
given; pay that isn't a readable yearly salary) is **skipped, never failed**,
so missing data never rejects a posting. Every failed screen is listed in
`reasons`. The grader answers only "does this role build hands-on AI
experience?" as `{"answer": "yes"|"no", "reasons": [...]}`, and code maps it
(yes → STRONG, no → WORTH REVIEWING); other keys aren't passed on. The grader
no longer gets the Location / Remote / Compensation lines, since the screens
already used them.
**Guards vs rules** (Justin's review of PR #51): a **guard** catches a
failure (a crash, a hang, bad data) and gets an E-step under "When something
goes wrong". A **rule** applies one of Justin's decisions; a posting that
fails one is the agent working as intended, so a rule is a **normal step**.
The hard screens are a rule: step `hard_screen` (STEPS.md 7a, "Code checks
your hard rules"), labelled `RULE (hard_screen)` in agent.py, not `GUARD`.
CLAUDE.md and `test_annotations.py` now enforce both labels.
**Trace:** each rule (`remote`, `comp_floor`) records one normal event at
step `hard_screen`, with the `evaluate_job` tool call as its parent and
`{rule, checked, value, outcome, note}` as its payload (`outcome`: passed,
failed or skipped). Never a guard event, so `caught: true` still means only
that something went wrong (D25). A skipped rule's `value` is the text it
couldn't read (e.g. `"competitive"`).
**Reasoning:** CLAUDE.md: deterministic rules belong in code. Reading pay in
code is a heuristic (SPEC, Known limits), so it errs toward skipping:
wrongly rejecting a good posting is worse than sending one more posting to the
grader.
**What would change it:** postings whose pay `lowest_base` misreads (other
currencies, unusual formats); then extract a number in Claude #1's tool input
instead of parsing text.

## D29 — A stop reason the agent doesn't handle stops the run

**Status:** **Approved** (issue #21, PR #52)
**Date:** 2026-11-13
**Options:** list each unhandled stop reason and stop on those · stop on
anything that isn't `tool_use` · handle some (e.g. resume after `pause_turn`)
**Decision:** after the `end_turn` and `max_tokens` checks, anything other
than `tool_use` stops the run with "Claude stopped for a reason this agent
doesn't handle (stop_reason '…'). The run stopped." Nothing in the reply is
acted on, even a tool request, and no further request is sent. Only the stop
reason goes in the message, not any text Claude wrote.
**Reasoning:** same as D22: the run must always finish, and it shouldn't act
on a reply it doesn't understand. Checking for "not `tool_use`" rather than a
list means a stop reason the API adds later is stopped too; the SDK already
lists one (`model_context_window_exceeded`) the issue didn't mention.
Resuming after `pause_turn` is out of scope (#21); this agent uses no server
tools, so it shouldn't occur.
**What would change it:** the agent starting to use server tools (then
`pause_turn` needs a resume), or wanting to show Claude's refusal text.

## D30 — How a recording is checked against its scenario

**Status:** **Approved** (issue #53, PR #54)
**Date:** 2026-11-13
**Options:** parse the prose `expected_tools` / `expected_outcome` · add a
machine-readable `expect` to each scenario · compare the exact tool sequence
or count retries once · for multiple postings, run them separately or together
**Decision:** each scenario in `scenarios.json` gets an `expect`
(`{"tools": [...], "outcome": ...}`), next to the prose, which stays for the
page. Outcome is one of STRONG, WORTH REVIEWING, IGNORE, `flagged`, `stopped`,
`no rating`, or a list when the run handles several postings. `expect` may be
a list of acceptable results (scenario 6). Back-to-back calls to the same tool
count once. Several postings are sent together in one run, joined with a
`---` line, which also fixes `agent.py --scenario 4` (it passed the list as
text). SCENARIOS.md shows the `expect` as a "Checked by record.py" line. The
first three choices made in chat on #53.
**Reasoning:** parsing prose is fragile, since a wording edit would silently
change the check. Retries vary between real runs (scenarios 6 and 8), so an
exact count would mismatch on Claude's choice rather than on a wrong path.
Scenario 6 promises "retries or explains", so both are a PASS.
**What would change it:** the page needing a finer check (e.g. the number of
retries), or postings that must be evaluated in separate runs.

## D31 — Page v0: how the page is served, and what it shows where

**Status:** **Approved** (issue #57, PR #60 review)
**Date:** 2026-11-13
**Options:** put the page at the repo root or in `job-evaluator/site/` · copy
the recording into `site/` or read it where it is · load Inter and JetBrains
Mono from Google Fonts, ship the font files, or use them only when installed ·
show Claude's words wherever they occur, or only under "Claude's response"
**Decision:** the page lives in `job-evaluator/site/` and is served from
`job-evaluator/`, so it reads `../recordings/` and `../scenarios/` directly,
with no copies to keep in sync; it also loads `scenarios/scenarios.json` for the
scenario's name. The fonts ship with the page in `site/fonts/` (woff2, Latin,
the weights the design uses, with their OFL licenses). Claude's prose (text,
thinking, final answer, the grader's reply) appears only under "Claude's
response"; in Payload it's replaced with a pointer to that tab. Tool requests
(names, IDs, arguments) count as data and show in both. The map caption and the
three box descriptions from the mockup are kept as fixed text, labelled
"Written for this page"; step explanations come only from steps.json. The first
version listed every event in the timeline; the review replaced that with page
steps (D32).
**Reasoning:** the issue requires no requests except the page's own files,
which rules out Google Fonts; shipping the files keeps the design's fonts
without breaking that. Keeping Claude's words in one place makes it plain what
Claude wrote and what the page wrote. All approved in review on PR #60.
**What would change it:** GitHub Pages (M5) serving only `site/` (then the
recording is copied in at publish time).

## D32 — What counts as a step on the page

**Status:** **Approved** (issue #57, PR #60 review)
**Date:** 2026-11-13
**Options:** one step per event · hide passing guard checks · also group
events that belong together (the rules of one hard screen; evaluate_job's own
call) · also fold whole STEPS.md steps together (e.g. save the turn into
Claude's decision) to reach ~15
**Decision:** a passing guard check isn't a step: it's attached to the step
after it, or, inside a tool, to the tool's step before it, and while that step
is shown its badge flashes with a one-line explanation. The lines live in a new
"Checks" section of STEPS.md, built into steps.json with the step explanations.
A caught check stays a step. So does step 9, "Claude says it's done", though
it's recorded as a passing `stop_reason` check: it's routing, not a check. One
hard screen's rule events are one step, and evaluate_job's own call to Claude
(request, reply, any simulated failure) is one step. No further folding:
scenario 6 has 23 steps. The "This request carries" line is shown for
evaluate_job's own call too, not only the main loop's request. Justin chose
no fold, and step 9 as a step, in review.
**Reasoning:** saving the turn and adding results back are what make "the
conversation is the memory" visible, and the hard rules step is scenario 5's
principle, so none of them is folded away. Step 9 is one of Claude's two
decisions in the run and the reason the loop ends; the run can't finish without
showing it. Putting the check lines in STEPS.md keeps one source for every
explanation the page shows.
**What would change it:** other scenarios playing too long, or another guard
event that is really routing (it would join step 9 as an always-shown step).

## D33 — Page structure: one page, six sections, a "Watch it" button on every claim

**Status:** **Approved** (issue #62)
**Date:** 2026-11-13
**Decision:** one page with a header bar linking to six sections: Hero + run,
How it works, Design principles, Guardrails, How it was built, Footer.
Principles and guardrails each have a "Watch it" button that loads and plays
the matching scenario. Each run ends with a labeled summary card. I'm named
in the hero and footer.
**Reasoning:** learners want to watch; people evaluating my work want to see
how I think. One page serves the learner first and rewards the reader who
scrolls. "Watch it" turns every claim into something provable by pressing Play.
**What would change it:** the first-visitor test shows people never scroll
past the run view.

## D34 — Researched pay: code recognises it; no change to evaluate_job's inputs

**Status:** **Approved** (issue #65, PR #66)
**Date:** 2026-11-14
**Options:** add a field to evaluate_job's input schema so Claude says the
pay was researched · let code remember what research_company found in this
run and recognise it · key stored pay by exact role title, or by a seniority
word in the level Claude sends
**Decision:** code. `run_agent` keeps the pay each `research_company` call
found, by company (lowercase). `evaluate_job` gets it as a keyword argument
Claude can't set, and treats its pay as researched when research found pay for
the same company and Claude passed that pay (same lowest base) or none it
could read; in that case it uses the researched pay for the hard rules and adds
"base estimated from stored company data" to the reasons. Stored pay in
`data/companies.json` is keyed by a seniority word ("principal") matched in
the level Claude sends. `scenarios.json` names a scenario's company
(`stored_company`) instead of holding its facts, and SCENARIOS.md shows the
facts from `data/companies.json`.
**Reasoning:** the only thing Claude sees change is the new tool, with the
description from the issue; evaluate_job's schema stays as it was. Whether pay
is an estimate is a fact about where it came from, which code knows for
certain; asking Claude to declare it would put a rule in the model's hands
(CLAUDE.md). A seniority word matches the role levels Claude actually sends
("Principal Product Manager", "Principal PM").
**What would change it:** postings whose listed pay could equal the stored
figure (then the label could be wrong), or companies with several levels that
share a word (then key by full level).

## D35 — Scenario chooser: a drop-down in the header; each pick is a history entry

**Status:** **Approved** (issue #71, PR #72)
**Date:** 2026-11-14
**Options:** a native drop-down (`<select>`) · a row of nine buttons · a
side list · picking replaces the URL (Back leaves the page) or adds to the
browser history (Back returns to the previous pick)
**Decision:** a native `<select>` next to the playback controls, with two
labelled groups ("Normal runs", "Break the agent", D21). Each pick pushes
`?scenario=N` onto the history, so Back and Forward move between picks. No
`scenario` in the URL opens scenario 1 without changing the URL. An unknown id
or a missing recording hides the run and shows one line; the chooser stays.
**Reasoning:** a native drop-down is keyboard- and screen-reader-ready and
fits on a phone; nine buttons wouldn't fit the header. Visitors expect Back to
undo their last click, and "Watch it" buttons (D33) will use the same URL.
**What would change it:** the hero section (D33) needs the scenarios visible
at once, e.g. as cards; then the chooser becomes those cards, same URL.

## D36 — Page structure: eight sections, principles after the run

**Status:** **Approved** (issue #78, PR #86 review)
**Date:** 2026-11-14
**Supersedes:** D33's section list. D33's "Watch it" buttons, the summary
card at the end of a run (D37), and naming me in the hero and footer stay.
**Decision:** one page, a header bar linking to eight sections in this order:
1. **Hero:** what this is in one line, who built it, and a **Watch it run**
   button that jumps to the run view.
2. **What's an agent:** three sentences, a small loop diagram, and "Claude
   decides; Python executes".
3. **How this agent works:** the four parts (Python, Claude, the tools, the
   grader), the loop, and the tools with one line each on when they're
   used. Watch it buttons for scenarios 1, 3 and 4.
4. **Scenarios:** nine cards (#79).
5. **The run view:** the Execution Explorer (D15).
6. **Design principles:** principle → feature → Watch it (#80). This replaces
   D33's separate Guardrails section: guards are listed as features under
   the principle they serve.
7. **How it was built** (#81).
8. **Footer** (#81).

What D33 changes:
- D33's "How it works" becomes two sections, What's an agent and How this
  agent works.
- The run view is its own section, after the scenarios.
- Principles come after the run, because they point at scenarios.
- A "Watch it" button loads its scenario at step 1 and scrolls to the run.
  It starts paused, like every run (D33 said "loads and plays").

**Reasoning:** a first-time visitor needs "what's an agent" before the run
means anything. Someone evaluating the work wants the principles once they've
seen a run, and the cards give them a way into any scenario.
**What would change it:** the first-visitor test shows people skip the text
and go straight to the run. Then the run view moves up, under the hero.

## D37 — Scenario intro and summary card: where they sit, and what they may say

**Status:** **Approved** (issue #75, PR #77)
**Date:** 2026-11-14
**Options:** what's simulated as its own field · as a "Simulated:" sentence in
`setup` · the summary card inside the inspector · full width above it
**Decision:** the intro is a full-width panel under the title, always visible
while a run is shown. The summary card is full width between the four
questions and the timeline, visible only on the last step. What's simulated is
a "Simulated:" sentence at the end of `setup`, not a new field: the issue
asked for two intro lines. The rules are tests, not just guidance: no outcome
words in an intro, and each summary must name the recording's tools and
outcome.
**Reasoning:** the intro is what a first-time visitor reads before pressing
Play, so it sits above the map. The summary is the payoff, so it sits where
the eye lands after the last step, above the details. A test catches a summary
that goes stale when a scenario is re-recorded with a different path.
**What would change it:** the scenario cards (#79) show `setup` on each
card; then the intro panel may shrink to just "Watch for". Or a re-recording of scenario 6 that
explains the failure instead of retrying, which would need a new summary.

## D38 — Browser tests: Playwright in a dev requirements file, skipped when missing

**Status:** **Approved** (issue #84, PR #85 review)
**Date:** 2026-11-14
**Options:** add Playwright to `requirements.txt` · a separate
`requirements-dev.txt` · check every tab in the "Claude's words" test, or only
what the page shows by default
**Decision:**
- Playwright (pinned, 1.65.2) goes in a new `requirements-dev.txt`, which
  includes `requirements.txt`. Someone who only runs the agent doesn't need a
  browser.
- `tests/test_browser.py` is plain `unittest`. It starts its own local server
  and skips with a one-line reason when Playwright or Chromium is missing.
- The "Claude's words" check (D31) searches the State change, Code and
  Payload tabs at every step, along with everything else on the page. A tab
  that fails to draw, or a console error, fails the check, so it can't
  search the wrong tab by mistake.
- **One exemption, in Payload only:** the content of a tool_result. A tool's
  result is data, even when it carries the grader's reasons inside
  evaluate_job's rating. The test removes exactly the recorded
  tool_result content strings from Payload's text before searching. Nothing
  else on any tab is exempt.
- Claude often repeats its input: a line of the posting, or the
  job_description it passed to evaluate_job. A piece of Claude's words that
  also appears in the posting, in what Python sends Claude (system prompt,
  tool definitions, user messages other than tool results), or in Claude's
  tool request arguments (data, D31) isn't searched for. It would match the
  input, not a leak. Between 92% and 100% of each scenario's pieces are still
  searched.
- The tests read the page's state through `window.explorer`, which the page
  already exposes for checking by hand.
**Reasoning:** the page's rules (D31, every scenario plays) were checked by
hand on each PR and a gap slipped through (#76). A dev file keeps the agent's
install small; skipping keeps a fresh checkout's tests green while CLAUDE.md
makes a skipped suite not count for a `site/` PR.
**What would change it:** a CI runner with Chromium (then the suite always
runs). A new tab, which gets added to the searched tabs. Claude's words
reaching a tool_result through some new path (then the exemption needs
narrowing).

## D39 — Scenario cards: tool paths worked out from the recordings, by pass

**Status:** **Approved** (issue #79, PR #89 review)
**Date:** 2026-11-14
**Options:** the path from each scenario's expected tools, typed into
scenarios.json · from the recording, generated at build time · from the
recording, worked out in the browser
**Decision:**
- Each card's path is worked out in the browser from its recording: every
  tool result Python sent back, grouped by pass. Tools in one pass are joined
  with "+", passes with "→", and a failed tool is followed by "→ error". So
  scenario 4 reads `evaluate_job + research_company → flag_for_review` and
  scenario 6 reads `evaluate_job → error → evaluate_job`.
- A run that calls no tool (scenario 9) says "no tools called".
- The page fetches all nine recordings when it loads, once each, and the run
  view reuses them.
- A card's own words never state the rating. This loosens #79's "cards never
  state the outcome" (PR #89 review). Its own words are the setup line and
  the "Simulated failure" tag. The full path stays, including paths that end
  in `flag_for_review` (scenarios 2 and 4): it's the card's most useful line.
  The names of scenarios 8 and 9 ("Runaway loop stopped", "Reply cut off")
  stay too: for a break-the-agent scenario, the failure is the premise, not
  the ending.
**Reasoning:** the recording is what happened, so the path can't drift from
it. Expected tools can't show an error or two tools in one pass, and a build
step would add a generated file to keep in sync. A browser test compares each
path with one worked out separately in Python.
**What would change it:**
- The nine recordings get large enough to slow the first load. They're about
  820 KB together, uncompressed. Then the paths move to a generated file.
- First-visitor tests show the paths spoil the runs. Then the path could
  stop before the last tool.

## D40 — Which principle each guard serves

**Status:** **Approved** (issue #80, PR #90)
**Date:** 2026-11-14
**Decision:** every guard (E-step) is listed once, under the principle it
serves:
- **Errors go back to the model as information:** E1 `tool_failed`
  (scenario 6), E5 `grader_cut_off`, E8 `invalid_grade`. All three end as an
  `is_error` tool result Claude can act on.
- **Fail closed on the unknown:** E2 `unknown_tool` (scenario 7), E3
  `reply_cut_off` (scenario 9), E9 `unexpected_stop`, E6 `api_call_failed`,
  E7 `no_final_answer`. Each meets something the agent can't safely act on and
  ends the run, or refuses the request, with a clear message instead of
  guessing.
- **Bound the loop:** E4 `pass_cap` (scenario 8).

A guard a scenario shows gets a Watch it button. Tests check that its
scenario's recording really catches it. The other five are marked "Tested,
not demonstrated", with a test that's checked to exist.
**Reasoning:** "Errors go back" is about what Claude gets to see; "fail
closed" is about what the agent refuses to do. E3 sits under fail closed,
not bound the loop: a cut-off reply is never acted on (D22), whatever pass
it's on.
**What would change it:** a scenario added for a tested guard (it gets a
Watch it), or a guard whose effect changes, e.g. E6 retrying instead of
stopping.

## D41 — How it was built: numbers counted from the repo, links to GitHub

**Status:** **Approved** (issue #81, PR #92 review)
**Date:** 2026-11-14
**Decision:**
- Every number in How it was built comes from `build_numbers.py`, written to
  `site/numbers.json` and filled in by the page. The counts:
  - **Tests:** test cases unittest finds.
  - **Scenarios:** by group.
  - **Guards:** E-steps, and how many a recording shows caught.
  - **Decisions:** entries in this file, and how many say Approved or
    Proposed. 16 early entries have no Status line, and one says "closed by
    D28", so the page shows logged, approved and proposed.
  - **Merged pull requests:** `Merge pull request #` commits before this
    PR. On main, HEAD isn't counted when it's a merge: it's this PR's own
    merge, so the count a PR commits still matches once it's merged. On a
    feature branch HEAD is counted, since a branch with no commits yet starts
    at the previous PR's merge (#108).
- Every PR reruns the script (CLAUDE.md). A test fails if the file and a
  fresh count differ.
- The page may link to this repo on GitHub, in `<a href>` only, and only to
  files that exist in it. Links aren't requests: D31's "loads nothing but its
  own files" still holds, and a test enforces both.
- The footer has no contact link yet (your call in #81).

**Reasoning:** numbers typed by hand go stale silently. Counting from the
repo, and testing the count, keeps the page honest as it grows.
**What would change it:**
- Squash merges, which leave no "Merge pull request" commit. Then count with
  the GitHub API at build time.
- The repo staying private at launch. Then the links come out, or copies of
  the docs ship with the page.

## D42 — Precedence lives in the description of the tool that should wait

**Status:** **Approved** (issue #91, PR #98 review)
**Date:** 2026-11-14
**Options:** say nothing and let Claude choose (as before) · say "use this
first" in `research_company`'s description · say "try research first" in
`flag_for_review`'s description · enforce the order in code
**Decision:** `flag_for_review`'s description ends with "If compensation is
missing, try research_company first; flag only if research finds no pay."
`research_company`'s description is unchanged.
**Reasoning:** the order is a judgment about which tool fits, so it belongs
in what Claude reads, not in code. It goes in the tool that should wait,
because that's the description Claude reads when it's about to choose too
early. The instruction ("flag only if research finds no pay") also says when
waiting ends. Before this, Claude already researched first in scenarios 2 and
4, but that was the model's preference, not a decision (#65). After it, all
nine scenarios still PASS with the same tools and outcomes.
**What would change it:** a third tool that also claims "no pay listed" (then
precedence may need stating in more than one description), or a run where
Claude flags without researching (then the order may need enforcing in
code).

## D43 — Link previews: a generated screenshot, absolute URLs in two meta tags

**Status:** **Proposed** (issue #105)
**Date:** 2026-11-15
**Decision:**
- The page has a meta description and Open Graph tags, plus `twitter:card` =
  `summary_large_image`, so a shared link shows a card with a title, a
  description and an image.
- The image, `site/preview.png` (1200×630), is made by `make_preview.py`,
  not by hand. It's scenario 6 (a tool fails) in the run view, at the step
  where the tool's error goes back to Python: the red arrow, "evaluate_job
  failed", and the four questions. The script finds that step by what happens
  there, so it survives a re-recording, and only the run view is shown.
- `og:url` and `og:image` are absolute URLs on the GitHub Pages address,
  because crawlers need them. Like the GitHub links (D41), this is a narrow
  exception to "no URLs in the source": the test allows exactly these two
  meta tags on that address. The page still requests only its own files.

**Reasoning:** the failure moment is the most telling single frame. It shows
the three parts, the boundary crossing, and an error being handled, which is
what the page is about. A script means the image can be remade in one command
whenever the page's look changes.
**What would change it:**
- The Pages address changes. Update `PAGES_URL` in the tests and the two tags.
- A clearer moment for the card, e.g. scenario 4's two tools at once. That's
  a change to `SCENARIO` and `FIND_STEP` in the script.


## D44 — Check cards: worded from two tables in STEPS.md, keyed by check and step

**Status:** **Proposed** (issue #115)
**Date:** 2026-11-16
**Decision:**
- The Payload tab shows each guard check and each rule as a short card
  instead of raw JSON. The raw data stays behind a "Show data" toggle,
  collapsed by default.
- The wording lives in STEPS.md, not in the page. The old one-line "Checks"
  list became a table with one row per check **and the step it runs at**,
  naming the E-step it becomes when it catches something. A row is keyed by
  both because the same check can run in two places with two outcomes:
  `max_tokens` on the main reply is E3, on the grader's reply E5. A new
  "Rules" table words the two hard rules.
- Everything else on a card is already written somewhere: when it runs is
  that step's title, what failing does is the E-step's text, and the check
  and its value come from the recording.
- "Watch it fail" reuses the guard-to-scenario links in Design principles
  (D40), so there is one place that says which scenario shows which guard.
- A rule that rejects a posting reads "rule · rejected the posting", with an
  amber edge, never "failed" or "caught" in red: it's the agent working as
  intended (D28).

**Reasoning:** the issue asks that wording come from STEPS.md, and STEPS.md
already explains every step and E-step. Adding only the two facts it didn't
have (where each check runs and what it becomes when caught), as a table
the build script parses, means no sentence on a card is written twice. A test
reads tracing.py's guard calls and all nine recordings and fails if any check
has no row.
**What would change it:**
- A guard added in tracing.py. Its check needs a row, or the test fails.
- Cards proving too long when a step has several checks. Then the passing
  checks could collapse to one line each, with the rest behind the toggle.

## D45 — A check card shows its guard's code from steps.json, built from agent.py's markers

**Status:** **Proposed** (issue #118)
**Date:** 2026-11-16
**Decision:**
- Each check card's "Where it lives" shows the code under the `# STEP:`
  marker of the E-step the check becomes when caught (a rule's, `hard_screen`;
  a check that only routes, the step it runs at). `build_steps.py` looks it
  up with `code_refs.code_ref`, the same function recordings use, and writes
  it into `steps.json` as `code`.
- So `steps.json` now depends on agent.py as well as STEPS.md. Editing
  either means rerunning `python build_steps.py`; the "committed steps.json
  matches" test fails, saying so, until you do.
- Event ids (`e1`, `e2`, ...) appear only labelled "event": in Payload's
  event headers and the cards' raw data. The heading carries the real
  E-number from STEPS.md instead.

**Reasoning:** most guards never fire in a recording (E5–E9 are tested, not
demonstrated), so no recording holds their code; the page can't take it from
the run it's showing. Building it from the markers keeps one source for "where
is this guard" (`# STEP:` markers, never line numbers), and a test fails if a
check or rule has no marker. The cost: the code shown is agent.py as of the
last build, not as of the recording's commit, which the Code tab shows. The
card labels it with file, line and marker, not a commit.
**What would change it:**
- If the two ever confuse a visitor (a card's line numbers differing from
  the Code tab's for the same run), record each run's guard code with it
  instead, at the cost of a re-record.

## D46 — Terminal labels: the code's first line, from the markers; claude_decides points at the call

**Status:** **Proposed** (issue #120)
**Date:** 2026-11-16
**Decision:**
- Every terminal line starts `[<step_id> agent.py:<line>]`. `<line>` is the
  first line of the step's code, just below its `# STEP:` marker, the same
  line `code_refs.code_ref` gives the page. `code_refs.terminal_labels`
  looks them all up when the agent starts. agent.py prints only through
  `say(step_id, text)`, and a test fails if `.py:<digit>` appears anywhere
  in agent.py.
- `claude_decides` has no code (Claude decides on Anthropic's servers), so
  its lines (`stop_reason`, and each text or tool_use block) point at
  `send_to_claude`'s call: the reply they describe is what that call
  returned. `claude_done` uses `check_reply`'s line, as on the page.
- `main`'s lines (the fault notice, the final answer, the trace path) are
  labelled `agent_starts`, the step whose marker sits on `run_agent(...)`
  in `main`.
- Every non-blank line is labelled, each line of a multi-line text
  included. Blank lines between passes stay blank.

**Reasoning:** the issue asks for every line to lead to its code. Pointing
`claude_decides` at nothing would leave the one gap in the run, and a
`# STEP: claude_decides` marker would change what the page shows for that
step, which #120 rules out. The call is where the reply appears in the
code. Labelling each line of a multi-line answer keeps "every line" true
and keeps a pasted run readable line by line.
**What would change it:**
- If showing `send_to_claude`'s line on a `claude_decides` line confuses,
  label it `[claude_decides (no code) ...]` instead, or give
  `claude_decides` a marker of its own, together with the page.
