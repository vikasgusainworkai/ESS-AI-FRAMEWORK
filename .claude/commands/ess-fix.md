---
description: Fix a ticket or bug test-first, then stop for approval to commit and push
argument-hint: <ticket id or bug description>
---

Work on this ticket / bug with the ESS bug-fix workflow (`.ess-ai/workflows/bug-fix.md`): $ARGUMENTS

1. **Understand.** Read the ticket (if the project has a ticket tool, it is named in `CLAUDE.md`), the code it touches and the existing tests. Run the tests once to get the baseline.
2. **Plan, then STOP.** Reply with: root cause with file:line evidence, the smallest fix, the regression test you will add, the files you will change, risks and UNKNOWNs. Do not change any file yet. Wait for the developer to approve.
3. **Red.** After approval, add a regression test that reproduces the bug (one new test file named after the ticket, or new cases in the matching test file). The ESS auto-test hook runs the suite after every edit; confirm the new test fails for the reason in the ticket.
4. **Green.** Make the smallest code change that fixes the root cause. Follow existing patterns, no unrelated refactoring, no new dependencies. Confirm the auto-test result is green; run the full test command yourself and quote the exact result.
5. **Review, then STOP.** Show `git diff` and `git status`, summarise each change in one line, map every acceptance criterion to a test, and ask: "Approve commit and push?" Do not commit or push yourself.
6. When the developer approves, follow `/ess-ship` for this ticket.
