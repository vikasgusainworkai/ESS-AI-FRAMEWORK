# API Contracts

Document approved endpoints, request/response schemas, authentication, authorization, errors and compatibility requirements.

AI must not silently change an existing contract.

## Existing
- `GET /health` → 200 `{"status": "ok", "environment": "<env>"}`
- Any unhandled error → 500 `{"error": "internal_error"}`

## Users API (demo, no authentication)
User: `{"id": "<uuid>", "name": str, "email": str, "role": "admin|manager|user", "status": "active|inactive"}`

| Method | Path | Body | Success |
|---|---|---|---|
| POST | `/api/users` | `{name, email, role, status?}` | 201 User |
| GET | `/api/users?q=&role=&status=` | – | 200 `[User]` (`q` matches name or email, case-insensitive) |
| GET | `/api/users/{id}` | – | 200 User |
| PATCH | `/api/users/{id}` | any of `{name, email, role, status}` | 200 User |
| POST | `/api/users/{id}/deactivate` | – | 200 User (status `inactive`) |
| DELETE | `/api/users/{id}` | – | 204 |

Unknown fields in a body are rejected. `null` is not accepted for a field in PATCH.

## Errors
- 404 `{"error": "user_not_found", "message": "..."}`
- 409 `{"error": "email_already_exists", "message": "..."}`
- 422 `{"error": "validation_error", "details": [{"field": "email", "message": "..."}]}` — submitted values are not echoed back.
