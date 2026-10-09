# ESS AI Rules

1. AI generates or assists; engineers understand, review, validate, secure, test and approve.
2. Read `.ess-ai/context/` and applicable rules before changing code.
3. Requirement → Understand → Impact → Plan → Approval → Implement → Test → Review.
4. Never guess missing business, architecture, DB, API or security facts. Mark them `UNKNOWN`.
5. Keep AI changes small, focused and traceable.
6. Reuse existing patterns before creating new ones.
7. No secrets, customer credentials or restricted data in unapproved AI tools.
8. No unrestricted DB or production access for AI.
9. No silent architecture, DB, auth or dependency changes.
10. Generated tests must be reviewed for meaningful assertions.
11. Do not claim a test, scan or deployment was performed unless evidence exists.
12. Before PR, produce an AI Change Report.
