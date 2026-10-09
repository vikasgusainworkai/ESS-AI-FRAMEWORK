# Test Data / Fixtures

_When to use:_ When tests depend on realistic scenarios.

```text
Identify the test data required for this feature.
Create safe, reproducible test fixtures for:
- happy path
- edge cases
- negative cases
- authorization cases
- duplicate/retry scenarios
- business-rule failures
Do not use real customer secrets or production-sensitive data.
Keep the data deterministic where possible.
Explain which fixture supports which test.
Run the tests using the fixtures.
```
