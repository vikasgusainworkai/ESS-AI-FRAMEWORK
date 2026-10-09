# ESS Prompt Library — Index

These prompts mirror the ESS AI Framework (pages 05, 06, 07, 08 and 10). Project context and `.ess-ai/rules/` remain the source of truth. Copy the text block of a prompt into your AI chat, or invoke it as a slash command where your tool supports it.

## Core flow (use in this order)

| File | Purpose |
|---|---|
| [ESS_BOOTSTRAP_PROMPT.md](ESS_BOOTSTRAP_PROMPT.md) | First prompt in every new session |
| [01-discover.md](01-discover.md) | Discover the repository |
| [02-requirement.md](02-requirement.md) | Analyze the requirement |
| [03-plan.md](03-plan.md) | Phased implementation plan |
| [04-implement.md](04-implement.md) | Implement an approved phase |
| [05-bugfix.md](05-bugfix.md) | Bug fix flow |
| [06-test.md](06-test.md) | Test plan |
| [07-review.md](07-review.md) | Senior review |
| [08-security.md](08-security.md) | Security review |
| [09-change-report.md](09-change-report.md) | AI Change Report |

## Developer prompts (framework page 05)

| File | When to use |
|---|---|
| [Understand The Project](dev/01-understand-the-project.md) | Use before starting a new task. |
| [Create An Implementation Plan](dev/02-create-an-implementation-plan.md) | Use when the requirement is ready. |
| [Implement The Approved Plan](dev/03-implement-the-approved-plan.md) | Use only after the developer approves. |
| [Debug A Failure](dev/04-debug-a-failure.md) | Use when code or tests fail. |
| [Test The Change](dev/05-test-the-change.md) | Use after implementation. |
| [Code Review](dev/06-code-review.md) | Use before commit or PR. |
| [Security Review](dev/07-security-review.md) | Use before staging or production. |
| [Token-Saving Prompt](dev/08-token-saving-prompt.md) | Use when you want to reduce unnecessary AI input and token usage. |
| [Clarify An Ambiguous Requirement](dev/09-clarify-an-ambiguous-requirement.md) | When the requirement is incomplete or unclear. |
| [Analyze Existing Code First](dev/10-analyze-existing-code-first.md) | When working in an existing customer or legacy application. |
| [Reduce A Large Ai Change](dev/11-reduce-a-large-ai-change.md) | When AI has changed too many files or generated too much code. |
| [Analyze Logs / Error Message](dev/12-analyze-logs-error-message.md) | When debugging is taking too long. |
| [Check Dependency Impact](dev/13-check-dependency-impact.md) | Before adding a package or changing a dependency. |
| [Generate Pr Description](dev/14-generate-pr-description.md) | Before creating a pull request. |
| [Turn A Bug Into A Reproducible Test](dev/15-turn-a-bug-into-a-reproducible-test.md) | When a bug is fixed and you want to prevent it returning. |
| [Report Unknowns Before Coding](dev/16-report-unknowns-before-coding.md) | When AI does not have enough context. |
| [Find Reusable Existing Implementation](dev/17-find-reusable-existing-implementation.md) | When you suspect ESS already solved something similar. |
| [Check Database Change Safety](dev/18-check-database-change-safety.md) | Before changing PostgreSQL / Oracle / other database structures. |
| [Right AI Tool Or Model For The Job](dev/23-right-ai-tool-or-model-for-the-job.md) | Before starting a task, to pick an approved tool/model category. |
| [Debug From Evidence](dev/24-debug-from-evidence.md) | When debugging; give exact console/network/log evidence instead of screenshots. |

## Manager / lead prompts (page 05)

| File | When to use |
|---|---|
| [Requirement & Scope Summary](lead/19-requirement-scope-summary.md) | For a lead/manager who needs a quick understanding before work starts. |
| [Ai Work Status Summary](lead/20-ai-work-status-summary.md) | For daily/weekly reporting without reading every AI conversation. |
| [Review Ai Change Risk](lead/21-review-ai-change-risk.md) | Before approving a significant AI-generated change. |
| [Release Readiness Summary](lead/22-release-readiness-summary.md) | Before staging/UAT/production approval. |

## Testing prompts (page 06)

| File | When to use |
|---|---|
| [Full Test Planning](testing/01-full-test-planning.md) | Use immediately after completing a feature. |
| [Unit Test Generation](testing/02-unit-test-generation.md) | For a function, service, utility or component. |
| [API Testing](testing/03-api-testing.md) | For REST/API changes. |
| [UI / E2E Testing](testing/04-ui-e2e-testing.md) | For React or screen-level business flows. |
| [Regression Testing](testing/05-regression-testing.md) | Use after changing existing functionality. |
| [Failure Analysis](testing/06-failure-analysis.md) | Use when an AI-generated test fails. |
| [Test Data / Fixtures](testing/07-test-data-fixtures.md) | When tests depend on realistic scenarios. |
| [Integration Testing](testing/08-integration-testing.md) | For API → DB, React → API, ERP or service integrations. |
| [ERP / Source-of-Truth Validation](testing/09-erp-source-of-truth-validation.md) | For ESS ERP, finance, transaction or AI-assisted data flows. |
| [Smoke Test Before Demo](testing/10-smoke-test-before-demo.md) | Quick check before sharing a build with a customer or team. |
| [Coverage Gap Review](testing/11-coverage-gap-review.md) | Use before declaring the change tested. |
| [Final Test Report](testing/12-final-test-report.md) | Use as the final verification step before PR/review. |

## Code review prompts (page 07)

| File | When to use |
|---|---|
| [Slim AI-Written Code](dev/25-slim-ai-written-code.md) | When AI code is much longer than it needs to be; cut lines without changing behaviour (`/ess-slim` in Claude Code). |
| [Code Review](dev/06-code-review.md) | Before commit or PR (`/ess-review`). Over-engineering only: `/ponytail-review` (diff) or `/ponytail-audit` (repo). |
| [Reduce A Large Ai Change](dev/11-reduce-a-large-ai-change.md) | When AI has changed too many files or generated too much code. |

## Git / PR / CI-CD / deployment prompts (page 08)

| File | When to use |
|---|---|
| [Pre-Commit Review](deploy/01-pre-commit-review.md) | Use before git commit. |
| [PR Preparation](deploy/02-pr-preparation.md) | Use after tests pass and before opening a PR. |
| [CI Failure Analysis](deploy/03-ci-failure-analysis.md) | Use when a pipeline check fails. |
| [Deployment Readiness](deploy/04-deployment-readiness.md) | Use before staging or production deployment. |
| [Release Notes](deploy/05-release-notes.md) | Use for the release/change record. |
| [Production Smoke Check](deploy/06-production-smoke-check.md) | Use immediately after an approved deployment. |
| [Rollback Planning](deploy/07-rollback-planning.md) | Use before a high-impact release. |
| [Final Deployment Evidence](deploy/08-final-deployment-evidence.md) | Use to close the release record. |

## AI Knowledge Hub (page 10)

| File | When to use |
|---|---|
| [Create ESS AI Knowledge Document](knowledge/01-create-ess-ai-knowledge-document.md) | After completing a new reusable AI implementation (MCP, agent, RAG, integration, automation). |
