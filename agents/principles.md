---
type: principles
status: current
---

# Agents — Principles

What building these agents has taught me, kept as I go. Each entry says where it came from, so it can be checked against the code, issues and PRs.

Newest at the bottom of each section.

## How agents work

- **Claude decides; Python executes.** The model never runs anything. It returns a request (`tool_use`), and code decides whether and how to carry it out. "The agent" is the loop, the tools and the model together. _(job-evaluator, first walkthrough)_
- **The conversation is the memory.** Each API call is independent. Claude "remembers" only because the full messages list is sent every time. Drop an append and the agent forgets what it just did. _(job-evaluator, step 5 and 8)_
- **Tool descriptions steer the agent.** Removing compensation from a posting made Claude pick `flag_for_review` over `evaluate_job` with no code change. The description was the control logic. _(compensation test)_
- **Every request gets an answer with the same ID, even when the answer is an error.** Each `tool_use` needs a matching `tool_result` in the next message, or the next call is rejected. _(#7, #11)_
- **Find content by type, never by position.** The model can return a thinking block before its text. Code that assumed `content[0]` was text crashed. _(ThinkingBlock crash, #4)_
- **A guard turns a crash into information the model can act on.** Sending a tool error back as a `tool_result` marked `is_error` lets Claude retry, switch tools, or explain. Without it, the run just dies. _(#8, #11)_
- **In practice, Claude stops retrying on its own.** Live runs showed one retry, then an explanation. The loop cap is a backstop for when it doesn't, not the normal stop. _(#46 live runs)_
- **The model for judgment, code for rules.** Anything already decided (a salary floor, a remote requirement) belongs in code: same answer every time, testable, readable. The model gets only what needs interpretation. Same reason a bank never lets the model decide whether a caller is authenticated. _(#26, D28)_
- **Claude extracts, code decides.** Claude reads messy text and fills in clean fields; code applies the rule to those fields. Check what the model hands you: an unreadable value should be skipped and recorded, not trusted. _(#26)_
- **Smaller questions get more reliable answers.** The rating prompt went from three criteria including pay and location to one yes/no question about the work. _(#26)_
- **Guards, rules and routing are different things.** Guards catch failures. Rules apply decisions already made. Routing decides where the loop goes next. Treating them as one confuses both the code and anyone reading it. _(stop_reason discussion, #51 review)_
- **Fail closed on the unknown.** The loop handles the stop reasons it knows and stops on anything else, rather than listing known bad ones. A stop reason the API adds later is caught automatically. _(#21, D29)_
- **Guards catch failures; defensive handling prevents them.** Fence stripping, finding text by type and answering every tool request never "catch" anything: they handle every input correctly so nothing fails. Keeping them out of the guard list keeps "guard" meaning one thing. *(#63)*
- **Choosing a tool is intent classification.** Each tool description is a definition Claude matches the input against. Adding `research_company`, whose description overlapped `flag_for_review` on "no pay listed," moved scenarios 2 and 4 to a new path with no code change. Where two tools overlap, the model picks the order unless the descriptions state precedence. _(#65, PR #66)_
- **Adding a tool can change behavior you didn't touch.** A new description competes with every existing one. _(PR #66)_
- **A check means what it's checking for, where it runs.** The same `max_tokens` check is "Claude's reply was cut off" in the loop and "the grader's reply was cut off" inside a tool, with different outcomes. Describe checks per place they run, not per name. _(#115, D44)_

## Showing how an agent works

- **Show what happened; label everything else.** Recorded data comes only from real runs. Teaching explanations are labeled as written for the page. Never present an explanation as the model's reasoning. _(BRIEF, truthfulness rule)_
- **Record real runs and replay them.** A demo that depends on a live API call can fail in front of the person you most want to impress. _(D12)_
- **The interesting moments are the boundary crossings.** What goes from Python to Claude, what comes back, what goes to a tool. Keep the architecture on screen and animate what crosses it. _(D15)_
- **Error handling is the most convincing part of the demo.** Happy-path agent demos are everywhere; watching an agent recover from a failure is what shows it was built properly. _(D21)_
- **A mockup shows one moment; the real page has to decide every moment.** The mockup answered what the page looks like at the failure. It didn't answer what an arrow shows between crossings, or how long a caught guard stays lit. Each of those had to be decided once the page played a whole run. _(#57, PR #60)_
- **Show only what's happening now.** A dashed "next · request" arrow, drawn during the pass count check, made it look as if the check sent the request. The Next card already says what comes next; the map should show only what's crossing at this step. _(PR #60 review)_
- **Events aren't steps.** The trace records 47 events for scenario 6; a visitor steps through 23. Checks that pass flash their badge with one line instead of being steps, and the events of one action (the hard rules, the grader call) are grouped. Saving the turn and adding results back stay, because they're what make "the conversation is the memory" visible. _(PR #60, D32)_
- **Routing isn't a check, even when it's recorded like one.** "Claude says it's done" is logged as a passing `stop_reason` check, but it's one of Claude's two decisions in the run and the reason the loop ends. The page shows it as a step. _(PR #60 review)_
- **One source for every explanation.** Step text and the one-line check explanations live only in STEPS.md, and a script builds the page's copy. A test fails if they drift. _(#57, build_steps.py)_
- **Explaining the system tests it.** Writing "state precedence" on the page as a principle showed the agent didn't follow it yet. The fix (#91) came from writing the page, not from a failing test. _(PR #90, PR #98)_
- **A page built on one example only covers that example.** Page v0 was built and checked on scenario 6. Playing the other eight turned up four kinds of step it had no words for: "Has · nothing new", "rating: undefined". _(#71, PR #72)_
- **Set up the run without giving away the ending.** A first-time visitor needs to know what's different about this input and what to watch for, and the scenario's `behavior` line told them how it ends. So the page has an intro before the run (setup, watch for) and a summary card after it. _(#75, PR #77)_
- **A summary says what the recording shows, not why Claude did it.** "Claude asked for research_company first" is in the data. "Claude realised it needed pay" is a guess presented as fact. _(#75)_
- **Show what the model actually received.** The trace kept tool names per request; the page showed only those, while Claude got the full descriptions it chooses by. Showing less than was sent misleads. _(#114, PR #116)_
- **A run shows only the guards that fired.** Only four of the nine guards are ever caught in a recording. To explain all of them on any run, the page reads each guard's code from its marker, not from the trace. _(#118, D45)_

## Testing an agent

- **Test the code and the behavior separately.** Unit tests with a fake client prove the Python works, with no API calls and the same result every time. Recorded scenarios prove what Claude actually does on known inputs. Neither replaces the other. _(tests/, record.py)_
- **Break it on purpose.** Fault injection makes a tool fail, invents an unknown tool, forces a runaway loop, or cuts a reply off, so every guard is seen working in a real run instead of trusted. _(#48, faults.py)_
- **A description change is a code change.** Any PR that adds a tool or changes a description, prompt or rubric re-runs every scenario. That's the only reason the scenario 2 and 4 shift was caught. _(#69)_
- **Don't edit the expectation to make it pass.** A mismatch is information. Change the expected path only when you've decided the new path is right. _(#69)_
- **A check only finds what it looks for.** The browser scripts for #71 searched every step for "undefined" and "nothing new" and passed. A screenshot for #75 then showed Claude's whole final answer in the "Has" box, which breaks D31, because no script checked where Claude's words appear. Each rule needs its own check. _(#76)_
- **Tie written text to the recorded data.** The summary card's text is tested against what `record.actual()` reads from each recording (tools and outcome), and the intros are tested for outcome words. If a re-recording takes a different path, the stale summary fails the test instead of misleading visitors. _(#75, PR #77)_
- **One PASS isn't proof.** The model varies run to run. Reliability means pass rates over many runs, which is next. _(open)_
- **Testing on one example only tests what that example reaches.** The page was built and checked against scenario 6 alone. Playing the other eight found four kinds of step it had no words for, and one that leaked Claude's final answer. _(#72, #76)_
- **A test needs its own check that it looked where it meant to.** A tab that crashed left the previous tab on screen, and the leak check passed while searching the wrong one. Now it fails unless the tab it clicked is the one showing. _(PR #85)_
- **Check every view, not just the default.** The leak check first searched only the tab the inspector opens on; the raw payloads, where a leak is likeliest, were a click away and unchecked. _(PR #85)_
- **A test only sees the shape it was built to read.** The principles test read only four-column rows, so six leftover rows of the old table sat in SPEC unnoticed. _(#94)_
- **Same PASS, different run.** Re-recorded, scenario 9 still passed, but Claude was cut off at a different point. A PASS checks the outcome, not the path inside it. _(PR #98)_
- **A check that flags its own output is noise.** Recordings were marked "uncommitted code" because writing them dirtied the tree. Exclude what the tool itself writes, or every result looks suspect. _(#99)_
- **Test a count everywhere it runs.** The merged-PR count was right on main and wrong on a fresh branch. _(#108)_
- **Follow the README from an empty folder.** Only a fresh clone shows what a newcomer meets. _(#102, PR #112)_

## Building with an AI coding agent

- **The issue is the spec.** The coding agent builds exactly what the issue says, so acceptance criteria have to be input → expected result, something you can actually check. _(every issue)_
- **Ask for a plan before a big change.** For tracing (#1), a plan as an issue comment, then three small PRs, kept each review manageable. _(#1, PRs #34–#36)_
- **Verify from the output, not from the agent's report.** Run the tests yourself. Best practice: break the fix on purpose and confirm the tests fail. _(#5, #9 onward)_
- **Rules belong in a file the agent reads every time.** `CLAUDE.md` holds the workflow; every review that finds a gap becomes a new rule. _(CLAUDE.md)_
- **Two workers can't share one checkout.** The coding agent's uncommitted work rode along when I switched branches and landed in the wrong PR. Fix: the agent always works in its own git worktree. _(PR #39)_
- **A pushed key is a leaked key.** Revoke it; deleting it from the file doesn't remove it from history. And a stale key in the shell can silently override `.env`. _(day one)_
- **Define the product before writing issues.** Issues written ahead of the brief kept raising "what is this for?" Once the brief existed, every issue could be checked against it. _(BRIEF)_
- **Commit before you break things on purpose.** Claude Code nearly reset `site/` with `git checkout` to undo a deliberate breakage, before the real work was committed. A safety check refused the command. Commit first, then break, then reset. _(PR #86)_
- **Only commit when the tests pass.** A command chain with `;` committed and pushed before the tests finished, and they failed. Use `&&`, or check the result first. _(#106, PR #109)_
- **Give commands for the folder the person is in.** A path that's right from the repo root fails from inside `job-evaluator/`. _(#104)_
- **Read why a breakage failed, not just that it did.** Four breakages for #120 all "failed", with the same error: the test command never ran. A breakage proves something only if it fails in the test you meant, with the message you expected. _(#120)_
- **A suggestion in chat isn't a record.** Build-log lines suggested after each PR were never written, and the log went two days stale. Now every PR writes its own entries. _(#121)_
