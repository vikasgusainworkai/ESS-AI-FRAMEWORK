# Gemini / Antigravity — ESS project

Follow the ESS AI engineering instructions in `AGENTS.md` at the repository root. They require reading `.ess-ai/rules/` and `.ess-ai/context/` before any change, planning before coding, waiting for developer approval, small reviewable phases, evidence-based test results, and never exposing secrets or requesting unrestricted production access.

Before every commit run `python tools/ess_guard.py check` and fix every FAIL. Protected files are listed in `.ess-ai/guardrails.json`; never change them or work around a guardrail.
