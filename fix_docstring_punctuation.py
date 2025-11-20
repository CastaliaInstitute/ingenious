#!/usr/bin/env python3
"""Fix docstrings that are missing ending punctuation (D415).

This script automatically adds periods to docstrings that don't end with
proper punctuation (.?!).
"""

import re
from pathlib import Path
from typing import Tuple


def fix_docstring_punctuation(file_path: Path) -> Tuple[bool, str]:
    """Fix docstrings in a file by adding ending punctuation.

    Args:
        file_path: Path to the Python file to fix.

    Returns:
        Tuple of (True if file was modified, new content).
    """
    content = file_path.read_text()
    original_content = content

    # Pattern to match docstrings (both """ and ''')
    # Matches: """some text""" or '''some text'''
    # Where 'some text' doesn't end with .?!

    # Single-line docstrings
    pattern_single = r'("""|\'\'\')((?:(?!\1).)+?)(?<![.?!])\1'

    def add_punctuation(match: re.Match[str]) -> str:
        """Add period before closing quotes."""
        quote = match.group(1)
        text = match.group(2)
        # Don't add period if it's just whitespace or already ends with punctuation
        if not text.strip() or text.rstrip()[-1] in ".?!":
            return match.group(0)
        return f"{quote}{text}.{quote}"

    # Fix single-line docstrings
    content = re.sub(pattern_single, add_punctuation, content)

    return (content != original_content, content)


def main() -> None:
    """Fix D415 violations across test files."""
    # Get list of files with D415 violations
    import subprocess

    result = subprocess.run(
        ["uv", "run", "ruff", "check", "--select", "D415", "tests/", "--output-format=concise"],
        capture_output=True,
        text=True,
    )

    # Parse output to get unique file paths
    files_with_violations: set[str] = set()
    for line in result.stdout.splitlines():
        if line.startswith("tests/"):
            file_path_str = line.split(":")[0]
            files_with_violations.add(file_path_str)

    print(f"Found {len(files_with_violations)} files with D415 violations")

    modified_files: list[Path] = []
    for file_path_str in sorted(files_with_violations):
        file_path = Path(file_path_str)
        if file_path.exists():
            was_modified, new_content = fix_docstring_punctuation(file_path)
            if was_modified:
                file_path.write_text(new_content)
                modified_files.append(file_path)
                print(f"Fixed: {file_path}")

    print(f"\nModified {len(modified_files)} files")

    # Re-run ruff to see remaining violations
    result = subprocess.run(
        ["uv", "run", "ruff", "check", "--select", "D415", "tests/", "--output-format=concise"],
        capture_output=True,
        text=True,
    )

    remaining = len([line for line in result.stdout.splitlines() if line.startswith("tests/")])
    print(f"Remaining D415 violations: {remaining}")


if __name__ == "__main__":
    main()
