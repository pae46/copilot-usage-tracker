# Copilot Usage Tracker — Agent Instructions

## Project Overview

Single-file SwiftBar/xbar menu bar plugin for macOS that displays GitHub Copilot AI Credits usage. Written in pure Python 3 with no external dependencies.

## Key Files

- `copilot-spending.py` — the entire plugin (one file, ~230 lines)
- `.env` — local credentials (never committed, see `.gitignore`)
- `.env.example` — template for configuration

## Installation / Symlink Convention

The plugin runs via a symlink in the SwiftBar Plugins folder:

```
~/Library/Application Support/SwiftBar/Plugins/copilot-spending.py → /path/to/repo/copilot-spending.py
```

When renaming the file, always update both the repo file and the symlink:

```bash
# Remove old symlink
rm "$HOME/Library/Application Support/SwiftBar/Plugins/copilot-spending.py"
# Create new symlink pointing to repo
ln -s "$(pwd)/copilot-spending.py" "$HOME/Library/Application Support/SwiftBar/Plugins/copilot-spending.py"
```

## Schedule

Refresh schedule is controlled by the SwiftBar metadata header in `copilot-spending.py`:

```python
# <swiftbar.schedule>1 * * * *</swiftbar.schedule>
```

**Do not use the filename to control schedule** (e.g. `15m` suffix is no longer used). Always edit the `swiftbar.schedule` header instead.

## Configuration

Loaded from `.env` in the script directory (repo root when using symlink). See `.env.example` for all variables:

- `GITHUB_TOKEN` — Fine-grained PAT with **Account → Plan (read-only)** permission
- `GITHUB_USERNAME` — GitHub username
- `PLAN_LIMIT` — Free: `50`, Pro: `300`, Pro+: `7000`

## SwiftBar Metadata Headers

All SwiftBar/xbar behavior is controlled via comment headers at the top of `copilot-spending.py`. Keep them in sync with actual behavior:

```python
# <swiftbar.refreshOnOpen>true</swiftbar.refreshOnOpen>
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.schedule>1 * * * *</swiftbar.schedule>
```

## GitHub API

- Endpoint: `GET /users/{username}/settings/billing/ai_credit/usage`
- Uses `urllib` only (no `requests` or other third-party libs)
- Auth: `Bearer {GITHUB_TOKEN}` header

## Output Format

Plugin prints to stdout in SwiftBar format:
1. First line → menu bar title
2. `---` separator
3. Dropdown content
