# ESS Bootstrap Prompt — Python

Paste this as the first message in every new AI session (your tool may also load it automatically through `AGENTS.md` / `CLAUDE.md` / tool rules).

```text
You are working inside an ESS Python project.
Read the .ess-ai rules and project context first
(.ess-ai/rules/, then .ess-ai/context/about.md, requirements.md, architecture.md,
security.md, testing.md, reuse-catalog.md and any other context relevant to the request).
Inspect the repository, pyproject.toml, src/, tests/, API contracts and configuration.
Do not modify any files yet.
Do not invent business rules, APIs, database fields, dependencies or architecture.
Mark missing material facts as UNKNOWN.
Then give me:
1. Your understanding
2. Files/modules likely to change
3. Data/API/security/tenant impact
4. Implementation plan (small phases, each with its verification steps)
5. UNKNOWNs or risks
STOP and wait for my approval before coding.
```
