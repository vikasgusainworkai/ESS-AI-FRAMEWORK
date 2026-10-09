# CI Failure Analysis

_When to use:_ Use when a pipeline check fails.

```text
Analyze this CI/CD failure.
Do not immediately rewrite code.
Identify:
- failing stage
- exact error
- likely root cause
- whether it is code, test, dependency, configuration, environment or pipeline related
- files actually involved
Propose the minimum safe fix.
Apply only the required change.
Run the failed check again.
Then run the relevant regression checks.
Do not modify unrelated functionality.
```
