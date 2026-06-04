# GitHub Copilot AI Credits Usage Widget for macOS

> 🍴 **Fork** of GitHub Copilot usage tracking widget — modified to track **AI Credits** instead of Premium Requests, with per-model breakdown and Python implementation.
> - **Original:** https://github.com/your-original-repo (if applicable)
> - **Maintained by:** [@pae46](https://github.com/pae46)

A SwiftBar/xbar menu bar widget that shows your GitHub Copilot AI Credits usage with detailed breakdown by model.

## Features

✨ **What's different in this fork:**
- Tracks **AI Credits** (instead of Premium Requests)
- **Per-model breakdown**: Claude Sonnet, Claude Haiku, Gemini, etc.
- **Python** implementation (no external dependencies)
- **Total cost** displayed in USD
- Supports **Pro+** plan (7000 AI Credits limit)
- Shows usage percentage in menu bar (color-coded: 🟢 green → 🟡 yellow → 🔴 red)
- Progress bar with credits used/total
- Days until monthly reset

## Screenshot

<p align="center">
  <img src="screenshot.png" alt="Copilot AI Credits Widget" width="400">
</p>

## Requirements

- macOS
- [SwiftBar](https://github.com/swiftbar/SwiftBar) or [xbar](https://xbarapp.com/)
- Python 3.6+ (built-in on macOS)
- GitHub Personal Access Token with billing permissions

## Installation

### 1. Install SwiftBar

```bash
brew install swiftbar
```

### 2. Create a GitHub Personal Access Token

1. Go to [GitHub Token Settings](https://github.com/settings/tokens?type=beta)
2. Click **Generate new token** (Fine-grained)
3. Give it a name like "Copilot Usage Widget"
4. Under **Account permissions**, enable **Plan** → **Read-only**
5. Generate and copy the token

### 3. Configure and Deploy

1. Clone this repo or download `copilot-spending.15m.py`
2. Edit the file and replace:
   - `GITHUB_TOKEN` with your token
   - `GITHUB_USERNAME` with your GitHub username
3. Set `PLAN_LIMIT` based on your plan:
   - Pro: `1500`
   - Pro+: `7000`

### 4. Install to SwiftBar

```bash
# Make executable
chmod +x copilot-spending.15m.py

# Copy to SwiftBar plugins folder
cp copilot-spending.15m.py "$HOME/Library/Application Support/SwiftBar/Plugins/"
```

Or create a symlink (recommended for development):
```bash
ln -s "$(pwd)/copilot-spending.15m.py" "$HOME/Library/Application Support/SwiftBar/Plugins/"
```

### 5. Refresh SwiftBar

Click the SwiftBar icon → Refresh All

## Refresh Interval

The filename `copilot-spending.15m.py` sets refresh to every 15 minutes. Rename to change:
- `copilot-spending.5m.py` → 5 minutes
- `copilot-spending.1h.py` → 1 hour

## API Endpoints Used

- `GET /users/{username}/settings/billing/ai_credit/usage` — AI Credits usage per model
- Per-month breakdown with costs in USD

## Troubleshooting

**Plugin not appearing**
- Check SwiftBar is running
- Verify file is in `~/Library/Application Support/SwiftBar/Plugins/`
- Test manually: `python3 copilot-spending.15m.py`

**Showing "Error"**
- Verify `GITHUB_TOKEN` is correct and has "Plan" permission
- Check `GITHUB_USERNAME` matches your GitHub account
- Ensure token hasn't expired

**Wrong usage numbers**
- Verify you're on the correct plan (Pro vs Pro+)
- Check `PLAN_LIMIT` matches your subscription
- Token needs "Plan" read permission in Account settings

## Development

Test locally:
```bash
python3 copilot-spending.15m.py
```

SwiftBar format reference:
- Menu bar title (first line): `25.4% | color=#3fb950`
- Dropdown separator: `---`
- Standard output format for menu items

## License

MIT

---

**Contributing**: Feel free to fork, modify, and adapt for your needs!

