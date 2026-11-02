---
name: run-tests
description: Runs the project's tests and summarizes the result with the evidence. Use it after changing code or when the user asks whether something works.
allowed-tools: Bash(python3 -m unittest *)
---
1. Run `python3 -m unittest discover -s tests -v`.
2. If everything passes, reply with the number of tests and the last line of the output (for example `OK`).
3. If something fails, copy the test name, the error and the file and line where it happens.
   Suggest the most likely cause, but don't change code if the user only asked to run the tests.
4. Never say "everything works" without pasting the real output.
