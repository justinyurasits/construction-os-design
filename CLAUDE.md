# CLAUDE.md

Design docs for several projects, one folder per project.

## Rules

- Never commit or push directly to main. Every change goes on a branch and through a pull request.
- A synced file (one that starts with the "Synced from Claude Docs" header) is never edited by hand. Change the Claude Doc, export it, and replace the file in a sync PR. Keep the two-line header, and update that file's `rev` and `synced` in the folder's `sync-manifest.yaml`.
- One sync PR per project unless asked otherwise.
- A new project starts as a copy of `_template/project/` and gets a row in the root README table. A new component starts as a copy of `_template/component/`.
- Every project's design docs live here; no project keeps them in its code repository. A new code repository starts as a copy of `_template/repo/`.
- Roll-ups arrive from code-repository sessions as suggestions in the Claude Docs (synced files) or as pull requests (repo-authored files). A roll-up adds decisions to the component's `design.md` log and findings to `build-log.md`, and ends with a `Roll-up: <repo> #<first>–#<last>` line. Nothing goes in without Justin's approval. A roll-up also compares each synced file's manifest `rev` with its Claude Doc's current revision and offers a sync PR for any doc that has moved ahead.
- `_template/` is repo-authored and edited by hand. When STANDARD.md changes, update `_template/` in the same pull request as the sync.
- Within a project, product-level docs sit at the top of its folder and each component gets a subfolder with its own README and `sync-manifest.yaml`.
- Run `python tools/validate.py` before opening a pull request. It checks the structure against STANDARD.md and runs in CI on every pull request; an ERROR fails the check.
- Don't rewrite git history.
- No secrets, ever.
- The document model — component file set, naming, front matter — is in `STANDARD.md`, synced from a Claude Doc. Read it before creating or restructuring any document.
