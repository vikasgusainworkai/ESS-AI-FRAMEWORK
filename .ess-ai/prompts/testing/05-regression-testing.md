# Regression Testing

_When to use:_ Use after changing existing functionality.

```text
The implementation has changed.
Review the changed files and identify functionality that could be affected.
Run the relevant existing tests and identify missing regression tests.
Check:
- existing screens
- shared components
- APIs
- business rules
- database interactions
- authentication/authorization
- integrations
- related user flows
Add only the regression tests required for the affected behavior.
Run them and report passed, failed and remaining regression risks.
```
