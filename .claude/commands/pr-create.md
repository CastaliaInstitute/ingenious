# Pull Request Creation

## Instructions

Use GitHub CLI to create a pull request with the remote branch `to-stable`.

## PR Guidelines

**CRITICAL Requirements:**
- **NEVER include emojis** in PR titles or descriptions
- **Maintain a concise, professional tone** in all PR content
- **DO NOT add attribution footers** (e.g., no "Generated with Claude Code")
- **DO NOT use squash merge** - preserve all commits
- Use clear, descriptive PR titles in imperative mood
- Include concise summary of changes in PR description
- List key changes as bullet points if applicable

## Command Format

```sh
gh pr create --base to-stable --title "Your PR title" --body "Your PR description"
```

## Example

```sh
gh pr create --base to-stable --title "Add authentication middleware" --body "Add JWT authentication middleware for API endpoints. Includes tests and documentation."
```
