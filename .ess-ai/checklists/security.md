# Security Checklist — before staging / production

Run `prompts/dev/07-security-review.md`. Every item needs evidence, not an assertion.

- [ ] Authentication enforced on every non-public route / API
- [ ] Authorization checked per action and per tenant
- [ ] Tenant context carried through API, DB, files, vector store, caches, agent tools and logs
- [ ] No SQL injection (parameterized queries / ORM only)
- [ ] Input validated and output encoded
- [ ] API exposure reviewed (no unintended endpoints, CORS restricted)
- [ ] No secrets or tokens in code, logs, prompts, front-end bundles or Git history (gitleaks clean)
- [ ] Database access least-privilege; AI/agents have no unrestricted DB access
- [ ] No customer-data exposure in responses, logs or AI tool inputs
- [ ] Dependency audit clean or exceptions approved (`npm audit` / `pip-audit`)
- [ ] Sensitive data not logged
- [ ] Error responses do not leak stack traces or internals
- [ ] MCP / agent tools have bounded identity, permissions, input/output validation, audit and timeouts
- [ ] Only ESS-approved AI tools and accounts used (`context/approved-tools.md`)
