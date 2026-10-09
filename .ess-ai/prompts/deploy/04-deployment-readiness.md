# Deployment Readiness

_When to use:_ Use before staging or production deployment.

```text
Review whether this change is ready for deployment.
Check:
- requirement completed
- tests executed and passed
- regression coverage
- build/package success
- secrets/configuration readiness
- database migration impact
- API compatibility
- dependency changes
- security checks
- logging/monitoring
- rollback plan
- customer impact
- environment-specific configuration
- approval requirements
Return:
READY / NOT READY / UNKNOWN
with evidence for every decision.
Do not deploy or change production.
```
