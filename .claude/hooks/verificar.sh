#!/usr/bin/env bash
# Hook Stop: si hay cambios sin probar, Claude no puede terminar hasta que pasen los tests.
set -euo pipefail
entrada=$(cat)
# Si ya estamos en una vuelta provocada por este hook, no insistas (evita bucles).
if grep -q '"stop_hook_active": *true' <<<"$entrada"; then exit 0; fi
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
# Sin cambios en el árbol de trabajo no hay nada que comprobar.
if [ -z "$(git status --porcelain 2>/dev/null || true)" ]; then exit 0; fi
if ! salida=$(python3 -m unittest discover -s tests 2>&1); then
  printf 'Los tests fallan; arréglalos antes de terminar:\n%s\n' "$salida" | tail -n 40 >&2
  exit 2
fi
exit 0
