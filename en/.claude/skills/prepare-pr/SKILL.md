---
name: prepare-pr
description: Reviews the current branch before opening a pull request (tests, secrets, dependencies and out-of-scope changes) and drafts the PR description.
disable-model-invocation: true
allowed-tools: Bash(git diff *) Bash(git log *) Bash(git status *) Bash(python3 -m unittest *)
---
Prepare the pull request for the current branch against `main`.

1. `git log --oneline main..HEAD` and `git diff --stat main...HEAD`: summarize what changes.
2. Run the tests: `python3 -m unittest discover -s tests -v`. If they fail, stop and say so.
3. Review `git diff main...HEAD` and point out, with file and line:
   - keys, tokens or passwords written in the code;
   - new dependencies or changed versions;
   - files that have nothing to do with the requested task;
   - tests deleted, skipped or with weakened assertions.
4. Write the PR description: what changes, why, how it was tested (with the output) and what the reviewer should look at.
Don't run `git push` or open the PR: the user does that.
