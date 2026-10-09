# Testing Checklist — Definition of Tested

AI can write the code, write the tests and run the tests. The developer owns the verification.

- [ ] Relevant tests executed
- [ ] New behavior covered
- [ ] Happy path checked
- [ ] Edge cases checked
- [ ] Negative cases checked
- [ ] Error handling checked (no sensitive data leakage)
- [ ] Regression tests run
- [ ] Failures investigated (root cause, not re-run until green)
- [ ] Evidence available (command output, report, screenshots, API responses)

## Choose the test based on the change

| What changed | Required tests |
|---|---|
| Function / service | Unit tests + edge / negative |
| API | API + integration + auth |
| UI / React | Component + E2E + regression |
| Business / ERP logic | Source-of-truth validation |
| Existing application | Regression + smoke |

## ESS-specific cases

| Case | Test for |
|---|---|
| RAG / pgvector | Retrieval quality, grounding, stale data |
| Agent / MCP | Tool permissions, wrong tool calls, tool failure |
| Multi-tenancy | Tenant isolation, authorization |
| Customer environment | Environment-specific validation |
| Screen-level flow | AI testing agent with expected vs actual evidence |

Use `prompts/testing/12-final-test-report.md` and save the result in `.ess-ai/reports/`.
