# CLAUDE.md

Design docs for several projects, one folder per project.

## Rules

- Never commit or push directly to main. Every change goes on a branch and through a pull request.
- A synced file (one that starts with the "Synced from Claude Docs" header) is never edited by hand. Change the Claude Doc, export it, and replace the file in a sync PR. Keep the two-line header, and update that file's `rev` and `synced` in the folder's `sync-manifest.yaml`.
- One sync PR per project unless asked otherwise.
- A new project gets its own folder, a README, and a row in the root README table.
- Don't rewrite git history.
- No secrets, ever.
