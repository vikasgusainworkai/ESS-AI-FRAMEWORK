# Production Readiness Checklist — Deployment Gates

AI can prepare the change. Humans approve the release. A successful local build is not a production deployment.

| Gate | Must be true | Evidence |
|---|---|---|
| 01 Understand | Developer can explain the change and affected architecture | |
| 02 Review | Git diff clean; unrelated/generated changes removed | |
| 03 Test | Relevant automated/manual tests executed | |
| 04 Secure | Secrets, dependencies, auth and data boundaries checked | |
| 05 Approve | PR / reviewer / UAT approval completed where required | |
| 06 Release | Rollback, monitoring and production owner are known | |

## Staging / UAT
- [ ] Same build deployed that is intended for production
- [ ] Smoke and relevant regression tests run
- [ ] Customer / business behavior validated
- [ ] Evidence captured; approval obtained where required

## Production
- [ ] Release approval, backup / rollback path and owner confirmed (`templates/rollback-plan.md`)
- [ ] Deployed using the approved process
- [ ] Production smoke check run (`prompts/deploy/06-production-smoke-check.md`)
- [ ] Logs / errors monitored; result recorded (`templates/deployment-evidence.md`)

## If CI/CD is not available
Still required: Git diff → review → tests → security checks → deployment checklist → approval → deployment → smoke test → evidence. Capture command output, test results, screenshots/logs, deployment version and approval instead of pretending a missing pipeline exists. In customer environments follow the customer-approved process but keep the same gates.
