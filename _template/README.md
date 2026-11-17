---
type: readme
status: current
---

# Templates

[STANDARD.md](../STANDARD.md) as files. Every file says what belongs in it; replace
each line in italics or `<angle brackets>`. Where these templates and the standard
differ, the standard wins and the template is fixed in the same pull request.

| Folder | Copy it to | What it is |
| --- | --- | --- |
| [project/](project/) | `<project-name>/` at the repo root | Product-level docs: README, brief, product spec, architecture, principles, manifest. README, brief and manifest are required; the rest are optional by type. |
| [component/](component/) | `<project-name>/<component-name>/` | The full component set: README, brief, spec, design, slice design, plan, build log, manifest, images. Every component has all of them. |
| [repo/](repo/) | the root of a new code repository | `CLAUDE.md` (sections 1–6 standard, section 7 the repo's own), `.github/pull_request_template.md`, `README.md`, `.gitignore`, `.env.example`. |

Links inside the templates are written for where the files end up once copied, so a
component's `../` reaches its project folder, and a project's `component/` links
point at its component folders.
