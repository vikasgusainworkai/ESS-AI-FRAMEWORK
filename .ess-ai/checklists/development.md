# Development Checklist

## Before coding
- [ ] Project context in `.ess-ai/context/` is filled and current
- [ ] Requirement analyzed; acceptance criteria written; UNKNOWNs listed
- [ ] Reuse catalogue checked for an existing ESS implementation
- [ ] Implementation plan reviewed and approved by the developer

## While coding
- [ ] Only the approved phase is implemented
- [ ] Existing architecture and patterns preserved
- [ ] No new dependency without approval (`prompts/dev/13-check-dependency-impact.md`)
- [ ] No secrets, customer data or production credentials in code or prompts

## Git diff (framework page 08)
- [ ] Every changed file reviewed
- [ ] Unneeded generated code removed
- [ ] No unrelated files, debug code, secrets or surprise dependency changes
- [ ] Business impact understood before committing

## Commit
- [ ] One logical change, meaningful message
- [ ] No `.env`, credentials, customer data or generated artifacts committed
- [ ] Pre-commit hooks passed (not bypassed)
- [ ] `.ess-ai/context/progress.md` updated
