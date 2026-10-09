# AI Project Progress

## Current State
- User Management demo: Users API, tests and browser UI done; ready for local demo. Not committed (no git repo).

## Completed
- 2026-10-09 Phase 0: requirements, API contract, security notes and ADR-001 draft recorded in `.ess-ai/context/`.
- 2026-10-09 Phases 1–2: `src/ess_app/users/` (models, store, router) mounted in `main.py` with 404/409/422 handlers; tests in `tests/test_users_store.py`, `tests/test_users_api.py`, `tests/conftest.py`. 48 tests pass, 100% coverage; ruff, format, mypy and pip-audit clean (.venv, Python 3.14.7).
- 2026-10-09 Phase 3: browser UI `src/ess_app/static/users.html` (plain HTML/JS, no CDN, user values via textContent) served at `GET /`; `tests/test_ui.py`. 51 tests pass, 100% coverage; ruff, format, mypy clean; uvicorn smoke test on 127.0.0.1 passed; page JS passes `node --check`. UI interactions verified manually only (no browser E2E tool approved).

## Decisions
- Roles `admin|manager|user`; statuses `active|inactive` (default `active`, reactivation via PATCH allowed); hard delete separate from deactivate; name 1–100 chars trimmed; email trimmed, lowercased, max 254, regex-checked (no `email-validator` dependency).
- 422 responses use `{"error": "validation_error", "details": [{field, message}]}` app-wide and do not echo input.

## Known Issues
- Not a git repository: `python tools/ess_guard.py check` cannot run and `ess_ship.py` cannot ship.
- ADR-001 needs tech lead approval.
- `.venv` is Python 3.14.7; project targets 3.12.
- Starlette deprecation warning for the httpx-based TestClient (pre-existing).
- `users.html` is not declared as package data, so `python -m build` would omit it; fixing needs a `pyproject.toml` change (dependency file, needs approval). Works from the source tree / editable install.
- `ess_guard.py check` exits 0 when it cannot run (protected file; tech lead to fix).

## Next Step
- Developer manual UI review; `git init` + initial `main` commit; security review and AI Change Report (Phase 4); then `/ess-ship`.
