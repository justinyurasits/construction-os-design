# Design docs

Design docs for Justin's projects, one folder per project.

| Project | Folder | What it is |
| --- | --- | --- |
| Construction OS | [construction-os/](construction-os/) | A company-specific AI authoring system for residential builders. First slice: a priced potential change order. |
| Intake router (Pass 0) | [intake-router/](intake-router/) | An intent classifier and router with evals: it reads inbound messages at a general contractor and says which workflow each should start. |

## How this repo works

- **Each project gets its own folder**, with its own README listing its docs and a `sync-manifest.yaml`.
- **Where docs are written in Claude Docs, the Claude Doc is the working copy** and the folder is the reviewed, versioned record. Changes sync here by pull request; the files are never edited by hand. Each synced file starts with a link to its source.
- **Every change is a branch and a pull request.** Never commit to main.

To add a project: create a folder named for the project, add a README describing it and its docs, and add a row to the table above.
