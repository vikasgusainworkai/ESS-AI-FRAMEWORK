# ESS Workflow

Reproduce → Evidence → Root Cause → Minimal Fix → Regression → Verify → Review → PR

## Step by step (Claude Code: `/ess-fix <ticket>`)
1. **Reproduce and gather evidence**: read the ticket, the code and the existing tests; run the tests for a baseline.
2. **Root cause and plan**: file:line evidence, smallest fix, the regression test to add, UNKNOWNs. **STOP for developer approval.**
3. **Regression test first (red)**: the auto-test hook shows the new test failing for the reported reason.
4. **Minimal fix (green)**: the auto-test hook and a full test run show everything passing.
5. **Review**: `git diff`, one line per change, every acceptance criterion mapped to a test. **STOP for developer approval.**
6. **Ship**: `python tools/ess_ship.py` (permission prompt = approval) commits and pushes the fix branch; then open or review the PR.
