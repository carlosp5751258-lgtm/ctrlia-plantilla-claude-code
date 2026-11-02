#!/usr/bin/env bash
# Stop hook: if there are untested changes, Claude can't finish until the tests pass.
set -euo pipefail
input=$(cat)
# If we are already in a turn triggered by this hook, don't insist (avoids loops).
if grep -q '"stop_hook_active": *true' <<<"$input"; then exit 0; fi
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
# With no changes in the working tree there is nothing to check.
if [ -z "$(git status --porcelain 2>/dev/null || true)" ]; then exit 0; fi
if ! output=$(python3 -m unittest discover -s tests 2>&1); then
  printf 'The tests fail; fix them before finishing:\n%s\n' "$output" | tail -n 40 >&2
  exit 2
fi
exit 0
