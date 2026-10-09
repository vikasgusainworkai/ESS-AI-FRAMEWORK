---
description: Run the ESS guardrail check on this branch and explain the result
---

Run `python tools/ess_guard.py check` and show the full output. For every FAIL line, explain in plain words what rule it enforces and propose the smallest compliant fix. Do not change protected files (`.ess-ai/guardrails.json` lists them) and do not try to work around a guardrail; if the change really needs one of them, say that it needs the tech lead's approval. Additional input: $ARGUMENTS
