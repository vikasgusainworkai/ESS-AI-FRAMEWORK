#!/usr/bin/env python3
"""ESS guardrails: the starter kit rules turned into checks a machine enforces.

  python tools/ess_guard.py prompt    Claude Code UserPromptSubmit hook: blocks or flags prompts
  python tools/ess_guard.py tool      Claude Code PreToolUse hook: denies risky edits and commands
  python tools/ess_guard.py check     Branch check against main, for any AI tool (also runs in CI)
        [--base origin/main] [--no-tests]

Configuration: .ess-ai/guardrails.json (protected files, code and test folders, blocked imports).
Every hook decision is appended to .ess-ai/reports/guardrail-log.md.
Standard library only, so it runs before the project is installed.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT / ".ess-ai" / "guardrails.json"
LOG_FILE = ROOT / ".ess-ai" / "reports" / "guardrail-log.md"

DEFAULTS: dict[str, Any] = {
    "base_branch": "main",
    "protected_paths": [".ess-ai/rules/", ".ess-ai/guardrails.json", ".claude/settings.json"],
    "dependency_files": ["pyproject.toml", "requirements.txt", "package.json"],
    "code_dirs": ["src/", "app/", "lib/"],
    "test_dirs": ["tests/", "test/"],
    "blocked_imports": ["sqlite3", "sqlalchemy", "psycopg2", "pymongo", "redis"],
    "allow_sql_in_code": False,
    "test_command": "",
}


def load_config() -> dict[str, Any]:
    cfg = dict(DEFAULTS)
    try:
        cfg.update(json.loads(CONFIG_FILE.read_text(encoding="utf-8")))
    except (OSError, ValueError):
        pass
    return cfg


CFG = load_config()

# --------------------------------------------------------------------------- prompts
PROMPT_BLOCK = [
    (
        r"\b(prod|production|live)\b.{0,40}\b(db|database|data|server|customer)",
        "It asks for production / live data access. ESS rule: AI never gets unrestricted "
        "production or database access. Use local test data instead.",
    ),
    (
        r"\b(drop|truncate)\b.{0,25}\b(tables?|database|db|schema)\b"
        r"|\bdelete\s+(all|every)\b.{0,30}\b(user|record|row|employee|customer)",
        "It asks for a destructive data operation. ESS rule: no destructive data changes from AI.",
    ),
    (
        r"\b(skip|disable|remove|turn off|bypass|ignore)\b.{0,20}"
        r"\b(tests?|ci|checks?|hooks?|guard\w*|security|review|approval)\b",
        "It asks to skip or disable a quality gate. ESS rule: never bypass tests, hooks, CI "
        "or developer approval.",
    ),
    (
        r"--no-verify|\bforce[- ]push\b|\bpush\b.{0,25}\bto\s+(main|master)\b"
        r"|\bcommit\b.{0,25}\bto\s+(main|master)\b",
        "It asks to push or commit straight to main or to force-push. ESS rule: every change "
        "goes on a branch and through a PR.",
    ),
    (
        r"\b(commit|hard[- ]?code|paste|put|store)\b.{0,30}"
        r"\b(api[ _-]?key|password|secret|token|credential)s?\b",
        "It asks to put a secret into the code. ESS rule: secrets live in environment "
        "variables only, never in files or commits.",
    ),
]

PROMPT_WARN = [
    (
        r"\b(add|use|introduce|switch to|migrate to|connect( it)? to|move to|replace)\b.{0,40}"
        r"\b(database|db|sql\w*|sqlite|postgres\w*|mysql|oracle|mongo\w*|orm|sqlalchemy|redis|"
        r"prisma|flask|django|fastapi|express|next\.?js|react|angular|vue|microservices?|kafka|"
        r"docker|kubernetes|graphql|auth\w*|login|sso|oauth|jwt)\b",
        "ARCHITECTURE CHANGE",
        "This prompt asks for an architecture change (database, framework, authentication or "
        "infrastructure). Check it against .ess-ai/context/architecture.md. Do NOT change any "
        "file. Reply with: (1) which approved or protected decision it changes, (2) impact on "
        "files, API contracts, data and security, (3) risks and UNKNOWNs, (4) the options, and "
        "ask the developer for explicit approval and an ADR before any code.",
    ),
    (
        r"\b(build|create|write|generate|make)\b.{0,15}\b(the\s+)?(entire|whole|complete|full)\b"
        r".{0,20}\b(app|application|system|project|module)"
        r"|\bfix\s+(everything|all\s+(the\s+)?bugs)\b|\bjust\s+(do|fix|build)\s+it\b"
        r"|\bdo\s+whatever\b",
        "VAGUE / TOO BIG",
        "This prompt is too broad for the ESS workflow. Do NOT write code. Restate the goal, "
        "list what is missing (acceptance criteria, scope, affected modules), ask the 3 most "
        "important questions and propose small phases. Start with "
        ".ess-ai/prompts/02-requirement.md.",
    ),
    (
        r"\b(pip|npm|yarn|pnpm|poetry|uv)\s+(install|add)\b"
        r"|\b(new|another|third[- ]party)\s+(library|package|dependency)\b",
        "NEW DEPENDENCY",
        "This prompt adds a dependency. ESS rule 07: new packages need necessity, security, "
        "license and architecture review. Do not install anything. Explain why it is needed and "
        "the alternatives, and ask the developer for approval.",
    ),
]


def check_prompt(prompt: str) -> tuple[str, ...] | None:
    for pattern, reason in PROMPT_BLOCK:
        if re.search(pattern, prompt, re.I):
            return ("block", reason)
    for pattern, label, instruction in PROMPT_WARN:
        if re.search(pattern, prompt, re.I):
            return ("warn", label, instruction)
    return None


# --------------------------------------------------------------------------- files and code
SECRET_FILES = re.compile(
    r"(^|/)(\.env(\.(?!example$).*)?|.*\.pem|.*\.key|id_rsa.*|credentials\.json)$", re.I
)
SECRET_PATTERNS = [
    r"sk-ant-[A-Za-z0-9_\-]{10,}",
    r"AKIA[0-9A-Z]{16}",
    r"gh[pousr]_[A-Za-z0-9]{20,}",
    r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----",
    r"""(?i)\b\w*(password|passwd|secret|api_?key|token)\w*['"]?\s*[:=]\s*['"][^'"\s]{6,}['"]""",
]
SQL_PATTERN = (
    r"(?i)\b(drop\s+(table|database)|truncate\s+table|delete\s+from|alter\s+table"
    r"|insert\s+into|update\s+\w+\s+set|select\s+[\w*,\s]+\s+from)\b"
)
PY_IMPORT = re.compile(r"^\s*(?:from\s+([\w.]+)\s+import|import\s+([\w., ]+))", re.M)
JS_IMPORT = re.compile(
    r"""(?:\bimport\s+(?:[\w*{}\s,]+\s+from\s+)?|\bexport\s+[\w*{}\s,]+\s+from\s+"""
    r"""|\brequire\(\s*|\bimport\(\s*)['"]([^'"]+)['"]"""
)
CODE_EXT = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}
TEXT_EXT = CODE_EXT | {".md", ".json", ".toml", ".yml", ".yaml", ".txt", ".html", ".cfg", ".ini"}


def norm(path: str) -> str:
    path = path.replace("\\", "/")
    while path.startswith("./"):
        path = path[2:]
    return path


def in_dirs(rel: str, dirs: list[str]) -> bool:
    return any(rel.startswith(d) or f"/{d}" in f"/{rel}" for d in dirs)


def is_test(rel: str) -> bool:
    name = rel.rsplit("/", 1)[-1]
    return (
        in_dirs(rel, CFG["test_dirs"])
        or "/__tests__/" in f"/{rel}"
        or re.match(r"(test_.*\.py|.*_test\.py|.*\.(test|spec)\.[cm]?[jt]sx?)$", name) is not None
    )


def is_code(rel: str) -> bool:
    return Path(rel).suffix in CODE_EXT and in_dirs(rel, CFG["code_dirs"]) and not is_test(rel)


def check_path(rel: str) -> str | None:
    rel = norm(rel)
    low = rel.lower()
    for p in CFG["protected_paths"]:
        pl = p.lower()
        if low == pl.rstrip("/") or low.startswith(pl):
            return f"'{rel}' is protected by the ESS guardrails ({p}). Changing it needs the tech lead's approval."
    if rel.rsplit("/", 1)[-1] in CFG["dependency_files"]:
        return f"'{rel}' changes dependencies. ESS rule 07: new packages need review and developer approval first."
    if SECRET_FILES.search(rel):
        return (
            f"'{rel}' is a secrets file. Secrets stay in environment variables, never in the repo."
        )
    return None


def _declared_python() -> set[str]:
    names: set[str] = set()
    for f in ("pyproject.toml", "requirements.txt", "requirements-dev.txt"):
        try:
            text = (ROOT / f).read_text(encoding="utf-8")
        except OSError:
            continue
        for m in re.finditer(
            r"""^\s*["']?([A-Za-z0-9][A-Za-z0-9_.\-]*)\s*(?:\[[^\]]*\])?\s*[<>=~!;"',]""",
            text,
            re.M,
        ):
            names.add(m.group(1).lower().replace("-", "_").replace(".", "_"))
        for m in re.finditer(r"^\s*([A-Za-z0-9][A-Za-z0-9_.\-]*)\s*$", text, re.M):
            names.add(m.group(1).lower().replace("-", "_"))
    return names


def _local_python(rel: str) -> set[str]:
    names = {p.stem for p in ROOT.glob("*.py")} | {p.name for p in ROOT.iterdir() if p.is_dir()}
    for base in ("src", str(Path(rel).parent)):
        d = ROOT / base
        if d.is_dir():
            names |= {p.stem for p in d.glob("*.py")} | {p.name for p in d.iterdir() if p.is_dir()}
    return {n.lower() for n in names}


def _declared_js() -> set[str]:
    try:
        pkg = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    names: set[str] = set()
    for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        names |= set(pkg.get(key, {}))
    return names


def check_code(rel: str, text: str) -> list[str]:
    rel = norm(rel)
    problems: list[str] = []
    if Path(rel).suffix in TEXT_EXT and not rel.endswith(".env.example"):
        for pat in SECRET_PATTERNS:
            if re.search(pat, text):
                problems.append(
                    f"{rel}: looks like a hard-coded secret. Use an environment variable."
                )
                break
    if not is_code(rel):
        return problems
    blocked = {b.lower() for b in CFG["blocked_imports"]}
    found: set[str] = set()
    if rel.endswith(".py"):
        stdlib = set(getattr(sys, "stdlib_module_names", ()))
        declared, local = _declared_python(), _local_python(rel)
        for m in PY_IMPORT.finditer(text):
            mods = (
                [m.group(1)]
                if m.group(1)
                else [x.strip().split(" ")[0] for x in m.group(2).split(",")]
            )
            for mod in mods:
                top = mod.split(".")[0].lower()
                if not top or top in found or top == "__future__":
                    continue
                found.add(top)
                if top in blocked:
                    problems.append(
                        f"{rel}: imports '{top}', a database driver. That is an architecture change: "
                        "it needs an ADR in .ess-ai/context/architecture.md and the tech lead's approval."
                    )
                elif stdlib and top not in stdlib and top not in local and top not in declared:
                    problems.append(
                        f"{rel}: imports '{top}', a third-party package the project does not declare. "
                        "New dependencies need approval (ESS rule 07)."
                    )
    else:
        declared_js = _declared_js()
        for m in JS_IMPORT.finditer(text):
            spec = m.group(1)
            if spec.startswith((".", "/", "@/", "~/", "node:", "virtual:")) or spec in found:
                continue
            parts = spec.split("/")
            pkg = "/".join(parts[:2]) if spec.startswith("@") else parts[0]
            found.add(spec)
            if pkg.lower() in blocked:
                problems.append(
                    f"{rel}: imports '{pkg}', a database client. That is an architecture change: "
                    "it needs an ADR in .ess-ai/context/architecture.md and the tech lead's approval."
                )
            elif declared_js and pkg not in declared_js:
                problems.append(
                    f"{rel}: imports '{pkg}', a package not in package.json. "
                    "New dependencies need approval (ESS rule 07)."
                )
    if not CFG["allow_sql_in_code"] and re.search(SQL_PATTERN, text):
        problems.append(
            f"{rel}: contains SQL. Architecture does not allow SQL in application code "
            "(allow_sql_in_code in .ess-ai/guardrails.json)."
        )
    return problems


def check_command(cmd: str) -> str | None:
    c = " ".join(cmd.split())
    if (
        re.search(
            r"(?i)(^|[\s;&|(])(sqlite3|psql|mysql|mongosh|mongo|sqlcmd|sqlplus|redis-cli)(\s|$)", c
        )
        or re.search(SQL_PATTERN, c)
        or re.search(r"(?i)\bimport\s+sqlite3\b", c)
    ):
        return "Direct database access. ESS rule: AI does not query or change databases directly."
    if re.search(
        r"(?i)\b(pip3?|npm|yarn|pnpm|poetry|uv)\s+(install|add|i)\s+\S", c
    ) and not re.search(
        r"(?i)\b(pip3?|uv pip)\s+install\s+(-e\s+)?['\"]?\.(\[[\w,]+\])?['\"]?(\s|$)", c
    ):
        return "Installing a new package. ESS rule 07: new dependencies need developer approval."
    if re.search(r"(?i)-m\s+pip\s+install\s+(?!(-e\s+)?['\"]?\.)", c):
        return "Installing a new package. ESS rule 07: new dependencies need developer approval."
    if re.search(r"\bgit\s+push\b", c) and (
        re.search(r"(\s|:)(main|master)(\s|$)", c)
        or re.search(r"\s(-f|--force)(\s|$)|--force-with-lease", c)
    ):
        return (
            "Pushing to main/master or force-pushing. ESS rule: push only your branch, never force."
        )
    if re.search(r"\bgit\s+commit\b.*(--no-verify|\s-n(\s|$))", c):
        return "Committing with --no-verify skips the hooks. ESS rule: never bypass hooks or CI."
    if re.search(r"\bgit\s+add\s+(-A|--all|\.)(\s|$)", c):
        return "'git add -A' / 'git add .' stages everything. Stage only the files you changed."
    if re.search(r"\bgit\s+(reset\s+--hard|clean\s+-[a-z]*f|checkout\s+--\s+\.)", c) or re.search(
        r"\brm\s+-[a-z]*r[a-z]*f?\s+(/|\*|\.)|Remove-Item\b.*-Recurse", c
    ):
        return "Destructive command that can delete work. Ask the developer to run it."
    if re.search(r"(?i)(cat|type|more|less|get-content|head|tail)\s+\S*\.env\b(?!\.example)", c):
        return "Reading a secrets file (.env). ESS rule: AI never reads or exposes secrets."
    return None


# --------------------------------------------------------------------------- hooks
def log(kind: str, decision: str, detail: str, reason: str) -> None:
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        new = not LOG_FILE.exists()
        with LOG_FILE.open("a", encoding="utf-8") as fh:
            if new:
                fh.write(
                    "# ESS guardrail log\n\n| Time | Check | Decision | What | Why |\n|---|---|---|---|---|\n"
                )

            def clean(s: str) -> str:
                return str(s).replace("|", "/").replace("\n", " ")[:160]

            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fh.write(f"| {now} | {kind} | {decision} | {clean(detail)} | {clean(reason)} |\n")
    except OSError:
        pass


def emit(obj: dict[str, Any]) -> None:
    print(json.dumps(obj))
    sys.exit(0)


def on_prompt(data: dict[str, Any]) -> None:
    prompt = str(data.get("prompt", ""))
    result = check_prompt(prompt)
    if not result:
        return
    if result[0] == "block":
        log("prompt", "BLOCKED", prompt, result[1])
        emit(
            {
                "decision": "block",
                "reason": f"ESS guardrail blocked this prompt: {result[1]} "
                "Rephrase it within the ESS rules (see AGENTS.md).",
            }
        )
    _, label, instruction = result
    log("prompt", f"FLAGGED: {label}", prompt, instruction)
    emit(
        {
            "systemMessage": f"ESS guardrail: {label} - Claude will analyse and ask for approval instead of coding.",
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": f"ESS GUARDRAIL ({label}): {instruction}",
            },
        }
    )


def deny(kind: str, detail: str, reason: str) -> None:
    log(kind, "DENIED", detail, reason)
    emit(
        {
            "systemMessage": f"ESS guardrail denied: {reason}",
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"ESS guardrail: {reason} Explain this to the developer "
                "and propose an approved alternative. Never try to work around a guardrail.",
            },
        }
    )


def rel_path(p: str) -> str:
    try:
        return Path(p).resolve().relative_to(ROOT).as_posix()
    except (ValueError, OSError):
        return norm(p)


def on_tool(data: dict[str, Any]) -> None:
    tool = data.get("tool_name", "")
    ti = data.get("tool_input") or {}
    if tool in ("Bash", "PowerShell"):
        cmd = str(ti.get("command", ""))
        reason = check_command(cmd)
        if reason:
            deny("command", cmd, reason)
    elif tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        rel = rel_path(str(ti.get("file_path") or ti.get("notebook_path") or ""))
        reason = check_path(rel)
        if reason:
            deny("edit", rel, reason)
        if tool == "Write":
            text = ti.get("content", "")
        elif tool == "MultiEdit":
            text = "\n".join(e.get("new_string", "") for e in ti.get("edits", []))
        else:
            text = ti.get("new_string", "") or ti.get("new_source", "")
        problems = check_code(rel, str(text))
        if problems:
            deny("edit", rel, " ".join(problems))


# --------------------------------------------------------------------------- branch check
def git(*args: str) -> tuple[int, str]:
    p = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    return p.returncode, p.stdout.strip()


def changed_files(base: str) -> list[str] | None:
    code, mb = git("merge-base", base, "HEAD")
    if code != 0:
        return None
    _, tracked = git("diff", "--name-only", mb)
    _, untracked = git("ls-files", "--others", "--exclude-standard")
    files = {f for f in (tracked + "\n" + untracked).splitlines() if f.strip()}
    return sorted(f for f in files if f != ".ess-ai/reports/guardrail-log.md")


def test_command() -> list[str] | str:
    if CFG["test_command"]:
        return str(CFG["test_command"])
    if (ROOT / "package.json").exists():
        return "npm test --silent"
    try:
        import importlib.util

        has_pytest = importlib.util.find_spec("pytest") is not None
    except ImportError:
        has_pytest = False
    if has_pytest:
        return [sys.executable, "-m", "pytest", "-q"]
    return [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."]


def run_tests() -> tuple[bool, str]:
    cmd = test_command()
    p = subprocess.run(
        cmd,
        cwd=ROOT,
        shell=isinstance(cmd, str),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    out = [line for line in (p.stdout + p.stderr).strip().splitlines() if line.strip()]
    shown = cmd if isinstance(cmd, str) else " ".join(["python", *cmd[1:]])
    hits = [ln for ln in out if re.search(r"\b(passed|failed|ok|error|ran \d+ tests?)\b", ln, re.I)]
    summary = (hits or out or ["no output"])[-1].strip()
    ran = re.search(r"Ran (\d+) tests?", "\n".join(out))
    if ran:  # unittest prints just "OK"; say how many
        bad = re.search(r"FAILED \((.*?)\)", "\n".join(out))
        summary = (
            f"{ran.group(1)} passed"
            if p.returncode == 0
            else f"{ran.group(1)} run, FAILED ({bad.group(1) if bad else 'errors'})"
        )
    return p.returncode == 0, f"{shown} -> {summary}"


def branch_check(base: str, no_tests: bool) -> int:
    files = changed_files(base)
    if files is None:
        print(f"ESS check: cannot find base '{base}'. Run it on a branch of a git repository.")
        return 0
    failures: list[tuple[str, str]] = []
    notes: list[tuple[str, str]] = []
    for f in files:
        reason = check_path(f)
        if reason:
            failures.append(("Protected / dependency / secret file", reason))
        path = ROOT / f
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
            for problem in check_code(f, text):
                failures.append(("Architecture / security", problem))
    code_changed = [f for f in files if is_code(f)]
    if code_changed and not any(is_test(f) for f in files):
        failures.append(
            (
                "Definition of Tested",
                f"Code changed ({', '.join(code_changed)}) but no test was added or changed.",
            )
        )
    if not no_tests:
        ok, summary = run_tests()
        (notes if ok else failures).append(("Tests", summary))

    print("ESS guardrail check")
    print(f"  compared with: {base}   files changed: {len(files)}")
    for f in files:
        print(f"    - {f}")
    print()
    for title, text in notes:
        print(f"  PASS  {title}: {text}")
    for title, text in failures:
        print(f"  FAIL  {title}: {text}")
    if not failures:
        print("  PASS  Protected files, dependencies, secrets, architecture, Definition of Tested")
        print("\nRESULT: PASS")
        return 0
    n = len(failures)
    print(f"\nRESULT: FAIL ({n} problem{'s' if n != 1 else ''}) - fix these before commit / merge.")
    return 1


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    except (AttributeError, ValueError):
        pass
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "check":
        ap = argparse.ArgumentParser(
            prog="ess_guard.py check", description="ESS guardrail branch check"
        )
        ap.add_argument("--base", default=CFG["base_branch"], help="branch to compare against")
        ap.add_argument("--no-tests", action="store_true", help="skip running the tests")
        args = ap.parse_args(sys.argv[2:])
        return branch_check(args.base, args.no_tests)
    if mode in ("prompt", "tool"):
        try:
            data = json.loads(sys.stdin.read() or "{}")
        except ValueError:
            return 0  # never break the session on bad input
        if mode == "prompt":
            on_prompt(data)
        else:
            on_tool(data)
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
