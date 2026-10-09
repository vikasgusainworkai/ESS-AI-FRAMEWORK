---
description: Cut the line count of AI-written code without changing what it does, proven by the tests, lint and type checks
argument-hint: [files or folders, default all code folders] [ticket id]
---

Make this code smaller without changing its behaviour: $ARGUMENTS

Scope: the files or folders named above; if none are named, every `code_dirs` folder in `.ess-ai/guardrails.json`. Behaviour means: the same inputs give the same outputs, errors, status codes and side effects, and every name that other code, tests or users import or call keeps working. Follow `.ess-ai/workflows/refactor.md`. Work without stopping until step 7.

1. **Clean start.** Run `git status`. If a file in scope has uncommitted changes, STOP and ask the developer to commit or stash them first, so every cut can be compared with the last commit.
2. **Baseline, all green.** Run `python tools/ess_loc.py <scope>` and keep the result. Run `python -m pytest -q`, `ruff check .`, `ruff format --check .` and `mypy src`. If any of them fails before you change anything, STOP and report it: slimming needs a green baseline.
3. **Lock the behaviour.** Read the coverage report from step 2 (`--cov-report=term-missing`). For each function, class, route or CLI in scope with uncovered lines, add characterization tests in `tests/test_slim_<module>.py` that pin what the code does today: normal results, edge cases, error paths. Run them; they must pass on the unchanged code. Existing tests stay as they are.
4. **Analyse.** Use the `ponytail-audit` skill on the scope (`.claude/skills/ponytail-audit/SKILL.md`): a numbered list of what to delete, replace with the standard library or an installed package, reuse from this repo, inline (`yagni`) or shorten (`shrink`), biggest cut first. Grep the whole repo for every symbol before you plan to delete it. Keep a finding out of the plan, with the reason, when it would:
   - change a public signature, route, response shape, config key or log/audit line that something outside the scope may use;
   - drop input validation at a trust boundary, error handling, security, accessibility or anything an ESS rule requires;
   - touch a protected or dependency file (`.ess-ai/guardrails.json`); removing a package is listed as "needs approval" only.
5. **Cut, one finding at a time,** biggest first: one edit per finding, never one rewrite of the whole file, so a red test points at one cut. After each edit the ESS auto-test hook runs the tests. If it is RED, undo that edit exactly and mark the finding "reverted" with the failing test. Never change an existing or characterization test to make a cut pass. Follow `.ess-ai/rules/03-coding.md`; no new dependencies, files or abstractions.
6. **Prove it.** Run `python -m pytest -q`, `ruff check .`, `ruff format --check .`, `mypy src`, `python tools/ess_guard.py check` and `python tools/ess_loc.py <scope>`. Fix lint or type failures you caused; if a cut cannot be made clean, undo it.
7. **Report, then STOP.** Reply with:
   - the line count before and after (per file and total, from `ess_loc.py`);
   - each finding: applied, reverted (failing test) or kept out (reason);
   - the characterization tests you added;
   - the exact result line of every check in step 6;
   - `git diff --stat`.
   Then ask: "Approve commit and push?" When the developer approves, follow `/ess-ship` with `--type refactor`.
