# Guardrails Rule
The ESS rules are enforced by `python tools/ess_guard.py` with the settings in `.ess-ai/guardrails.json`. In Claude Code it runs as hooks on every prompt, edit and command; in CI and before commit it runs as `python tools/ess_guard.py check`.
- Treat every guardrail denial as a stop. Explain it to the developer and propose a compliant alternative; never work around it (other file names, other tools, encoded commands).
- Protected paths, dependency files, blocked imports and the SQL rule change only through the tech lead, in a reviewed PR with an ADR in `context/architecture.md`.
- A change to code folders needs a test change (Definition of Tested). The branch check must say `RESULT: PASS` before a commit or PR.
- Every decision is logged in `reports/guardrail-log.md` as evidence.
