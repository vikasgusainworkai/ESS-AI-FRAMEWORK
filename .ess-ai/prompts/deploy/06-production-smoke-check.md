# Production Smoke Check

_When to use:_ Use immediately after an approved deployment.

```text
Run a production smoke verification for the deployed change.
Check only the relevant critical path:
- application loads
- authentication/login
- primary screen
- affected API
- affected business action
- database connectivity where applicable
- integration connectivity where applicable
- obvious runtime/console errors
Report PASS/FAIL for each check with actual evidence.
If anything fails, stop and report the issue. Do not make an unapproved production fix.
```
