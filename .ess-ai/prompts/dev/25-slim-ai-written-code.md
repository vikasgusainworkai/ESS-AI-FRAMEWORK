# Slim AI-Written Code

_When to use:_ When AI-generated code is much longer than the feature needs and you want fewer lines with exactly the same behaviour. In Claude Code use `/ess-slim <folder>`; in other AI tools paste the prompt below.

```text
Make the code in <files or folders> smaller without changing its behaviour (same inputs, outputs, errors, side effects and public names).
1. Confirm the working tree is committed and that python -m pytest -q, ruff check ., ruff format --check ., mypy src pass. Stop if not.
2. Where coverage is missing, add characterization tests that pin the current behaviour; they must pass on the unchanged code.
3. List the cuts, biggest first: dead code, hand-rolled standard library, wrappers or abstractions with one caller, config nobody sets, logic that can be shorter. Search the repo for every symbol before deleting it.
4. Keep out anything that changes a public signature, route or response shape, removes validation, error handling, security or accessibility, or touches a protected or dependency file.
5. Apply one cut at a time and run the tests after each; undo any cut that turns a test red. Never edit a test to make a cut pass.
6. Run all checks again plus python tools/ess_guard.py check and python tools/ess_loc.py. Report lines before and after, each cut (applied, undone or kept out, with the reason) and the check results, then stop for approval.
```
