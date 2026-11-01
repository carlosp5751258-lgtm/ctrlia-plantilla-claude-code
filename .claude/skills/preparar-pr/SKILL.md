---
name: preparar-pr
description: Revisa la rama actual antes de abrir un pull request (tests, secretos, dependencias y cambios fuera de alcance) y redacta la descripción del PR.
disable-model-invocation: true
allowed-tools: Bash(git diff *) Bash(git log *) Bash(git status *) Bash(python3 -m unittest *)
---
Prepara el pull request de la rama actual contra `main`.

1. `git log --oneline main..HEAD` y `git diff --stat main...HEAD`: resume qué cambia.
2. Ejecuta los tests: `python3 -m unittest discover -s tests -v`. Si fallan, para y avisa.
3. Revisa `git diff main...HEAD` y señala, con archivo y línea:
   - claves, tokens o contraseñas escritos en el código;
   - dependencias nuevas o versiones cambiadas;
   - archivos que no tienen que ver con la tarea pedida;
   - tests borrados, saltados o con aserciones debilitadas.
4. Escribe la descripción del PR: qué cambia, por qué, cómo se probó (con la salida) y qué debe mirar quien revise.
No hagas `git push` ni abras el PR: eso lo hace el usuario.
