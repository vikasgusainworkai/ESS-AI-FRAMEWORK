# Check Database Change Safety

_When to use:_ Before changing PostgreSQL / Oracle / other database structures.

```text
Review this proposed database change against the existing schema and application usage. Identify affected tables, queries, APIs, indexes, constraints, tenant boundaries, migration risks, rollback considerations and backward compatibility. Do not execute destructive changes. Provide a safe migration and validation plan first.
```
