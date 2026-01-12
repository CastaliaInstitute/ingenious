Run code quality checks in parallel using Opus subagents and git worktrees.

Create a separate git worktree for each tool, spawn an Opus subagent per worktree, and merge all outputs when complete.

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
3. Wait for all subagents to complete
4. Aggregate and summarize findings across all tools
5. Clean up worktrees when finished
