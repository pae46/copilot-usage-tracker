# Copilot Usage Tracker — Agent Instructions

## Project Overview

Single-file SwiftBar/xbar menu bar plugin for macOS that displays GitHub Copilot AI Credits usage. Written in pure Python 3 with no external dependencies.

This repo is a fork of https://github.com/bristena-op/copilot-usage-tracker, modified to show AI Credits instead of Premium Requests, with per-model breakdown, burn-rate indicator, monthly reset countdown, total cost, and optional OpenRouter balance tracking.

## Key Files

- `copilot-spending.py` — the entire plugin, one file
- `.env` — local credentials and settings, never committed
- `.env.example` — template for configuration
- `README.md` — user-facing setup and usage documentation
- `AGENTS.md` — instructions for coding agents working in this repo

## Installation / Symlink Convention

The plugin runs via a symlink in the SwiftBar Plugins folder:

```bash
~/Library/Application Support/SwiftBar/Plugins/copilot-spending.py → /path/to/repo/copilot-spending.py
```

When moving or renaming the plugin, always update both the repo file and the symlink:

```bash
# Remove old symlink
rm "$HOME/Library/Application Support/SwiftBar/Plugins/copilot-spending.py"

# Create new symlink pointing to repo
ln -s "$(pwd)/copilot-spending.py" "$HOME/Library/Application Support/SwiftBar/Plugins/copilot-spending.py"
```

## Schedule

Refresh schedule is controlled only by the SwiftBar metadata header in `copilot-spending.py`:

```python
# <swiftbar.schedule>*/2 * * * *</swiftbar.schedule>
```

**Do not use the filename to control schedule** (e.g. `15m` suffix is not used). Always edit the `swiftbar.schedule` header instead.

## Configuration

Loaded from `.env` in this priority order:

1. Same directory as `copilot-spending.py`
2. Parent of the `Plugins` directory when the script is symlinked from `~/Library/Application Support/SwiftBar/Plugins`
3. `~/.copilot-tracker/.env`

See `.env.example` for all variables:

- `GITHUB_TOKEN` — Fine-grained PAT with **Account → Plan (read-only)** permission
- `GITHUB_USERNAME` — GitHub username
- `PLAN_LIMIT` — Monthly AI Credits limit. Examples: Pro `1500`, Pro+ `7000`, Max `20000`
- `ORANGE_THRESHOLD` — Burn-rate warning threshold; `1.0` means usage is on expected monthly pace
- `RED_THRESHOLD` — Burn-rate critical threshold; `1.2` means usage is 20% ahead of expected pace
- `OPENROUTER_MANAGEMENT_KEY` — Optional OpenRouter Management API key

## SwiftBar Metadata Headers

All SwiftBar/xbar behavior is controlled via comment headers at the top of `copilot-spending.py`. Keep them in sync with actual behavior:

```python
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>
# <swiftbar.schedule>*/2 * * * *</swiftbar.schedule>
# <swiftbar.refreshOnOpen>false</swiftbar.refreshOnOpen>
```

## GitHub API

- Endpoint: `GET /users/{username}/settings/billing/ai_credit/usage`
- Uses `urllib` only, no `requests` or other third-party libraries
- Auth: `Bearer {GITHUB_TOKEN}` header
- Response field used for totals: `usageItems[].grossQuantity`
- Response field used for cost: `usageItems[].grossAmount`

## OpenRouter API

- Endpoint: `GET /api/v1/credits`
- Uses `urllib` only
- Auth: `Bearer {OPENROUTER_MANAGEMENT_KEY}` header
- Response fields used: `data.total_credits`, `data.total_usage`
- Shows remaining balance, spent amount, and loaded credits when a management key is configured

## Output Format

Plugin prints to stdout in SwiftBar format:

1. First line → menu bar title, usually usage percentage with color
2. `---` separator
3. Dropdown content:
   - GitHub Copilot section with burn-rate bar, credits progress bar, per-model breakdown, total cost, reset countdown, and GitHub link
   - Optional OpenRouter section with remaining balance, spent/loaded credits, activity link, and logs link
   - Footer separator and refresh action

If configuration is missing, the plugin prints setup instructions instead of API data.

## Development

Test locally:

```bash
python3 copilot-spending.py
```

When editing:

- Keep `README.md` in sync with actual configuration names, endpoints, and schedule.
- Keep SwiftBar metadata headers in sync with actual behavior.
- Do not add external Python dependencies unless explicitly requested.
- Avoid committing `.env`; it is local-only.

