#!/usr/bin/env python3
"""Hook PreToolUse: frena secretos, rm -rf fuera del proyecto y git push --force a main.
Versión corta; la completa y explicada está en la receta «hooks de seguridad» de ctrlia.dev."""
import json
import re
import sys

SECRETO = re.compile(r"(^|/)(\.env(\.[\w-]+)?|[\w.-]+\.pem|[\w.-]+\.key|id_rsa\w*|id_ed25519\w*)$")
PLANTILLA = re.compile(r"(^|/)\.env\.(example|sample|template)$")
SECRETO_EN_COMANDO = re.compile(r"(?<![\w.-])(\.env(\.[\w-]+)?|[\w.-]+\.pem|id_rsa\w*|id_ed25519\w*)(?![\w.-])")


def bloquear(motivo):
    print(f"Bloqueado por el hook de seguridad: {motivo}", file=sys.stderr)
    sys.exit(2)  # 2 = Claude Code cancela la herramienta y le pasa el motivo a Claude


def main():
    try:
        datos = json.load(sys.stdin)
    except ValueError:
        bloquear("entrada JSON ilegible; por seguridad no se ejecuta nada")
    herramienta = datos.get("tool_name", "")
    entrada = datos.get("tool_input", {}) or {}

    if herramienta in ("Read", "Edit", "Write"):
        ruta = entrada.get("file_path", "")
        if SECRETO.search(ruta) and not PLANTILLA.search(ruta):
            bloquear(f"'{ruta}' tiene secretos. Pide al usuario el dato que necesites.")
    elif herramienta == "Bash":
        comando = entrada.get("command", "")
        for m in SECRETO_EN_COMANDO.finditer(comando):
            if not re.fullmatch(r"\.env\.(example|sample|template)", m.group(1)):
                bloquear(f"el comando toca '{m.group(1)}', que tiene secretos.")
        for parte in re.split(r"&&|\|\||;|\||\n", comando):
            p = parte.split()
            if p[:1] == ["sudo"]:
                p = p[1:]
            opciones = "".join(o.lstrip("-") for o in p[1:] if o.startswith("-") and not o.startswith("--"))
            recursivo = "r" in opciones.lower() or "--recursive" in p
            forzado = "f" in opciones or "--force" in p
            if p[:1] == ["rm"] and recursivo and forzado:
                for destino in (x.strip("'\"") for x in p[1:] if not x.startswith("-")):
                    if destino in (".", "./", "..", "*", "./*") or destino.startswith(("/", "~", "$HOME", "..")):
                        bloquear(f"'rm -rf {destino}' es demasiado amplio. Borra rutas concretas del proyecto.")
            if re.search(r"\bgit\b.*\bpush\b", parte) and re.search(r"\s(--force\S*|-[a-zA-Z]*f)\b", parte) \
                    and re.search(r"\b(main|master)\b", parte):
                bloquear("'git push --force' a main está prohibido. Usa una rama y un pull request.")
    sys.exit(0)  # sin objeciones: sigue el flujo normal de permisos


if __name__ == "__main__":
    main()
