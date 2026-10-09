# Add this kit to an EXISTING Python project

You do not rewrite anything. You copy the ESS control plane and guardrails next to your code; your source, tests and dependency files stay as they are. Do it as one PR approved by the tech lead.

## 1. Copy the control plane (Windows PowerShell, in your project folder)

```
git checkout -b chore/adopt-ess-kit
$K = "C:\path\to\python-ai-starter"
robocopy $K . /E /XD "$K\src" "$K\tests" "$K\.github\workflows" "$K\.ess-ai\adopt" /XF "$K\README.md" "$K\SETUP.md" "$K\START_HERE.md" "$K\ADOPT_EXISTING_PROJECT.md" "$K\pyproject.toml" "$K\.gitignore" "$K\.pre-commit-config.yaml" "$K\.env.example"
```

Robocopy exit codes 1 to 3 mean success. If your project already has a file with the same name (for example its own `AGENTS.md`), merge it by hand.

## 2. Add the guardrails CI

Your own CI stays. Add the ESS workflow next to it:

```
mkdir .github\workflows -Force
copy $K\.ess-ai\adopt\ess-guardrails.yml .github\workflows\ess-guardrails.yml
```

It runs a secret scan on every push and the guardrail check (with your tests) on every PR.

## 3. Tell the guardrails about your project (tech lead)

Edit `.ess-ai/guardrails.json`:

| Setting | Set it to |
|---|---|
| `code_dirs` | Folders with application code (default `src/`, `app/`, `lib/`) |
| `test_dirs` | Folders with tests (default `tests/`, `test/`) |
| `test_command` | How you run the tests. Empty = auto: `pytest` if installed, else `unittest`; `npm test` when there is a `package.json` |
| `protected_paths` | Add what AI must never edit: data files, migrations, infrastructure, fixtures |
| `blocked_imports` | Database drivers / clients your architecture does not allow in application code |
| `allow_sql_in_code` | `true` only if your architecture has SQL in the application layer |

Then check `.ess-ai/automation.json`: `autotest_command` (the fast test command run after every AI edit, for example `python -m pytest -q --no-cov`), `remote`, `open_pr`, and `after_ship` (an optional command run after a push, for example to update your ticket).

## 4. Fix AGENTS.md and .gitignore

In `AGENTS.md`, replace the kit's verification commands with the ones your project really uses and keep the `python tools/ess_guard.py check` line. Add `.env` and `.ess-ai/reports/guardrail-log.md` to `.gitignore`.

## 5. Commit as one PR

```
git add .ess-ai .claude .cursor .amazonq .kiro .github AGENTS.md CLAUDE.md GEMINI.md .gitleaks.toml AI_CHANGE_REPORT_TEMPLATE.md tools .gitignore
git commit -m "Adopt ESS starter kit and guardrails"
python tools\ess_guard.py check
```

The check reports `FAIL` on this branch because every added file is protected. That is expected: the framework protects itself, so adopting or changing it is always a human, tech-lead-approved PR. Merge it; from the next branch on, normal work passes.

## 6. Let AI fill the project truth, then start

1. Open the project in Claude Code and accept "trust this folder" so the hooks run (or use another approved AI tool).
2. Run `/ess-bootstrap`. With empty context the AI marks architecture, data, security and tenancy as UNKNOWN instead of guessing.
3. Ask: "Draft the .ess-ai/context files from the existing code. Mark anything the code does not show as UNKNOWN. Show me the drafts first, do not write yet." Review, correct, approve, commit.
4. Run `/ess-bootstrap` again, then work ticket by ticket: plan, approve, test first, implement, `/ess-check`, PR.

The hooks call `python`. If that is not on PATH, change the two commands in `.claude/settings.json` (for example `py -3.12` on Windows).
