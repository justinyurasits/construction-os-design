---
type: build-log
status: current
---

# job-evaluator — Build log

Dated working log. What I did, what broke, what I learned. Entries come from the Build notes in agents pull requests, through roll-ups.

---

## 2026-11-11 — Repo setup and first run

**Did**

- Walked through the agent loop step by step: tool definitions vs functions, dispatch, `stop_reason`, the messages list as memory, `tool_use_id` pairing, the inner Claude call in `evaluate_job`.
- Created the `agents` repo (private, Python .gitignore), added `job-evaluator/` with `agent.py`, `requirements.txt`, `.env.example`.
- Set up a virtual environment and `.env`; added `load_dotenv()` so the key loads from `.env`.
- Removed compensation from the test job: Claude chose flag_for_review instead of
    evaluate_job (2 API calls instead of 3). No code changed; the tool description
    drove the choice.
- First successful end-to-end run: 3 API calls, evaluate_job requested and dispatched,
  tool_result returned, end_turn.

**Broke**

- Ran `python3 -m venv .venv` and `pip install -r requirements.txt` from the repo root instead of `job-evaluator/`. Error: `Could not open requirements file`. Fix: deleted the root `.venv`, `cd job-evaluator`, recreated it there.
- Note: `(base)` in the prompt is Anaconda's base environment. `(.venv)` takes priority; `conda deactivate` if package errors show up.
- Put my real API key in .env.example (the committed file) and pushed it.
  Fix: revoked the key in the console, new key in .env only, restored the placeholder.
- Misspelled the folder (job_evaluator). Fix: renamed, rebuilt .venv (a venv breaks
  when its folder moves).
- Ran python agent.py from the repo root. Error: "No such file or directory".
- 401 invalid x-api-key. A revoked key was set in the terminal and overrode .env
  (load_dotenv doesn't replace an existing variable), and .env had leading spaces.
  Fix: unset ANTHROPIC_API_KEY, rewrote .env cleanly.
- AttributeError: 'ThinkingBlock' object has no attribute 'text'. Code assumed
  content[0] is text; the model returned a thinking block first.
  Fix: find blocks by type, not position, in evaluate_job and in the exit check.
  Raised max_tokens to 2000.
- NameError: name `______` is not defined. Pasted the fill-in-the-blank template
  literally.

**Learned**

- API key in .env needs to have no leading spaces.
- High level walkthrough of the script, including the tools, the agent loop, and the basic interactions between.

## 2026-11-12 — Product brief, workflow, and the agent hardened

**Did**

- Wrote the product brief: a learning and demo tool, visitors watch real
  recorded runs, no visitor input.
- Picked the run view after four design directions on a canvas: the
  Execution Explorer (D15).
- Set up the workflow: project board, milestones, CLAUDE.md, step list
  (STEPS.md), issues with acceptance criteria, Claude Code working each
  issue as a PR that I review and merge.
- Hardened the agent, one issue at a time: JSON fences (#2), tests (#5),
  tool errors back to Claude (#8), unknown tool (#11), every tool request
  answered (#7), loop cap (#15), cut-off replies (#18).
- Tracing: a plan first, then three PRs (#34–#36), so every run records
  every step, crossing and guard check.
- Wrote the nine scenarios (PR #39): five normal runs, four that break
  the agent on purpose.

**Broke**

- 401 again in a new terminal: VS Code was still carrying the revoked key
  from before .zshrc was cleaned. Fix: load_dotenv(override=True); quit
  and reopen VS Code.
- Debugger "Connection refused": stale session. Fix: full VS Code restart.
- The sample job had been missing its compensation line since a test the
  day before, so the "clean" run had quietly been taking the missing-info
  path. A PR review caught it.
- A save conflict in CHANGELOG.md: an open editor tab with old content
  would have overwritten six entries from merged PRs. Closed the tab
  without saving.

**Learned**

- A run can finish cleanly and still be the wrong run. The sample job lost
  its compensation line, and the "clean" run quietly became the
  missing-info run. Nothing failed, so only a review of what it actually
  did caught it.
- Hardening one issue at a time, each with a test that fails without the
  fix, means every guard has an issue, a PR and a test I can point to.

## 2026-11-13

**Did**

- Moved the hard rules into code (#26, PR #51): Claude extracts remote and
  pay; code applies the $180K floor and the remote rule before any rating
  call. Rules and guards are now different things on the page.
- Unknown stop reasons stop the run (#21, PR #52): fail closed.
- Fault injection (#46) and the recording script, then the first real
  recording: scenario 6, PASS (PR #58).
- Added LEARNINGS.md, and a docs audit that brought every doc in line
  with the code (#62, PR #63).

**Broke**

- Issue #31's fix landed on the wrong branch and reached `main` through an
  unrelated PR.
  - What happened: Claude Code was working on #31 in the main repo folder,
    with its changes not yet committed. In that same folder the branch was
    switched to `main`, then to a new `scenarios-data` branch. Git carries
    uncommitted changes across a branch switch, so the #31 work moved onto
    `scenarios-data`, and Claude Code committed it there without noticing the
    branch had changed.
  - How it reached `main`: the scenarios were committed on top and opened as
    PR #39, which merged with the #31 commit inside it. Claude Code had
    meanwhile rebuilt #31 cleanly in a separate worktree as PR #40, so the
    same change was now in two places.
  - How it was closed out: confirmed the commit that reached `main` was
    identical to #40's (same 9 files, same diff), closed #40 unmerged, and
    rewrote no history. A `git stash` in between reported "No local changes
    to save", because the work was already committed: nothing was lost. The
    D26 approval that only lived in #40 moved to the #32 PR.
  - Fix going forward: Claude Code always works in its own git worktree
    (`../agents-worktrees/<branch>`), never in the main repo folder. Added to
    CLAUDE.md in the #32 PR.

**Built: page v0 (#57, PR #60)**

- First time the whole idea works end to end: the recorded run of scenario 6
  plays in the browser, step by step, from `recordings/scenario-06.json`.
- First version stepped through all 47 events. Watching it, too many were
  passing checks ("Check: pass count"), and a dashed "next" arrow made the
  pass count check look like it sent the request.
- Review changes:
  - Passing checks flash their badge with a one-line explanation, written
    in STEPS.md.
  - Arrows show only what's crossing now.
  - evaluate_job's own Claude call is drawn Tools → Python → Claude, only
    while it happens.
  - Each tab has a one-line description.
  - Each request says what it carries.
  - The four cards are plain sentences.
- Kept 22 steps instead of folding to ~15, then made "Claude says it's done"
  a step too (23). It was hidden as a passing check, but it's routing: the
  reason the loop ends.
- Fonts ship with the page, since it may load nothing but its own files.

**Learned**

- A rule rejecting a posting and a guard catching a failure look alike in
  code, but they mean opposite things: one is the agent working, the other
  is something going wrong. Naming them differently made both the code and
  the page easier to read.
- A mockup is one frame. Making it real meant deciding everything between
  frames, and the one thing that could be misread was: the dashed "next"
  arrow looked like cause and effect.
- Docs drift quietly. By the audit, SPEC still described behavior from
  before two merged PRs. A test that checks a doc against the code is what
  keeps it true.

## 2026-11-14

**Did**

- Added `research_company` (#65, PR #66): stored company facts, and
  researched pay is used by the hard rules and labelled "base estimated
  from stored company data" (D34). Scenario 3 now chains two tools by
  Claude's own choice: research, then rate.
- Recorded all nine scenarios for real (#67, PR #68). Every one PASS.
- Added a CLAUDE.md rule (#69, PR #70): any PR that adds a tool or changes
  a description, schema, prompt or rubric re-runs every scenario, and
  expectations aren't edited just to make a run pass.
- The page plays any of the nine scenarios (#71, PR #72): a drop-down in
  two groups, `?scenario=N` in the URL, Back and Forward between picks, and
  a one-line message for an unknown id. Playing all nine found steps that
  scenario 6 never reaches, so the page had no words for them ("Has ·
  nothing new", "rating: undefined"). Fixed in the same PR.
- Each scenario now has an intro before the run (the setup, and what to
  watch for) and a summary card on the last step (#75, PR #77). The text is
  a draft for all nine. Tests keep outcome words out of the intros and check
  each summary against its recording's tools and outcome.
- Wrote issues for the rest of the page: an eight-section structure (#78,
  D36), scenario cards (#79), design principles (#80), and How it was built
  plus the footer (#81).
- Fixed #76 (PR #83): only runs a guard stopped show Python's message in
  "Has"; normal runs say "Claude's final answer".
- Browser tests (#84, PR #85, D38): Playwright for Python, skipped when
  Chromium isn't installed. They check that Claude's words stay in their tab
  across State, Code and Payload on every step of all nine scenarios, and
  that every scenario plays to the end. CLAUDE.md now requires them for any
  PR that touches `site/`.
- Built the page out to eight sections (#78–#82, PRs #86, #89, #90, #92,
  #95): hero, What's an agent, How this agent works, nine scenario cards
  that load each run, the run view, seven design principles with every
  guard placed under one, How it was built with numbers counted from the
  repo, and a footer. BRIEF now describes the page as built.
- Fixed two docs bugs found along the way: leftover rows of the old
  principles table in SPEC (#94, PR #96) and two decisions both numbered D11
  (#93, PR #97).
- Stated precedence (#91, PR #98, D42): `flag_for_review`'s description now
  says to try `research_company` first. Re-recorded all nine scenarios; all
  PASS with the same tools and outcomes. The agent now follows the
  principle the page names, instead of showing it by its absence.

**Broke**

- Nothing in the agent. Adding `research_company` changed the path of
  scenarios 2 and 4, which the PR never touched: both now research the
  company before flagging. Re-running every scenario is the only reason it
  showed up.
- A commit landed on local `main` instead of a branch: `<N>` in a command
  was read by zsh as "read from a file called N", so the branch was never
  created. Nothing reached GitHub; the commit was moved to its branch.
- PR #72 put Claude's whole final answer in the "Has" box on the last step
  of every normal run, which breaks D31. The scripted browser checks passed.
  A screenshot taken for #75 showed it. Filed as #76.
- PR #77 numbered its decision D36, which #78 had already planned for the
  page structure. Renumbered to D37 before merge.
- The leak check first searched only the default tab. Widening it to
  Payload failed every scenario at step 1, because Claude's thinking quotes
  the posting. The fix was to drop text Claude was given from the search
  list, not to exempt the tab.
- A tab that crashed left the previous tab on screen, and the leak check
  passed while searching the wrong one. It now fails unless the tab it
  clicked is the one showing.
- Claude Code nearly reset `site/` with `git checkout` to undo a deliberate
  breakage, before #78's work was committed. A safety check refused it.
- PR #90's rewrite of SPEC cut at the wrong `---` and left six old rows.
  Its test only read four-column rows, so it didn't see them.
- Re-recording scenario 9 for #91: same PASS, but Claude was cut off in the
  middle of a tool request instead of after a sentence.

**Learned**

- Tool descriptions are intent definitions. Two that overlap leave the
  order to the model. The new order was a good one, but nobody decided it.
- Testing an agent has two layers: unit tests prove the code, recorded
  scenarios prove the behavior. A single PASS shows a path happened, not
  that it always will.
- A page tested on one scenario is tested on that scenario only. Every new
  path through the loop is a new thing for the page to describe.
- An automated check only finds what it was written to look for. A rule
  like "Claude's words only under Claude's response" needs its own check.
  The screenshot only caught it by luck.
- A test only sees the shape it was built to read. The principles test
  checked four-column rows, so six-column leftovers were invisible to it.
- Same scenario, same PASS, different run: scenario 9 was cut off at a
  different point the second time. A PASS checks the outcome, not every
  step on the way.
- Writing a principle on the page exposed that the agent didn't follow it.
  Explaining the system is a way of testing it.

## 2026-11-15

**Did**

- Recordings no longer say "uncommitted code" just because `record.py` had
  written them (#99, PR #103). The dirty check now ignores `recordings/` and
  `docs/SCENARIOS.md`, the files a recording run writes itself.
- Re-recorded all nine scenarios from committed code (#104, PR #107). Eight
  of nine had been marked as made from uncommitted code. All PASS; the
  recordings in the PR are the ones I ran myself.
- Removed the committed `.DS_Store` files and ignored them everywhere (#106,
  PR #109).
- Link previews (#105, PR #110, D43 Proposed): a meta description, Open
  Graph tags, and a preview image made by `make_preview.py`: scenario 6 at
  the moment the tool's error goes back to Python.
- Fixed the merged-PR count on "How it was built" (#108, PR #111). On a new
  branch with no commits yet, it left out one merged PR.
- Rewrote the root README for launch (#102, PR #112): what the repo is, the
  live page, how to run it, and how it was built. Checked by following it
  word for word in a fresh clone. A new test fails if any file in the repo
  holds something shaped like an Anthropic key.
- Released 1.0.0 (PR #113), with `.nojekyll` so GitHub Pages serves the
  site as is.

**Broke**

- A command chained with `;` committed and pushed #106 before its tests had
  passed. The tests then failed on the merged-PR count, which is how #108
  was found. Commits now only happen if the tests pass.
- Claude Code gave me `git checkout -- job-evaluator/recordings` while I was
  already inside `job-evaluator/`, so the path didn't exist. `git restore
  recordings` worked.
- The new key test failed on day one: two test files hold made-up keys on
  purpose. Checked (printing only true/false) that neither is the real key,
  then exempted those two files by name.

**Learned**

- A check that marks its own output as a change will always cry wolf. The
  recordings looked untrustworthy because writing them made the tree dirty.
- A count that depends on where it runs (main, a branch, a branch with no
  commits) needs a test for each place.
- Following your own README in an empty folder is the only way to know it
  works for someone else.

## 2026-11-16

**Did**

- The Payload tab shows the full tool definitions Claude receives on every
  request: name, description and input schema, behind a collapsed toggle
  (#114, PR #116). Before, it showed only the names, though the
  descriptions are what Claude reads to choose a tool.
- Each guard check and rule in the Payload tab is now a short card instead
  of raw JSON (#115, PR #117, D44). The wording comes from STEPS.md, whose
  Checks list became a table keyed by check and the step it runs at, plus a
  new Rules table.
- The cards carry each guard's real E-number and title, and a Details
  drop-down with what it protects against, when it runs, its code from its
  `# STEP:` marker, and what happens if it catches something (#118, PR #119,
  D45). Event ids are labelled "event", so none reads as a guard
  number.
- Brought this log and LEARNINGS up to date (#121), and changed CLAUDE.md
  so every PR writes its own entries instead of suggesting them.
- Every terminal line now starts with its step id and the file:line of that
  step's code, e.g. `[send_to_claude agent.py:<line>]` (#120, D46). The
  numbers are looked up from the `# STEP:` markers each run, so a blank line
  added at the top moves them all by one and nothing breaks.

**Broke**

- The page's Space shortcut (play/pause) took the key from the new toggle,
  so Space played the run instead of closing it. Fixed in #114: a focused
  toggle keeps Space, as buttons already did.
- The first check cards showed as `[object HTMLDivElement]`: the tab
  flattens only one level of lists. A new browser test caught it.
- The old "every guard has a line" test read `tracing.py` with a pattern
  that missed a call split over two lines, so `no_final_answer` was only
  covered through the recordings. Fixed in #115's new test.
- `stop_reason` also runs at step 9, whose code is shared with step 5. The
  first #118 card looked for code under step 9 and would have shown "No code
  found". A browser test caught it.
- One deliberate breakage in #114 was itself broken: the edit left a syntax
  error, so the page didn't load and the test failed for the wrong reason.
  Redone with a clean breakage.
- These logs went two days without an entry. Claude Code suggested lines in
  chat after each PR, and none were written down.
- The first round of deliberate breakages for #120 tested nothing. The test
  names were in a shell variable, and zsh doesn't split one into words, so
  every breakage gave the same "no such test" error. The identical results
  gave it away; rerun with the names written out.

**Learned**

- What the page shows is what a visitor thinks the model saw. Shortening
  the tools to names hid the part that decides which tool Claude picks.
- The same check means different things in different places: `max_tokens`
  on Claude's reply is E3, on the grader's reply E5. The docs needed a row
  per place, not per check.
- A recording only shows the guards that fired. To explain every guard on
  every run, the page needs the code, not just the trace.
- A suggestion in chat isn't a record. If it matters, it goes in the PR.
- Reading the terminal output can teach the code, if each line says where
  it came from. The marker that anchors the page's Code tab can anchor the
  terminal too, from the same lookup.
