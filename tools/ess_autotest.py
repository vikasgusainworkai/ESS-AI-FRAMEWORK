#!/usr/bin/env python3
"""ESS auto-test: run the tests after every AI edit to code or tests.

Claude Code PostToolUse hook (.claude/settings.json). After Claude writes or edits a file in a
code or test folder (code_dirs / test_dirs in .ess-ai/guardrails.json), the test suite runs and:
  * you see a one-line result in the Claude Code chat ("ESS auto-test: 9 passed")
  * Claude gets the failing test names and messages as feedback, so a red run is fixed
    from evidence instead of guesses

Command: autotest_command in .ess-ai/automation.json, else the project test command.
It never blocks the session: any error here is reported and ignored.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ess_guard  # noqa: E402

ROOT = ess_guard.ROOT


def autotest_command() -> list[str] | str:
    try:
        cfg = json.loads((ROOT / ".ess-ai" / "automation.json").read_text(encoding="utf-8"))
        cmd = str(cfg.get("autotest_command") or "")
    except (OSError, ValueError):
        cmd = ""
    return cmd or ess_guard.test_command()


def run() -> tuple[bool, str, str]:
    cmd = autotest_command()
    p = subprocess.run(
        cmd,
        cwd=ROOT,
        shell=isinstance(cmd, str),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=110,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8"},
    )
    text = (p.stdout + "\n" + p.stderr).strip()
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    ran = re.search(r"Ran (\d+) tests?", text)
    hits = [
        ln for ln in lines if re.search(r"\b(\d+ (passed|failed)|Tests?\s+\d+|FAILED \(|^OK\b)", ln)
    ]
    if ran:  # unittest
        n = ran.group(1)
        bad = re.search(r"FAILED \((.*?)\)", text)
        summary = (
            f"{n} passed"
            if p.returncode == 0
            else f"{n} run, FAILED ({bad.group(1) if bad else 'errors'})"
        )
    else:  # pytest / vitest / anything else
        summary = (hits or lines or ["no output"])[-1]
    failures = [
        ln for ln in lines if re.match(r"^(FAIL|ERROR|FAILED)\b|^(\w+Error|AssertionError|E\s)", ln)
    ][:25]
    return p.returncode == 0, summary, "\n".join(failures)


def main() -> int:
    try:
        data: dict[str, Any] = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        return 0
    ti = data.get("tool_input") or {}
    raw = str(ti.get("file_path") or ti.get("notebook_path") or "")
    try:
        rel = Path(raw).resolve().relative_to(ROOT).as_posix()
    except (ValueError, OSError):
        rel = ess_guard.norm(raw)
    if not (ess_guard.is_code(rel) or ess_guard.is_test(rel)):
        return 0
    try:
        ok, summary, failures = run()
    except (OSError, subprocess.SubprocessError) as exc:
        print(json.dumps({"systemMessage": f"ESS auto-test could not run: {exc}"}))
        return 0
    if ok:
        msg = f"ESS auto-test after editing {rel}: GREEN, {summary}"
        context = f"ESS auto-test ran the whole suite after this edit: GREEN ({summary})."
    else:
        msg = f"ESS auto-test after editing {rel}: RED, {summary}"
        context = (
            f"ESS auto-test ran the whole suite after this edit: RED ({summary}).\n{failures}\n"
            "If this is the new regression test before the fix, red is expected. Otherwise fix "
            "the cause from this evidence; never weaken or delete a test to make it pass."
        )
    print(
        json.dumps(
            {
                "systemMessage": msg,
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": context,
                },
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
