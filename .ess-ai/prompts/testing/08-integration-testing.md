# Integration Testing

_When to use:_ For API → DB, React → API, ERP or service integrations.

```text
Review the integration points affected by this change.
Create tests for:
- successful integration
- invalid downstream response
- timeout
- unavailable dependency
- malformed response
- authentication failure
- authorization failure
- retry behavior where applicable
- data mapping errors
Use mocks only where the real dependency is not appropriate for the test.
Run the integration tests and report actual results.
```
