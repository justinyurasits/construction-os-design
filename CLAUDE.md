# CLAUDE.md

Design docs for several projects, one folder per project.

## Rules

- Never commit or push directly to main. Every change goes on a branch and through a pull request.
- A synced file (one that starts with the "Synced from Claude Docs" header) is never edited by hand. Change the Claude Doc, export it, and replace the file in a sync PR. Keep the two-line header, and update that file's `rev` and `synced` in the folder's `sync-manifest.yaml`.
- One sync PR per project unless asked otherwise.
- A new project gets its own folder, a README, and a row in the root README table.
- Within a project, product-level docs sit at the top of its folder and each component gets a subfolder with its own README and `sync-manifest.yaml`.
- Don't rewrite git history.
- No secrets, ever.
- The document model — component file set, naming, front matter — is in `STANDARD.md`, synced from a Claude Doc. Read it before creating or restructuring any document.
