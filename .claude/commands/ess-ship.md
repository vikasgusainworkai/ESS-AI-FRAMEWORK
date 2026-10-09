---
description: Commit and push the approved change through the ESS gate
argument-hint: <ticket id> [short title]
---

The developer has approved the current change for: $ARGUMENTS

1. Run `git status` and `git diff --stat` and list the files that belong to this change. Leave out anything you did not change for this ticket.
2. Run exactly one command (the developer gets a permission prompt for it; that prompt is the approval gate):
   `python tools/ess_ship.py --ticket <TICKET-ID> --title "<one-line summary>" --type fix --body "<root cause and fix in one or two sentences>" --files <file> <file> ...`
   Use `--type feat` for a feature. Never run `git commit` or `git push` directly; they are denied.
3. Report the result in the developer's words: branch, commit, test result, push target and PR link if one was opened. If the script STOPPED, quote its reason, fix the cause only if it is inside the approved scope, and ask before shipping again.
