#!/usr/bin/env python3
"""PreToolUse hook: stops secrets, rm -rf outside the project and git push --force to main.
Short version; the full, explained one is in the "security hooks" recipe on ctrlia.dev."""
import json
import re
import sys

SECRET = re.compile(r"(^|/)(\.env(\.[\w-]+)?|[\w.-]+\.pem|[\w.-]+\.key|id_rsa\w*|id_ed25519\w*)$")
TEMPLATE = re.compile(r"(^|/)\.env\.(example|sample|template)$")
SECRET_IN_COMMAND = re.compile(r"(?<![\w.-])(\.env(\.[\w-]+)?|[\w.-]+\.pem|id_rsa\w*|id_ed25519\w*)(?![\w.-])")


def block(reason):
    print(f"Blocked by the security hook: {reason}", file=sys.stderr)
    sys.exit(2)  # 2 = Claude Code cancels the tool and passes the reason to Claude


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        block("unreadable JSON input; for safety nothing is run")
    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input", {}) or {}

    if tool in ("Read", "Edit", "Write"):
        path = tool_input.get("file_path", "")
        if SECRET.search(path) and not TEMPLATE.search(path):
            block(f"'{path}' contains secrets. Ask the user for the value you need.")
    elif tool == "Bash":
        command = tool_input.get("command", "")
        for m in SECRET_IN_COMMAND.finditer(command):
            if not re.fullmatch(r"\.env\.(example|sample|template)", m.group(1)):
                block(f"the command touches '{m.group(1)}', which contains secrets.")
        for part in re.split(r"&&|\|\||;|\||\n", command):
            p = part.split()
            if p[:1] == ["sudo"]:
                p = p[1:]
            flags = "".join(o.lstrip("-") for o in p[1:] if o.startswith("-") and not o.startswith("--"))
            recursive = "r" in flags.lower() or "--recursive" in p
            forced = "f" in flags or "--force" in p
            if p[:1] == ["rm"] and recursive and forced:
                for target in (x.strip("'\"") for x in p[1:] if not x.startswith("-")):
                    if target in (".", "./", "..", "*", "./*") or target.startswith(("/", "~", "$HOME", "..")):
                        block(f"'rm -rf {target}' is too broad. Delete specific paths inside the project.")
            if re.search(r"\bgit\b.*\bpush\b", part) and re.search(r"\s(--force\S*|-[a-zA-Z]*f)\b", part) \
                    and re.search(r"\b(main|master)\b", part):
                block("'git push --force' to main is forbidden. Use a branch and a pull request.")
    sys.exit(0)  # no objections: the normal permission flow continues


if __name__ == "__main__":
    main()
