# Version Bump and Release Workflow

## Objective

Increment the patch version (vx.x.x to vx.x.(x+1)), create a pull request, merge it, and publish a new release to GitHub and PyPI.

## Workflow Steps

### 1. Version Detection and Update

1. **Find current version**: Search for version references in:
   - `pyproject.toml` (version field)
   - `ingenious/__init__.py` (__version__ attribute)
   - `CLAUDE.md` (version documentation)
   - Any other files containing version strings

2. **Calculate new version**: Increment the patch number (e.g., v0.2.7 → v0.2.8)

3. **Update all version references**: Replace all occurrences of the old version with the new version across all identified files

4. **Verify changes**: Confirm all version references have been updated correctly

### 2. Pull Request Creation

Run the `/pr-create` command to create a pull request with:
- **Title format**: "Bump version to vx.x.x"
- **Description**: "Update version from vx.x.x to vx.x.x across all files"
- Target branch: `to-stable`

### 3. Pull Request Merge

Run the `/pr-merge` command to:
- Merge the version bump PR to `to-stable`
- Run complete quality assurance pipeline (pytest, pre-commit, mypy)
- Merge `to-stable` to `main`
- Use `--admin` flag
- Preserve all commits (no squash)
- Keep branches intact (no deletion)

### 4. GitHub Release Creation

After successful merge to `main`:

```sh
gh release create vx.x.x \
  --title "Release vx.x.x" \
  --notes "Release version x.x.x" \
  --target main
```

### 5. PyPI Release Verification

1. **Check GitHub Actions**: Verify the PyPI release workflow has been triggered

```sh
gh run list --workflow=pypi-release.yml --limit 1
```

2. **Monitor release progress**: Check the workflow status

```sh
gh run watch
```

3. **Verify completion**: Ensure the PyPI release action completes successfully

## Guidelines

**CRITICAL Requirements:**
- **NEVER include emojis** in any commit messages, PR titles, descriptions, or release notes
- **Maintain a concise, professional tone** throughout
- **DO NOT add attribution footers** in any commits or releases
- Update ALL version references consistently across the codebase
- Ensure version format consistency (with or without 'v' prefix as per existing convention)
- Verify quality checks pass before proceeding to release
- Confirm PyPI workflow triggers automatically after release creation

## Error Handling

- If version detection fails, report the issue and request manual version specification
- If quality checks fail during merge, resolve issues before proceeding to release
- If PyPI workflow does not trigger, investigate GitHub Actions configuration
- If PyPI release fails, check authentication credentials and workflow logs

## Communication

- Report current version detected
- Confirm new version to be used
- Show status of each step (PR creation, merge, quality checks, release, PyPI)
- Provide links to created PR, merged commits, and release page
- Confirm successful completion of entire workflow
