# ESS AI Engineering Instructions

This is an ESS project governed by the ESS AI Framework for Vibe Coders. These instructions apply to every AI coding agent working in this repository.

## Before doing anything
1. Read every file in `.ess-ai/rules/`.
2. Read `.ess-ai/context/about.md`, `requirements.md`, `architecture.md`, `security.md`, `testing.md`, `reuse-catalog.md`, `progress.md`, plus any other context relevant to the request.
3. If material facts are missing, mark them `UNKNOWN`. Do not guess business rules, APIs, database fields, dependencies or architecture.

## How to work
- Follow the matching workflow in `.ess-ai/workflows/` (new feature, bug fix, refactor, migration, legacy modernization, release).
- Plan first. Do not modify files until the developer approves the plan.
- Implement one approved phase at a time. Smallest safe change; reuse existing patterns; no unrelated refactoring; no new dependencies without approval.
- Check `.ess-ai/context/reuse-catalog.md` before building a new RAG, MCP, agent, integration or migration.
- Run the project checks listed in `.ess-ai/context/testing.md` and report exact results. Never claim a test, scan or deployment ran without evidence.
- Never expose secrets, never commit `.env`, never request unrestricted production or database access, never bypass hooks or CI.
- After each phase, update `.ess-ai/context/progress.md`.
- Before a PR, produce an AI Change Report in `.ess-ai/reports/` from `AI_CHANGE_REPORT_TEMPLATE.md`.

## Guardrails (enforced, not optional)
- In Claude Code, `.claude/settings.json` runs `python tools/ess_guard.py` on every prompt, file edit and shell command. It blocks or flags risky prompts and denies edits to protected files, new dependencies, database drivers and SQL in application code, hard-coded secrets, direct database access, pushes to main, force-pushes and `git add -A`.
- If a guardrail denies an action, explain why to the developer and propose an approved alternative. Never try to work around it.
- Run `python tools/ess_guard.py check` before every commit (`/ess-check` in Claude Code). CI runs the same check on every pull request, whatever AI tool wrote the change.
- `.ess-ai/guardrails.json` holds the project's settings (protected paths, code and test folders, blocked imports). Only the tech lead changes it, in a reviewed PR, together with an ADR in `.ess-ai/context/architecture.md`.

## Commit and push
- Commits and pushes go through `python tools/ess_ship.py` only, after the developer approves the diff. It runs the guardrail check and the tests, creates `<type>/<ticket>-<summary>` from main, stages only the named files, commits with an ESS message and pushes the branch (never main, never force). In Claude Code, plain `git commit` / `git push` are denied and the ship command always asks for permission.
- AI tools without hooks (Copilot, Cursor, Amazon Q, Kiro, Gemini) must ask the developer to run the same command.

## Prompt library
Task-specific prompts live in `.ess-ai/prompts/` (index: `.ess-ai/prompts/INDEX.md`).

## Verification commands
```bash
ruff check .
ruff format --check .
mypy src
pytest --cov=ess_app --cov-report=term-missing
pip-audit
python tools/ess_guard.py check
```

The developer remains the gate: AI generates and assists; engineers understand, review, validate, secure, test and approve.
