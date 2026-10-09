# ESS Workflow — Quality Gate Feedback Loop

AI change → Push → Quality / security check → PASS, or REJECT + exact failure → AI analyzes (`prompts/deploy/03-ci-failure-analysis.md`) → minimum fix → re-run failed check → re-run regression checks → Push / PR

Never bypass the gate (`--no-verify`, skipped tests, disabled rules). A green-looking explanation is not evidence; only the actual check result is.
