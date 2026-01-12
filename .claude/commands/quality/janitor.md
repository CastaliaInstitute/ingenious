Run code quality checks in parallel using Opus subagents and git worktrees. **Fix all issues found—don't just report them.**

Create a separate git worktree for each tool, spawn an Opus subagent per worktree, and merge all changes into the `soca` branch when complete.

## Tools to run

- `/bandit` — Python security linter
- `/docstrings` — Python docstring checker
- `/mypy` — Python type checker
- `/radon` — Python complexity metrics
- `/vulture` — Python dead code finder
- `/audit` — Dependency vulnerability scan
- `/complexity` — Code complexity analysis
- `/jsdoc` — JavaScript documentation checker
- `/knip` — JavaScript unused exports/dependencies
- `/tsc` — TypeScript compiler checks

## Instructions

1. Create a git worktree for each tool in a temp directory
2. Launch all Opus subagents concurrently (one per tool/worktree)
3. Each subagent must:
   - Run its assigned tool
   - **Automatically fix every issue found** (not just diagnose)
   - Group fixes into small, logical commits with clear messages
4. Wait for all subagents to complete
5. Merge each subagent's commits into the `soca` branch, preserving the small logical commits (rebase or cherry-pick as needed to maintain clean history)
6. Resolve any merge conflicts
7. Clean up worktrees when finished

**Important:** The goal is a fully remediated codebase with a clean commit history, not a report. Take action on every finding.
