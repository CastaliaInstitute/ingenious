# Verify and Fix Docstrings with Interrogate and Pydocstyle

Use static analysis tools to ensure all functions, classes, and modules have proper, consistent docstrings.

## CRITICAL: Persistence Requirement

**DO NOT STOP until ALL docstring issues are resolved.** This task requires complete coverage:
- Process every single file reported by the tools
- Fix every missing or malformed docstring
- Continue working through all modules systematically
- Re-run the analysis tools after each batch of fixes to confirm progress
- Only consider this task complete when both `interrogate` and `pydocstyle` report zero issues

If context window limits approach, document remaining files in the todo list and continue in the next session. Do not leave the codebase in a partially documented state.

## 1. Run Docstring Coverage Analysis

```bash
uv run interrogate -v . --fail-under 100 --ignore-init-method --ignore-init-module --exclude .venv --exclude venv --exclude .git --exclude __pycache__ --exclude node_modules
```

This shows which modules, classes, and functions are missing docstrings. The `-v` flag provides detailed output. The `--fail-under 100` ensures nothing is missed.

For a summary report:
```bash
uv run interrogate . --generate-badge /tmp/docstring-badge --exclude .venv --exclude venv
```

## 2. Run Docstring Style Check

```bash
uv run pydocstyle . --convention=google --match='(?!test_).*\.py' --ignore=D100,D104
```

This validates docstrings follow Google style conventions (D100 and D104 are ignored for module-level docstrings which are often unnecessary).

For specific error codes only:
```bash
uv run pydocstyle . --select=D101,D102,D103,D107
```

Key codes:
- D100: Missing docstring in public module
- D101: Missing docstring in public class
- D102: Missing docstring in public method
- D103: Missing docstring in public function
- D107: Missing docstring in __init__

## 3. Processing Order

Work through files systematically:
1. Start with public API functions and classes
2. Then complex functions with cyclomatic complexity >= B
3. Then entry points and orchestration code
4. Then utility functions and helpers
5. Finally, private methods and internal functions

**Document everything.** Even simple functions benefit from a one-line docstring describing their purpose.

## 4. Docstring Standards

Use Google-style docstrings consistently:

```python
def function_name(param1: str, param2: int) -> bool:
    """Short one-line summary ending with period.

    Longer description if needed. Explain the purpose,
    not the implementation.

    Args:
        param1: Description of first parameter.
        param2: Description of second parameter.

    Returns:
        Description of return value.

    Raises:
        ValueError: When param2 is negative.
    """
```

For classes:
```python
class ClassName:
    """Short one-line summary.

    Longer description of the class purpose and usage.

    Attributes:
        attr1: Description of attribute.
        attr2: Description of attribute.
    """
```

## 5. Fix Iteratively

For each file with issues:
1. Add missing docstrings starting with public interfaces
2. Fix style violations reported by pydocstyle
3. Verify changes:
   ```bash
   uv run interrogate -v <file.py>
   uv run pydocstyle <file.py> --convention=google
   ```
4. Commit when a file passes:
   ```bash
   git add <file.py>
   git commit -m "docs(<module>): add docstrings to <file>"
   ```

## 6. Validate Coverage Improvement

After each batch of fixes, re-run analysis to track progress:
```bash
uv run interrogate -v . --fail-under 100 --exclude .venv --exclude venv --exclude __pycache__
uv run pydocstyle . --convention=google --match='(?!test_).*\.py' --ignore=D100,D104
```

Continue fixing until both commands pass with zero issues. Then run tests:
```bash
uv run pytest
```

## 7. Install Dependencies (if missing)

```bash
uv add --dev interrogate pydocstyle
```

## Completion Criteria

This task is NOT complete until:
1. `uv run interrogate -v .` shows 100% coverage (excluding venv directories)
2. `uv run pydocstyle .` reports zero violations
3. All tests pass

**Do not stop early. Do not skip files. Process the entire codebase.**
