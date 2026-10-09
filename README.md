# ESS Python AI Starter Kit

ESS baseline for AI-assisted Python API/service development: FastAPI, typed settings, safe error handling, Ruff, mypy (strict), pytest with coverage, pre-commit (ruff, gitleaks, mypy), and CI with secret scan, lint, format, typecheck, tests, dependency audit and build.

## Developer flow
Copy → Setup → Open in approved AI IDE → Fill `.ess-ai/context/` → Bootstrap prompt → Discover → Plan → Approve → Implement small phases → Test → Security → AI Change Report → PR.

FastAPI is the starter example; the ESS AI control plane (`.ess-ai/`, `AGENTS.md`, tool adapters, PR template) is the reusable layer.

## Guardrails (built in)
The rules are enforced, not just written down. `python tools/ess_guard.py` reads `.ess-ai/guardrails.json` and:
- **in Claude Code** (hooks in `.claude/settings.json`) blocks risky prompts (production data, destructive data changes, skipping tests or approval, pushing to main, secrets in code), flags architecture changes, vague asks and new dependencies, and denies edits to protected files, undeclared packages, database drivers, SQL in application code, hard-coded secrets, direct database commands, `git add -A`, force-push and push to main;
- **before commit and in CI** (`python tools/ess_guard.py check`) checks the branch against `main` for the same rules plus the Definition of Tested (a code change needs a test change).
Every decision is logged in `.ess-ai/reports/guardrail-log.md`. To add the kit to an existing project, see `ADOPT_EXISTING_PROJECT.md` in the starter pack.

See `START_HERE.md`, `SETUP.md` and `.ess-ai/README.md`.
