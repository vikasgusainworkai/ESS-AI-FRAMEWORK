# Coverage Gap Review

_When to use:_ Use before declaring the change tested.

```text
Review the current tests against the implementation and requirement.
Identify missing coverage for:
- business rules
- branches/conditions
- error paths
- edge cases
- negative cases
- integration points
- user flows
Do not chase a coverage percentage blindly. Prioritize behavior that carries business, security or regression risk.
Add the highest-value missing tests and run them.
```
