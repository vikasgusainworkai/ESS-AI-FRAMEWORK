# START HERE — ESS Python Vibe Coder

1. Copy the complete `python-ai-starter` folder and rename it to your project name. Keep `.ess-ai/`, `AGENTS.md` and the tool folders.
2. Follow `SETUP.md` (Python 3.12+, install, `pre-commit install`, run the checks once so you start green).
3. Open the folder in VS Code / your approved AI IDE. Claude Code, Copilot, Cursor, Amazon Q, Kiro and Gemini/Antigravity load `AGENTS.md` automatically through their adapter files.
4. Fill `.ess-ai/context/` (about, requirements, architecture, database-schema, api-contracts, security, testing, approved-tools).
5. Run the ESS bootstrap prompt (`.ess-ai/prompts/ESS_BOOTSTRAP_PROMPT.md`, or `/ess-bootstrap` in Claude Code).
6. Review and approve the plan.
7. Implement one small phase at a time.
8. Test against the Definition of Tested (`.ess-ai/checklists/testing.md`).
9. Review the diff, run the security review, and write the AI Change Report in `.ess-ai/reports/`.
10. Run `python tools/ess_guard.py check` (`/ess-check` in Claude Code) and fix every FAIL.
11. Approve the diff; Claude ships it with `python tools/ess_ship.py` (`/ess-ship`), which commits and pushes your branch. See `CLAUDE_CODE_VSCODE.md`.
12. Open the PR (the template is pre-filled with the ESS sections).

Never give AI unrestricted production DB access and never paste production secrets into prompts.

The guardrails in `.ess-ai/guardrails.json` are enforced by Claude Code hooks and by CI. Only the tech lead changes that file, in a reviewed PR with an ADR.
