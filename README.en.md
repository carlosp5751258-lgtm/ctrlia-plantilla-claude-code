# Claude Code project template (Ctrl+IA)

The Spanish version is in the repository root and in [README.md](README.md); the English template is in `en/`.

**GitHub template repository**: click "Use this template" to create your repo from this one, or copy the files from `en/` into your project.

A project ready to work with Claude Code without opening holes: a short `CLAUDE.md`, a `.claude/settings.json` with allow, ask and deny rules and bypass mode blocked, two hooks (one stops secrets, broad `rm -rf` and force pushes to main; the other won't let Claude finish with broken tests), two skills, a reviewer subagent, a CI and a `.worktreeinclude`. No external dependencies: Python 3 and git.

Full explanation of every file and of what it does **not** protect against: https://ctrlia.dev/en/recetas/plantilla-claude-code.html (Español: https://ctrlia.dev/recetas/plantilla-claude-code.html)

## What's inside
| File | What for |
| --- | --- |
| `en/CLAUDE.md` | Commands, how the team works and what isn't in the code |
| `en/.claude/settings.json` | Team permissions and hook registration (goes in git) |
| `en/.claude/hooks/protect.py` | PreToolUse: blocks secrets, broad `rm -rf` and `git push --force` to main |
| `en/.claude/hooks/verify.sh` | Stop: if there are changes, Claude can't finish until the tests pass |
| `en/.claude/skills/run-tests/SKILL.md` | `/run-tests`: runs the tests and pastes the real output |
| `en/.claude/skills/prepare-pr/SKILL.md` | `/prepare-pr`: reviews the branch and drafts the PR description (no push) |
| `en/.claude/agents/reviewer.md` | Read-only reviewer subagent |
| `en/.github/workflows/ci.yml` | Tests on every PR and a failure if a `.env` is committed |
| `en/.worktreeinclude` | Copies `.env` into `claude --worktree` worktrees |
| `en/.gitignore`, `en/.env.example`, `en/src/`, `en/tests/` | Personal files out of git and a minimal example to test with |

## How to use it
1. Create your repo from the template and keep only the English version: from the root of your new repo, run the commands below (they delete the Spanish files and the READMEs, keep `.git` and `LICENSE`, and move the contents of `en/`, dotfiles included, to the root). Then delete the sample `src/` and `tests/`.

   ```bash
   find . -mindepth 1 -maxdepth 1 ! -name .git ! -name en ! -name LICENSE -exec rm -rf {} +
   (shopt -s dotglob; mv en/* .) && rmdir en
   ```

2. Replace the test command (`python3 -m unittest discover -s tests -v`) with yours in `CLAUDE.md`, `settings.json`, `verify.sh`, both skills and `ci.yml`.
3. Validate the JSON: `python3 -m json.tool .claude/settings.json`.
4. Open `claude` interactively once and accept the trust dialog: until then the allow rules don't apply.
5. In the session, check `/hooks`, `/permissions`, `/skills` and `/context`.
6. Stress test: ask "read the .env" (it should be blocked) and "change add so it subtracts and finish" (the Stop hook should hand back the broken test).
7. Turn on branch protection for main on GitHub, requiring the "tests" check and one review.

Test the hooks without opening Claude (from the root once you have moved `en/`, or from inside `en/`):

```bash
echo '{"tool_name":"Read","tool_input":{"file_path":"/x/project/.env"}}' | python3 .claude/hooks/protect.py; echo "exit $?"   # exit 2
echo '{"stop_hook_active": false}' | CLAUDE_PROJECT_DIR=$PWD bash .claude/hooks/verify.sh; echo "exit $?"
```

## Tested
With Claude Code 2.1.316 on Linux: the hooks with simulated inputs, the Stop hook with broken and green tests, the CI, `claude doctor`, the untrusted allow rules warning and `claude -w`. The English copy in `en/` was checked with the same simulated hook inputs, its tests and the move-to-root commands above. Still to test in a logged-in session (see the page).

## License
MIT. Copyright (c) 2026 Ctrl+IA (Carlos P.).
