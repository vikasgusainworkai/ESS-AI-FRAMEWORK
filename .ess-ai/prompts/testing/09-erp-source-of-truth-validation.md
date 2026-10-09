# ERP / Source-of-Truth Validation

_When to use:_ For ESS ERP, finance, transaction or AI-assisted data flows.

```text
Validate this AI-assisted implementation against the system of record.
Identify the source-of-truth fields and expected business rules first.
Compare:
- input
- transformed data
- calculation/business rule
- stored result
- API response
- UI result
Test normal, boundary and invalid cases.
If AI output differs from the source of truth, do not assume the AI result is correct. Show the mismatch and identify where it was introduced.
```
