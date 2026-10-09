# Pre-Commit Review

_When to use:_ Use before git commit.

```text
Review the changes I am about to commit.
Do not modify code yet.
Check:
- requirement vs implementation
- git diff and changed files
- unnecessary/generated code
- unrelated changes
- secrets, credentials and customer data
- new dependencies
- database/API/configuration impact
- security risks
- missing tests
- regression risk
Tell me what must be fixed before commit.
Do not claim the change is safe without evidence.
```
