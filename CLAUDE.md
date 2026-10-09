# Claude Code — ESS project

@AGENTS.md

Project slash commands live in `.claude/commands/` and wrap the ESS prompt library.

Before every commit run `python tools/ess_guard.py check` and fix every FAIL. Protected files are listed in `.ess-ai/guardrails.json`; never change them or work around a guardrail.

## Test, approve, commit and push (automated)
- After every edit to code or tests, the `tools/ess_autotest.py` hook runs the tests and shows GREEN or RED in this chat. Use that evidence; never weaken a test to make it pass.
- Fix work goes test-first with two stops: the developer approves the plan, then approves the diff (`/ess-fix <ticket>`).
- Never run `git commit` or `git push` yourself (they are denied). When the developer approves the diff, run `python tools/ess_ship.py --ticket <ID> --title "<summary>" --files <changed files>` (`/ess-ship <ticket>`). Claude Code shows a permission prompt for it: that is the approval gate. The script re-checks the guardrails and tests, creates the branch, commits only those files and pushes the branch.
