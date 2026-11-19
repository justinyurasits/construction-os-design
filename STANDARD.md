> **Synced from Claude Docs. Edit there, not here.**
> Source: [Design — Document Standard](https://claude.ai/artifact/XH2r6ocKxZXUpUdyndiDWN) · doc revision 58 · synced 2026-11-19

# Design — Document Standard

Nov 5, 2026 · @Justin

The document model for the `design` repository. The Claude Doc is the editable source; `STANDARD.md` in the repository is its reviewed snapshot, synced by pull request. Anything that needs the standard — a Claude Code session, a project doing design-document work — reads it from the Claude Doc or from that snapshot, never from a second copy.

Repo operation rules stay in `CLAUDE.md`: no direct commits to main, synced files are never hand-edited, no history rewrites, no secrets. Those are guardrails against damage and have to be read rather than followed to. This document holds the model, which is the part that grows.

## Component structure

Every component has the same files from the day it is created. A file with nothing settled in it yet exists at `status: draft` and says what is open. Nothing holds two jobs.

| File | Its one job |
| --- | --- |
| `README.md` | Index, plus the short public version: what this is, why it exists, the two or three decisions worth knowing, and what is designed vs. built vs. validated |
| `brief.md` | Who it's for, the painful moment, what it replaces, what's out of scope |
| `spec.md` | The domain, named and bounded. A pointer if the domain lives elsewhere. |
| `design.md` | Architecture, boundaries, and the decision log |
| `plan.md` | Work still ahead: milestones, each with an exit criterion. Finished work moves to the build log; bugs and small tasks are GitHub issues. |
| `build-log.md` | What happened, in order, and what each finding changed |
| `sync-manifest.yaml` | Source Claude Doc, rev, sync date, per synced file |
| `images/` | Static exports, re-exported when the drawing changes |

**Optional, by named type** — any number per component:

| File | Its one job |
| --- | --- |
| `<slice>-design.md` | Technical design for one vertical slice |
| `<name>-prompt.md` | A prompt the component sends to a model, with its version log. The code repository holds the copy that runs, and a test there checks the two match. |

As at the project level, a new optional type is added to this table when a real document needs one, so every document has a name and a stated job. A file that fits no row is a reason to add a row, not to keep an unnamed file.

## Rules

- **One decision, one source.** Decisions live in that component's `design.md` log. A plan or build log may reference a decision; neither records one.
- **One document, one job.** If a file matches two rows above, it is two files.
- **Front matter: `type` and `status`** (`draft | current | superseded`) on every `.md`. For a **synced** file those two values live in the manifest beside `source` and `rev`, and the file carries the two-line sync header instead of front matter — a block added by hand is wiped the next time that file syncs. For a **repo-authored** file, the READMEs included, the front matter is written in the file itself.
- Filenames are lowercase-kebab `.md`. No version numbers in filenames.
- **Claude Doc or repo-authored.** A doc is a Claude Doc when Justin writes it with Claude in chat. It is repo-authored when Claude Code writes it through pull requests, when it is still a placeholder, or when it is a README. A placeholder moves to a Claude Doc the first time real content is written in it.
- **Claude Doc titles** follow `<Project> — <Component> <doc type>`, with the doc type taken from the file name: "Construction OS — Corpus Design", "Construction OS — Intake Router Classifier Prompt". Project-level docs drop the component ("Construction OS — Brief"); docs for this repository itself use "Design" as the project ("Design — Document Standard"). The manifest's `title` matches the Claude Doc's title.
- Restructuring happens in the Claude Docs first. The repo follows via sync; synced files are never hand-edited.
- A new component is this file set, not a decision about which files to make.

## Project structure

A project is a folder under the repo root holding one product's documents, with its components as subfolders beneath it.

**Required at the project level:** `README.md`, `brief.md`, `sync-manifest.yaml`.

**Optional, by named type:**

| File | Its one job |
| --- | --- |
| `principles.md` | Craft knowledge — what building this taught, each principle anchored to the incident that taught it and to where it is enforced |
| `product-spec.md` | What the product must do for its users, independent of implementation: capabilities, each with a stable ID in its heading (`<PROJECT>-CAP-<nn>`) and acceptance criteria; user journeys, including incomplete input and failures; and product-wide requirements. Needed once a project's components make up one product. A project that groups independent builds, such as a set of demos, has no product spec or architecture: its brief says what's in the folder and why it's grouped, and each component's own brief and spec say what it must do. A capability moves to its own spec when it is big enough to manage on its own: several journeys, complicated rules, or its own acceptance-test suite. |
| `architecture.md` | How the components fit together and how a request moves through them |

The project level is deliberately not a fixed file set the way a component is, and the difference is structural rather than a matter of judgment. Components repeat: each does the same job, so fixing the set removes decisions that would otherwise get made differently each time. Projects do not repeat — as one with two components needs an architecture document and one with a single component does not. New optional types are added to the table above as they appear, so a document has a name and a stated job rather than arriving ad hoc.

A new project gets a folder, a README, a brief, and a row in the root README's index table.

## The reference project

`_template/` at the repo root is this standard as files, in three folders. `project/` holds every required and optional project-level file; `component/` holds the full component set; `repo/` holds the files every code repository starts with. A README at `_template/` says which to copy where. Each file says what belongs in it. To start a project, copy `project/` and rename it; to add a component, copy `component/` into the project; to start a code repository, copy `repo/` into it. Real projects keep their product-level docs at the top of their folder; the `project/` subfolder exists only in the template, to keep it apart from the components.

The template shows the standard; it adds nothing to it. Where the two differ, this document wins and the template is fixed in the same pull request. `_template/` is repo-authored: edited by hand, never synced.

## Repositories

Every repository a project here describes follows the same conventions, so a person or a Claude Code session can find its way around any of them.

- **Naming.** A product built across several repositories names them `<product>-<part>`: `construction-os-corpus`, `construction-os-workbench`. A product in one repository takes its plain name: `fieldscope`, `agents`.
- **Starting files.** Every code repository starts from `_template/repo/`: `CLAUDE.md`, a pull request template, `README.md`, `.gitignore`, and `.env.example` when it uses secrets.
- **CLAUDE.md.** The standard sections are copied from `_template/repo/CLAUDE.md` and marked with the template version they came from, so drift shows. One section is the repository's own: its layout, conventions and domain language. A repository may override a standard rule only by saying so in that section, with the reason.
- **README.** What it is, its status (`active`, `prototype` or `archived`), how to run it, and a link to its design folder here.
- **Sidebar.** A one-line description and topics on GitHub.
- **Links both ways.** A code repository links to its design folder; the design folder's README links to the code.

## How design and code work together

Every project works the same way.

- **Every design doc lives here.** No project keeps design docs in its code repository. The one exception is visual design: colors, type, marks and components live in the brand-system repository, with their own rules and change control. Files generated from code, such as a page built from recorded runs, stay with the code.
- **Design leads, code follows.** A change to what the product does, to a requirement or to the architecture is made in the design docs first, and the code pull request cites it. Code pull requests never edit design docs. Claude and Claude Code still make design changes: when the work needs one, they stop and propose it, and once Justin approves, they make it in the Claude Doc (synced files) or in a pull request here (repo-authored files). The code pull request follows and cites it.
- **The issue is the plan.** An approved GitHub issue authorizes the work; the spec and design constrain how it is done. If they conflict, or the work needs a change the design doesn't cover, stop and say so.
- **Pull requests capture the small stuff.** Decisions made while coding and what the work taught go in the pull request under the template's *Decisions (proposed)* and *Build notes* headings. Merging the pull request approves its decisions. That covers implementation choices made inside an approved issue only. A decision that changes a requirement, the architecture, a security boundary or documented behavior is a design change: it goes through the design docs first (Design leads, code follows), and a code pull request can't approve it.
- **Roll-up.** Claude Code asks "Roll up to design?" when a pull request it opened is merged, when an issue or milestone is done, and about every ten turns of work since it last asked. On yes, it gathers Decisions and Build notes from pull requests merged since the last roll-up and proposes them: decisions for the component's `design.md` log, findings for `build-log.md`, and lessons that generalize beyond the work (what the next component or project would want to know) for the project's `principles.md`, under the principle they serve or flagged as a candidate new one. For synced files they go in as suggestions in the Claude Doc; for repo-authored files, as a pull request here. Nothing enters the record until Justin approves it. The roll-up also checks for drift: for each synced file in the component and its project, it compares the revision in the manifest with the Claude Doc's current revision, and offers a sync pull request for any doc that has moved ahead. A session without Claude Docs access lists those docs from DOCS.md and asks Justin to check them. The build log notes each roll-up ("Roll-up: construction-os-workbench #16–#22"), which marks where the next one starts.
- **Tests can read design docs.** A code repository's tests may read its design docs to check the code against them. Those files are then sync-sensitive: their headings and formats are part of the contract, so renaming a heading or reshaping a table needs a matching code pull request. Take extra care with a synced file, because a sync can rename a heading.
- **Finding the design repo.** `../design` means next to the repository's main checkout. A session working in a git worktree finds it from the main checkout, or from a `DESIGN_DIR` override, not from the worktree's own folder.

## Maintaining this document

**Changes are made here.** `STANDARD.md` in the repo is a snapshot and is never edited, the same rule as every other synced file.

**Re-sync at the moment it matters, not on a schedule.** The standard is only load-bearing when a component is created or restructured, so the sync happens immediately before that work. If nothing has changed, the sync is a no-op. If something has, the repo was stale and now isn't. Nothing detects drift automatically — the manifest records the rev it was synced at, and comparing that to this doc's current rev is a manual check — so tying the sync to the moment of use is what keeps it honest.

**Every change gets a dated line in the history below.** One line, what changed and why. This is what makes a convention trustworthy to someone reading it six months later, including a Claude Code session that has never seen the conversation it came from.

**The structure is checked automatically.** `tools/validate.py` checks every project and component against this standard: required files, front matter, manifests and sync headers, the document index and links. It runs on every pull request, and an error fails the check. It can't see Claude Docs, so whether a doc has moved ahead of its synced snapshot is checked at sync and roll-up time.

**A component that doesn't fit is evidence about the standard, not an exception to it.** Either the shape is wrong and this document changes, or the component is wrong and it changes. No component is exempted. Exemptions are how a convention stops being one.

## The document index

`DOCS.md` at the repo root lists every synced document: its title, its Claude Doc URL, the file it syncs to, and the rev and date of that snapshot.

It is **generated from the sync manifests and never hand-written** — its first line says so. The manifests stay the source; this is a derived view that collects what is already there into one table.

It is regenerated in the same pull request as any manifest change, which is the only moment it can go wrong.

It does two jobs at once. It is the list of every synced working document, so no bookmarks are needed — open the repo, open the index, follow a link. And because it carries each snapshot's rev beside its source, it is the staleness check: a rev behind the live doc means that file in the repo is out of date, visible at a glance instead of by opening four manifests.

## Change history

| Date | Change |
| --- | --- |
| 2026-11-19 | The roll-up also proposes lessons that generalize for the project's principles, after the agents repo's rule that every pull request adds its learnings was lost when its docs moved here and nothing fed the principles anymore. |
| 2026-11-19 | A product spec is needed once a project's components make up one product, not once it has two components. A project that groups independent builds (agents, the demos) keeps only its brief, after the old rule would have required a product spec for two unrelated demos. |
| 2026-11-19 | Added which docs are Claude Docs (written with Claude in chat) and which are repo-authored (written by Claude Code, placeholders, READMEs), and a title pattern for Claude Docs, after DOCS.md showed fourteen titles in six styles and no rule for which docs were synced. |
| 2026-11-19 | DOCS.md described as the list of every synced working document, not every working document, to match the index's own scope. |
| 2026-11-19 | Opening reworded so it reads correctly from the repo copy: the Claude Doc is the editable source, STANDARD.md its reviewed snapshot. Pull requests capture the small stuff now bounds what merging a code pull request approves: implementation choices inside an approved issue, never a change to a requirement, the architecture, a security boundary or documented behavior, after a review found the line between the two left room for an agent to slip an architecture decision into a code pull request. |
| 2026-11-19 | Every design doc lives here, with visual design in brand-system as the one exception. Design leads, code follows now says Claude and Claude Code do make design changes, once approved, in the Claude Doc or a design pull request, never inside a code pull request, after the old wording read as a ban on using Claude for design docs at all. |
| 2026-11-19 | The roll-up also checks for drift between each Claude Doc and its synced snapshot, and offers a sync for any that moved ahead, after two build logs were found a revision behind with nothing to flag it. |
| 2026-11-19 | Components get a table of named optional types, like projects: `<slice>-design.md` moved there and `<name>-prompt.md` added, after the intake router's classifier prompt had no legal home. `plan.md`'s job now says it holds only work still ahead, a rule the template already had. |
| 2026-11-19 | Added `tools/validate.py`, run on every pull request, and corrected the front matter rule to match practice: synced files carry the sync header, not front matter, with type and status in the manifest. |
| 2026-11-19 | Added two rules to How design and code work together, after moving the agents docs: design docs that a repository's tests read are sync-sensitive, and `../design` resolves from the main checkout, because a git worktree has no sibling design folder. |
| 2026-11-17 | One model for every project: linked projects removed, every design doc lives here. Added How design and code work together (design leads, the issue is the plan, pull requests capture decisions and build notes, the roll-up) and `_template/repo/` with a standard CLAUDE.md, after the CLAUDE.md files across eight repositories were found to contradict each other on planning, merging and secrets. |
| 2026-11-17 | `_template/` split into `project/`, `component/` and `linked-project/`, with its own README, because project-level files at the template root sat beside the component folder and the project README doubled as the instructions. Real projects are unchanged. |
| 2026-11-17 | Added `product-spec.md` as a named optional project type, after a review found no single place that said what the product must do for its users: it was split across the brief's wedge, the architecture's walkthrough and a slice design's acceptance tests. Each of those should point to it once a project has one. |
| 2026-11-17 | Renamed for the `design` repository, which now indexes every project. Added the `_template/` reference project, linked projects for docs that change with their code, and repository conventions, after a cleanup found the same document concepts under different names across repositories. |
| 2026-11-05 | Project level given a required set (README, brief, manifest) and a table of named optional types, after `principles.md` was found to match no row in the standard. Components stay fixed because they repeat; projects vary structurally, so the project level is required-plus-named-optional rather than fixed. |
| 2026-11-05 | Added `DOCS.md`, a generated index of every synced document and its Claude Doc URL, so working documents are reachable from the repo rather than from bookmarks. |
| 2026-11-05 | Front matter rule corrected: for synced files `type` and `status` live in the manifest and the sync writes them, because a hand-added block is wiped on the next sync. |
| 2026-11-05 | Created. Fixed component file set replacing per-component judgment, after `build-log.md` and `build-guide.md` diverged between the two existing components. Decision logs consolidated to `design.md` after `document-workbench` was found keeping three. |
