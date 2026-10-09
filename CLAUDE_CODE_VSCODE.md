# Claude Code in VS Code — prompt, test, approve, commit and push

This kit turns Claude Code into the ESS workflow: you type prompts, Claude plans and stops, writes a failing test, fixes the code while the tests run automatically after every edit, shows you the diff and stops again. When you approve, one command commits and pushes the branch for you.

## One-time setup (Windows)

1. Install **VS Code**, **Git for Windows** and **Python 3.12** (`py -3.12 --version`).
2. Install Claude Code: in PowerShell run `irm https://claude.ai/install.ps1 | iex` (or `npm install -g @anthropic-ai/claude-code`), then install the **Claude Code** extension in VS Code (Extensions, search "Claude Code").
3. Open the project folder in VS Code (**File > Open Folder**) and open a terminal (**Ctrl+`**).
4. Create and activate the virtual environment, then install:
   ```
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -e ".[dev]"
   ```
   (If PowerShell blocks the script: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, or use `.venv\Scripts\activate.bat` in cmd.)
5. Check the project is green: `python -m pytest -q`
6. Make sure git knows you and has a remote:
   ```
   git config user.name "Your Name"
   git config user.email "you@company.com"
   git remote -v
   ```
   If there is no `origin`, add your company repository: `git remote add origin <url>` and `git push -u origin main`.
7. Start Claude Code in the same terminal: `claude`. Sign in with your ESS-approved account. Accept **"trust this folder"** so the hooks in `.claude/settings.json` run. (You can also click the Claude icon in the editor toolbar; the extension shows Claude's edits as VS Code diffs.)
8. Type `/hooks` once to confirm three hooks are listed: the prompt guard, the tool guard and the **ESS auto-test**.

## Every task: the prompts you type

| Step | You type in Claude Code | What happens |
|---|---|---|
| 1 | `/ess-bootstrap` | Claude reads the rules and context, explains the project, marks UNKNOWNs. No files change. |
| 2 | `/ess-fix ABC-123 <paste the ticket text>` | Claude reads the code and the tests, runs the baseline, then gives the root cause, the plan and the test it will add. **It stops.** |
| 3 | `Approved. Write the failing test first, then fix it.` | Claude writes the regression test. The **ESS auto-test** hook runs the suite after the edit: `RED`. Claude makes the smallest fix. Auto-test: `GREEN`. VS Code asks you to accept each edit unless you chose auto-accept. |
| 4 | `Show me the diff and map each acceptance criterion to a test.` | `git diff` plus a short review. **It stops** and asks "Approve commit and push?" |
| 5 | `Approved, commit and push.` | Claude runs `python tools/ess_ship.py --ticket ABC-123 --title "..." --files ...`. **Claude Code shows a permission prompt: choose Yes.** The script re-runs the guardrail check and the tests, creates `fix/ABC-123-...`, commits only those files and pushes the branch. With a GitHub remote and the `gh` CLI it also opens the PR. |
| 6 | (terminal) `git log --oneline -3` and `git branch -vv` | You see the commit and that the branch tracks `origin`. Open the PR and let CI run. |

You can also type the steps as plain prompts; `/ess-fix` and `/ess-ship` just save typing.

## Slim AI-written code: `/ess-slim`

When AI has produced far more code than the feature needs (one function, 2,000 lines), type:

```
/ess-slim src/ess_app
```

(Or `/ess-slim` alone for every code folder.) In one run Claude:

1. checks the working tree is committed and that `python -m pytest -q`, `ruff check .`, `ruff format --check .`, `mypy src` are green before it starts;
2. adds characterization tests (`tests/test_slim_<module>.py`) that pin what the code does today, wherever coverage is missing;
3. analyses the code with the bundled **ponytail-audit** skill: dead code, hand-written versions of the standard library, wrappers and abstractions with one caller, longer-than-needed logic;
4. applies the cuts one at a time; the auto-test hook runs after each edit and any cut that turns a test red is undone;
5. runs every check again plus `python tools/ess_guard.py check` and shows the line count before and after (`python tools/ess_loc.py`), then **stops** and asks "Approve commit and push?". Ship it with `/ess-ship` as `--type refactor`.

It never removes input validation, error handling, security or accessibility, never changes a public name, route or response shape, and never edits an existing test to make a cut pass. Want only the list of cuts? Use `/ponytail-review` on your diff or `/ponytail-audit` on the repo; both report and change nothing.

## Why this is safe

- **Approval is enforced, not promised.** `git commit` and `git push` are denied for Claude in `.claude/settings.json`; the only way to ship is `python tools/ess_ship.py`, which is on the **ask** list, so you get a permission prompt every time.
- **Nothing red can ship.** The ship command runs the guardrail check (protected files, dependencies, secrets, architecture, Definition of Tested: a code change needs a test change) and the tests first. Any FAIL stops it before the commit.
- **Only your branch is pushed.** Never main, never force. Only the files named are committed (never `git add -A`).
- **Evidence everywhere.** The commit message carries the ticket id, the test result and who approved it; guardrail decisions are logged in `.ess-ai/reports/guardrail-log.md`.

## Settings (tech lead): `.ess-ai/automation.json`

| Key | Meaning |
|---|---|
| `autotest_command` | Fast test command run after every AI edit (default `python -m pytest -q --no-cov`) |
| `remote` | Remote the branch is pushed to (default `origin`) |
| `branch_types` | Allowed branch prefixes (`fix`, `feat`, ...) |
| `open_pr` | `auto` opens a PR with the GitHub CLI when available; `off` never |
| `after_ship` | Optional command run after a push, e.g. to move your ticket. Placeholders: `{ticket}`, `{branch}`, `{commit}`, `{evidence}` (a JSON file with branch, commit, tests, files and diff). |

## If something goes wrong

| Problem | Fix |
|---|---|
| Hooks do nothing / `python` or `node` not found | Start `claude` from the VS Code terminal where the virtual environment is active (`python --version` shows 3.12). |
| The ship command STOPPED | Read the FAIL lines. Fix the cause (usually a missing test or a red test), then say "ship again". Nothing was committed. |
| Push failed | The commit is safe on your branch. Check `git remote -v` and your access, then `git push -u origin <branch>` yourself. |
| You chose "don't ask again" by mistake | Ask rules always prompt; if it stopped asking, check `.claude/settings.local.json` and remove the allow entry. |
