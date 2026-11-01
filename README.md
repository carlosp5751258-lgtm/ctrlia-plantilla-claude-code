# Plantilla de proyecto para Claude Code (Ctrl+IA)

**Repositorio plantilla de GitHub**: pulsa «Use this template» para crear tu repo a partir de este, o copia los archivos en tu proyecto.

Un proyecto listo para trabajar con Claude Code sin abrir agujeros: un `CLAUDE.md` corto, un `.claude/settings.json` con reglas allow, ask y deny y el modo bypass bloqueado, dos hooks (uno frena secretos, `rm -rf` amplios y push forzado a main; otro no deja terminar con los tests rotos), dos skills, un subagente revisor, un CI y un `.worktreeinclude`. Sin dependencias externas: Python 3 y git.

Explicación completa de cada archivo y de lo que **no** protege: https://ctrlia.dev/recetas/plantilla-claude-code.html (English: https://ctrlia.dev/en/recetas/plantilla-claude-code.html)

## Qué trae
| Archivo | Para qué |
| --- | --- |
| `CLAUDE.md` | Comandos, cómo trabaja el equipo y lo que no está en el código |
| `.claude/settings.json` | Permisos del equipo y registro de los hooks (va en git) |
| `.claude/hooks/proteger.py` | PreToolUse: bloquea secretos, `rm -rf` amplios y `git push --force` a main |
| `.claude/hooks/verificar.sh` | Stop: si hay cambios, Claude no termina hasta que pasen los tests |
| `.claude/skills/probar/SKILL.md` | `/probar`: ejecuta los tests y pega la salida real |
| `.claude/skills/preparar-pr/SKILL.md` | `/preparar-pr`: revisa la rama y redacta la descripción del PR (no hace push) |
| `.claude/agents/revisor.md` | Subagente revisor de solo lectura |
| `.github/workflows/ci.yml` | Tests en cada PR y fallo si se versiona un `.env` |
| `.worktreeinclude` | Copia `.env` a los worktrees de `claude --worktree` |
| `.gitignore`, `.env.example`, `src/`, `tests/` | Lo personal fuera de git y un ejemplo mínimo para probar |

## Cómo usarla
1. Crea tu repo desde la plantilla y borra `src/` y `tests/` de ejemplo.
2. Cambia el comando de tests (`python3 -m unittest discover -s tests -v`) por el tuyo en `CLAUDE.md`, `settings.json`, `verificar.sh`, las dos skills y `ci.yml`.
3. Valida el JSON: `python3 -m json.tool .claude/settings.json`.
4. Abre `claude` en modo interactivo una vez y acepta el diálogo de confianza: hasta entonces las reglas allow no se aplican.
5. En la sesión, comprueba `/hooks`, `/permissions`, `/skills` y `/context`.
6. Prueba de fuego: pide «lee el .env» (debe bloquearse) y «cambia sumar para que reste y termina» (el hook Stop debe devolver el test roto).
7. Activa en GitHub la protección de main exigiendo el check «tests» y una revisión.

Prueba los hooks sin abrir Claude:

```bash
echo '{"tool_name":"Read","tool_input":{"file_path":"/x/proyecto/.env"}}' | python3 .claude/hooks/proteger.py; echo "exit $?"   # exit 2
echo '{"stop_hook_active": false}' | CLAUDE_PROJECT_DIR=$PWD bash .claude/hooks/verificar.sh; echo "exit $?"
```

## Probado
Con Claude Code 2.1.316 en Linux: los hooks con entradas simuladas, el hook Stop con tests rotos y en verde, el CI, `claude doctor`, el aviso de reglas allow sin confianza y `claude -w`. Falta probarlo en una sesión con cuenta (ver la página).

## Licencia
MIT. Copyright (c) 2026 Ctrl+IA (Carlos P.).
