# ESS Workflow — Legacy Modernization (PHP → React/Node, Oracle Forms → APEX)

Capture current behavior → Map screens, rules, data and integrations → Define behavior that must be preserved → Plan small slices → Build slice → Compare old vs new outputs on the same inputs → Regression + source-of-truth validation → User acceptance → Cutover / rollback plan

Rules:
- Use `prompts/dev/10-analyze-existing-code-first.md` before every slice.
- Record preserved behavior in `.ess-ai/context/requirements.md` as acceptance criteria.
- A slice is done only when old and new produce the same result for the agreed test inputs, or the difference is approved.
