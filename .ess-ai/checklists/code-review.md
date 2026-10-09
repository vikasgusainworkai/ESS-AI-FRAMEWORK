# Code Review Checklist

Run `prompts/dev/06-code-review.md` (AI review) and then review as a human. AI review does not replace human approval.

- [ ] Change matches the requirement and approved plan; nothing extra
- [ ] Correctness: logic, edge cases, error paths
- [ ] Architecture preserved; material changes were approved separately
- [ ] No unnecessary complexity, abstraction or generated bloat
- [ ] Dependency impact reviewed
- [ ] DB / API contract changes are backward compatible or approved
- [ ] Security and tenant isolation reviewed (`checklists/security.md`)
- [ ] Tests are meaningful (assertions prove behavior) and were executed
- [ ] Regression risk identified
- [ ] AI-assisted areas identified in the PR
- [ ] Findings listed by severity with specific fixes
