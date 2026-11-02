# Project: sample app (Ctrl+IA template)

## Commands
- Tests: `python3 -m unittest discover -s tests -v`
- A single test: `python3 -m unittest tests.test_app -v`
- There is no build step: it is pure Python, with no external dependencies.

## How we work
- Before calling something done, run the tests and paste the command and its output.
- Small changes: one task, one branch, one pull request.
- Don't add new dependencies without asking first.
- Don't touch `.github/workflows/` or `.claude/` unless asked to.

## What isn't in the code
- Secrets go in `.env` (not in git). Use `.env.example` to see which variables exist; never read or copy `.env`.
- `main` is protected: it is only merged through a pull request with green CI.
