# Rollback Planning

_When to use:_ Use before a high-impact release.

```text
Review this change and create a rollback plan.
Identify:
- deployment artifact/version
- files or services affected
- database migration impact
- data compatibility risks
- configuration changes
- dependency changes
- exact rollback trigger
- rollback steps
- post-rollback smoke checks
- owner/approval required
If rollback is unsafe or unknown, say so explicitly.
Do not execute rollback.
```
