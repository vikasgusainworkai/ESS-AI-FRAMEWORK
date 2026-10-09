# Git Rule
Use focused branches and commits. Review the diff before PR. Do not commit secrets or generated artifacts unnecessarily.
- One ticket per branch: `<type>/<ticket>-<summary>` cut from main. Never commit or push to main; never force-push.
- AI never commits or pushes on its own. After the developer approves the diff, the change is shipped with `python tools/ess_ship.py`, which re-runs the guardrail check and the tests, commits only the named files and pushes the branch.
- Every commit message starts with the ticket id and records the test result and who approved it.
