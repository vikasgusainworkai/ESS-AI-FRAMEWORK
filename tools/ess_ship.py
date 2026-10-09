#!/usr/bin/env python3
"""ESS ship: commit and push an approved change in one guarded step.

  python tools/ess_ship.py --ticket ESS-123 --title "Short summary" [--type fix]
        [--files path ...] [--body "why / what"]

Claude Code runs this only after the developer approves it: `.claude/settings.json` puts it
on the "ask" list, so a permission prompt appears every time, while plain `git commit` and
`git push` are denied. That prompt is the review gate. When it is approved, this script:

  1. checks the change: protected files, dependencies, secrets, architecture and the
     Definition of Tested (tools/ess_guard.py), then runs the tests; any FAIL stops here
  2. creates the branch <type>/<ticket>-<slug> when you are on the base branch
  3. stages only the changed files (never `git add -A`) and commits with an ESS message
  4. pushes the branch to the remote (never the base branch, never force)
  5. opens a pull request with the GitHub CLI when it is installed (open_pr in automation.json)
  6. runs the optional after_ship command (for example a ticket update) from automation.json

Configuration: .ess-ai/automation.json. Standard library only.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ess_guard  # noqa: E402

ROOT = ess_guard.ROOT
CONFIG_FILE = ROOT / ".ess-ai" / "automation.json"
LOG = ".ess-ai/reports/guardrail-log.md"
DEFAULTS: dict[str, Any] = {
    "remote": "origin",
    "branch_types": ["fix", "feat", "chore", "refactor", "test", "docs"],
    "open_pr": "auto",
    "after_ship": [],
}


def load_config() -> dict[str, Any]:
    cfg = dict(DEFAULTS)
    try:
        cfg.update(json.loads(CONFIG_FILE.read_text(encoding="utf-8")))
    except (OSError, ValueError):
        pass
    return cfg


def git(*args: str, input_text: str | None = None) -> tuple[int, str]:
    p = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        input=input_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return p.returncode, (p.stdout + p.stderr).strip()


def out(msg: str = "") -> None:
    print(msg, flush=True)


def stop(msg: str) -> int:
    out(f"\nSTOPPED: {msg}")
    out("Nothing was committed or pushed.")
    return 1


def slug(text: str, words: int = 5) -> str:
    parts = re.findall(r"[a-z0-9]+", text.lower())
    return "-".join(parts[:words]) or "change"


def changed_files() -> list[str]:
    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout
    files: list[str] = []
    for line in status.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].split(" -> ")[-1].strip().strip('"')
        if path and path != LOG:
            files.append(path)
    return sorted(set(files))


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    except (AttributeError, ValueError):
        pass
    cfg = load_config()
    ap = argparse.ArgumentParser(prog="ess_ship.py", description=__doc__.splitlines()[0])
    ap.add_argument("--ticket", required=True, help="ticket / work item id, e.g. ESS-123")
    ap.add_argument("--title", required=True, help="one-line summary for the commit")
    ap.add_argument("--type", default="fix", choices=cfg["branch_types"], help="branch type")
    ap.add_argument("--body", default="", help="why and what changed (commit body)")
    ap.add_argument("--files", nargs="*", help="files to commit (default: every changed file)")
    args = ap.parse_args()
    ticket = args.ticket.strip().upper()
    if not re.fullmatch(r"[A-Z][A-Z0-9_]*-\d+", ticket):
        return stop(f"'{args.ticket}' does not look like a ticket id (for example ESS-123).")

    if shutil.which("git") is None:
        return stop("git is not installed or not on PATH.")
    if git("rev-parse", "--is-inside-work-tree")[0] != 0:
        return stop("this folder is not a git repository. Run `git init` first.")
    base = str(ess_guard.CFG["base_branch"])
    _, branch = git("rev-parse", "--abbrev-ref", "HEAD")

    detected = changed_files()
    files = [ess_guard.norm(f) for f in args.files] if args.files else detected
    files = [f for f in files if f != LOG]
    if not files:
        return stop("there are no changes to commit.")
    missing = [f for f in files if f not in detected]
    if missing:
        return stop(f"these files have no changes: {', '.join(missing)}")

    out("=" * 72)
    out(f"ESS SHIP  {ticket}: {args.title}")
    out("=" * 72)
    out("Files in this commit:")
    for f in files:
        out(f"  - {f}")

    # 1. the gate: same rules as the guardrail check, then the tests
    problems: list[str] = []
    for f in files:
        reason = ess_guard.check_path(f)
        if reason:
            problems.append(reason)
        path = ROOT / f
        if path.is_file():
            problems += ess_guard.check_code(f, path.read_text(encoding="utf-8", errors="replace"))
    code = [f for f in files if ess_guard.is_code(f)]
    if code and not any(ess_guard.is_test(f) for f in files):
        problems.append(
            f"Definition of Tested: code changed ({', '.join(code)}) but no test was added "
            "or changed. Add a regression test first."
        )
    out("\n[1/5] ESS guardrail check")
    if problems:
        for p in problems:
            out(f"  FAIL  {p}")
        return stop(f"{len(problems)} guardrail problem(s). Fix them, then ship again.")
    out("  PASS  protected files, dependencies, secrets, architecture, Definition of Tested")
    passed, summary = ess_guard.run_tests()
    out(f"  {'PASS' if passed else 'FAIL'}  tests: {summary}")
    if not passed:
        return stop("the tests are failing. Only a green change can be shipped.")

    _, who = git("config", "user.name")
    if not who:
        return stop('git has no user.name. Run: git config user.name "Your Name"')

    # 2. branch
    out("\n[2/5] Branch")
    created = ""
    if branch in (base, "master", "HEAD"):
        new = f"{args.type}/{ticket}-{slug(args.title)}"
        code_, msg = git("checkout", "-B", new)
        if code_ != 0:
            return stop(f"could not create branch {new}: {msg}")
        created = branch
        branch = new
        out(f"  created {branch} from {base}")
    else:
        out(f"  using the current branch {branch}")

    # 3. commit (only the listed files)
    out("\n[3/5] Commit")
    code_, msg = git("add", "--", *files)
    if code_ != 0:
        if created:
            git("checkout", "-q", created)
            git("branch", "-D", branch)
        return stop(f"git add failed: {msg}")
    body = args.body.strip()
    message = (
        f"{ticket}: {args.title.strip()}\n\n"
        + (f"{body}\n\n" if body else "")
        + f"Tests: {summary}\n"
        + "ESS-Check: PASS (guardrails, Definition of Tested)\n"
        + f"AI-Assisted: Claude Code; reviewed and approved by {who}\n"
    )
    code_, msg = git("commit", "-F", "-", "--", *files, input_text=message)
    if code_ != 0:
        git("reset", "-q", "--", *files)
        if created:  # back to where we started, changes kept
            git("checkout", "-q", created)
            git("branch", "-D", branch)
        return stop(f"git commit failed (a pre-commit hook may have changed files):\n{msg}")
    _, sha = git("rev-parse", "--short", "HEAD")
    out(f"  {sha}  {ticket}: {args.title.strip()}")

    # 4. push (branch only, never force)
    out("\n[4/5] Push")
    remote = str(cfg["remote"])
    pushed = False
    remote_url = ""
    if git("remote", "get-url", remote)[0] != 0:
        out(f"  skipped: there is no '{remote}' remote. The commit is on {branch} locally.")
    else:
        _, remote_url = git("remote", "get-url", remote)
        code_, msg = git("push", "-u", remote, f"{branch}:{branch}")
        if code_ != 0:
            out(f"  push FAILED:\n{msg}")
            out(
                f"  The commit is safe on {branch}. Fix the problem, then: git push -u {remote} {branch}"
            )
            return 1
        pushed = True
        out(f"  pushed {branch} -> {remote} ({remote_url})")

    # 5. pull request (optional)
    out("\n[5/5] Pull request")
    pr_url = ""
    want_pr = str(cfg.get("open_pr", "auto")).lower()
    if not pushed:
        out("  skipped: nothing was pushed")
    elif want_pr in ("false", "no", "off", "never"):
        out("  skipped: open_pr is off in .ess-ai/automation.json")
    elif "github.com" not in remote_url or shutil.which("gh") is None:
        out(
            "  skipped: needs a GitHub remote and the GitHub CLI (gh). Open the PR in your browser."
        )
    else:
        p = subprocess.run(
            ["gh", "pr", "create", "--base", base, "--head", branch, "--fill"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        found = re.findall(r"https://\S+", p.stdout + p.stderr)
        pr_url = found[-1] if found else ""
        out(f"  {pr_url or 'gh could not open the PR: ' + (p.stderr.strip() or p.stdout.strip())}")

    # evidence for the ticket update
    paths = [f for f in files if ess_guard.is_code(f) or ess_guard.is_test(f)] or files
    _, diff = git("show", "--format=", "--unified=3", "HEAD", "--", *paths)
    evidence = {
        "ticket": ticket,
        "title": args.title.strip(),
        "branch": branch,
        "commit": sha,
        "files": files,
        "tests": summary,
        "pushed": pushed,
        "remote": remote_url,
        "pr": pr_url,
        "approved_by": who,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "diff": diff,
    }
    after = [str(x) for x in cfg.get("after_ship") or []]
    if after:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
            json.dump(evidence, fh, indent=2)
        values = {"ticket": ticket, "branch": branch, "commit": sha, "evidence": fh.name}
        cmd = [sys.executable if x == "python" else x.format(**values) for x in after]
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        note = (p.stdout + p.stderr).strip()
        out(
            f"\nAfter ship: {note or 'done'}"
            if p.returncode == 0
            else f"\nAfter ship FAILED: {note}"
        )
        Path(fh.name).unlink(missing_ok=True)

    out("\n" + "=" * 72)
    out(f"SHIPPED  {ticket}  branch {branch}  commit {sha}  ({summary})")
    out("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
