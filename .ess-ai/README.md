# ESS AI Project Control Plane

This folder is the project's AI context, rules, prompts, workflows, checklists, templates and evidence layer. It implements the ESS AI Framework for Vibe Coders inside the repository.

AI tools load it through the adapter files at the repository root (`AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.cursor/rules/`, `.amazonq/rules/`, `.kiro/steering/`, `GEMINI.md`). If your tool is not covered, start each session with `prompts/ESS_BOOTSTRAP_PROMPT.md`.

| Folder | Purpose |
|---|---|
| `context/` | Project truth: about, requirements, architecture, DB, API, security, testing, approved tools, reuse catalogue, progress. Fill before implementation. |
| `rules/` | Non-negotiable engineering rules the AI must follow (00 to 18; 18 is the guardrails rule). |
| `guardrails.json` | Settings for the enforced guardrails: protected paths, dependency files, code and test folders, blocked imports, SQL rule. Tech lead only. |
| `automation.json` | Claude Code automation: the auto-test command run after every AI edit, the remote, PR opening and an optional after-ship command (for example a ticket update). Tech lead only. |
| `workflows/` | Step order for new features, bug fixes, refactors, migrations, legacy modernization, releases. |
| `prompts/` | The ESS prompt library (see `prompts/INDEX.md`). |
| `checklists/` | Gates for development, testing, security, code review, PR and production readiness. |
| `templates/` | Test report, release notes, rollback plan, deployment evidence, knowledge-hub document. |
| `knowledge/` | How to publish a reusable AI implementation to the ESS AI Knowledge Hub. |
| `reports/` | Evidence: AI Change Reports, test reports, deployment evidence for this project. |

Do not delete this folder. Do not treat it as optional documentation.
