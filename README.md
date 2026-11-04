# Design docs

Design docs for Justin's projects, one folder per project. A project with several components keeps its product-level docs at the top of its folder and gives each component a subfolder.

| Project | Folder | What it is |
| --- | --- | --- |
| Construction OS | [construction-os/](construction-os/) | A company-specific AI system for residential builders. Components: the [document workbench](construction-os/document-workbench/) (knowledge, retrieval and drafting) and the [intake router](construction-os/intake-router/) (classifies inbound messages and routes them to a workflow). |

## How this repo works

- **Each project gets its own folder**, with its own README listing its docs. Each folder of synced files has a `sync-manifest.yaml`.
- **Where docs are written in Claude Docs, the Claude Doc is the working copy** and the folder is the reviewed, versioned record. Changes sync here by pull request; the files are never edited by hand. Each synced file starts with a link to its source.
- **Every change is a branch and a pull request.** Never commit to main.

To add a project: create a folder named for the project, add a README describing it and its docs, and add a row to the table above. To add a component to a project: create a subfolder, add its README, and list it in the project README.
