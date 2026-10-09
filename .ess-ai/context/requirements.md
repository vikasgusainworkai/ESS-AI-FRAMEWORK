# Requirements

## Requirement
Minimal User Management demo on the existing ESS FastAPI starter: create, list, search, retrieve, edit, deactivate and delete users, with in-memory storage, a browser UI and automated tests. Local demo only.

Approved by the developer on 2026-10-09 (defaults proposed in the plan were accepted).

## Acceptance Criteria
- Users can be created, listed, searched (name/email text, role, status), retrieved, edited, deactivated and deleted through the API.
- Name, email, role and status are validated; invalid input returns 422 with one message per field.
- Duplicate emails are rejected with 409, case-insensitively and ignoring surrounding spaces.
- Unknown user ids return 404.
- Errors never expose internals.
- Browser UI: user table, search, create/edit form, deactivate and delete actions, readable error messages (phase 3, not started).

## Out of Scope
- Database or any persistent storage; new dependencies.
- Authentication, authorization, multi-tenancy.
- Production deployment.

## Business Rules
- Roles: `admin`, `manager`, `user`.
- Statuses: `active`, `inactive`. New users default to `active`. Deactivate sets `inactive`; edit may set status back to `active`.
- Delete is a hard delete (record removed from memory), separate from deactivate.
- Name: trimmed, 1–100 characters.
- Email: trimmed, stored lowercase, max 254 characters, must look like `local@domain.tld` (no spaces). Unique across all users.

## Affected Users / Tenants
- Local demo users only. No tenants.

## Evidence / References
- Developer approval in the Claude Code session, 2026-10-09.
