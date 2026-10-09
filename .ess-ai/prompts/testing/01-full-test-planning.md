# Full Test Planning

_When to use:_ Use immediately after completing a feature.

```text
Review the implementation I just completed against the requirement.
Do not modify the implementation yet.
First identify the required test scenarios:
1. Happy path
2. Edge cases
3. Negative cases
4. Validation and error handling
5. Regression risks
6. Integration/API impact
7. End-to-end/user-flow impact where applicable
Review existing tests and identify missing coverage.
Create or update the appropriate tests.
Run the relevant test suite.
If anything fails, analyze the root cause before changing code.
Do not modify unrelated functionality.
Report:
- Tests added/changed
- Tests executed
- Passed
- Failed
- Coverage gaps
- Remaining risks
- UNKNOWNs
Do not claim a test passed without execution evidence.
```
