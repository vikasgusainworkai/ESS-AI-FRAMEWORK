# ESS Workflow — Release

Git diff → Commit → PR → CI checks (secret scan, lint/format, typecheck, tests, dependency audit, build) → Staging / UAT (same build) → Approval → Production → Smoke check → Monitor → Deployment evidence

Templates: `templates/release-notes.md`, `templates/rollback-plan.md`, `templates/deployment-evidence.md`. Gates: `checklists/production-readiness.md`.
