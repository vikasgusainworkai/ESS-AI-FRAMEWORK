#!/usr/bin/env python3
"""ESS line counter: code lines now versus the last commit, for /ess-slim.

  python tools/ess_loc.py                 every code folder in .ess-ai/guardrails.json
  python tools/ess_loc.py src/ess_app     only these files or folders
        [--base HEAD]                     compare with another git ref (default HEAD)

Counts lines that are not blank and not comment-only. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODE_EXT = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}


def count(text: str, suffix: str) -> int:
    marks = ("#",) if suffix == ".py" else ("//", "/*", "*")
    return sum(1 for ln in text.splitlines() if ln.strip() and not ln.strip().startswith(marks))


def git(*args: str) -> tuple[int, str]:
    p = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    return p.returncode, p.stdout


def files_now(scope: list[str]) -> set[str]:
    out: set[str] = set()
    for s in scope:
        p = ROOT / s
        found = [p] if p.is_file() else p.rglob("*") if p.is_dir() else []
        out |= {
            f.relative_to(ROOT).as_posix() for f in found if f.is_file() and f.suffix in CODE_EXT
        }
    return out


def main() -> int:
    ap = argparse.ArgumentParser(prog="ess_loc.py", description="ESS line counter")
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--base", default="HEAD", help="git ref to compare with")
    args = ap.parse_args()
    try:
        cfg = json.loads((ROOT / ".ess-ai" / "guardrails.json").read_text(encoding="utf-8"))
        default = [d for d in cfg.get("code_dirs", ["src/"]) if (ROOT / d).exists()]
    except (OSError, ValueError):
        default = ["src/"]
    scope = [p.replace("\\", "/").rstrip("/") for p in (args.paths or default)]

    has_git = git("rev-parse", "--verify", args.base)[0] == 0
    then: dict[str, int] = {}
    if has_git:
        _, listed = git("ls-tree", "-r", "--name-only", args.base, "--", *scope)
        for f in listed.splitlines():
            if Path(f).suffix in CODE_EXT:
                then[f] = count(git("show", f"{args.base}:./{f}")[1], Path(f).suffix)
    now = {
        f: count((ROOT / f).read_text(encoding="utf-8", errors="replace"), Path(f).suffix)
        for f in files_now(scope)
    }

    rows = sorted(set(then) | set(now), key=lambda f: now.get(f, 0) - then.get(f, 0))
    print(
        f"ESS line count ({', '.join(scope)}), code lines {'at ' + args.base + ' -> now' if has_git else 'now'}"
    )
    for f in rows:
        b, a = then.get(f, 0), now.get(f, 0)
        if has_git:
            print(f"  {b:6} -> {a:6}  {a - b:+6}  {f}")
        else:
            print(f"  {a:6}  {f}")
    b, a = sum(then.values()), sum(now.values())
    if has_git:
        pct = f" ({(a - b) / b:+.0%})" if b else ""
        print(f"  TOTAL {b} -> {a}  {a - b:+d}{pct}")
    else:
        print(f"  TOTAL {a} (not a git repository, nothing to compare with)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
