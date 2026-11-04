# CLAUDE.md

This repo holds the Construction OS design docs as synced copies of Claude Docs.

## Rules

- Never commit or push directly to main. Every change goes on a branch and through a pull request.
- Don't edit the design files (`*.md` other than README.md and CLAUDE.md) by hand. They are exports of Claude Docs. Changes are made in the Claude Doc and synced here.
- A sync PR replaces a file with a fresh export, keeps the two-line header at the top, and updates `rev` and `synced` for that file in `sync-manifest.yaml`.
- Don't rewrite git history.
- No company content beyond what the design docs already describe. No secrets, ever.
