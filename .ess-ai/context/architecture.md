# Approved Architecture

## System Boundary
Describe frontend, backend, database, integrations and external services.

## Allowed Extension Points
- 

## Protected Decisions
- 

## ADRs
- ADR-001 (proposed 2026-10-09, developer-approved; **tech lead approval pending**): User Management demo stores users in process memory (`ess_app.users.store`, a lock-protected dict). No database, driver, ORM or new dependency. Data is lost on restart; single process only. The UI (phase 3) is static HTML/JS served by the same FastAPI app. No authentication; local demo only.

## Architecture Change Rule
AI may propose architecture changes, but must not implement material architecture, database, authentication or infrastructure changes without explicit approval.
