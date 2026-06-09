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
- **🆕 OpenRouter integration** (optional): Track monthly spend and key balance
  - Budget progress bar (if configured)
  - Monthly usage summary

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

### 3. Configure with .env file

1. Clone this repo or download `copilot-spending.py`
2. Copy and configure `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your GitHub values:
   ```env
   GITHUB_TOKEN=github_pat_YOUR_TOKEN_HERE
   GITHUB_USERNAME=your_github_username
   PLAN_LIMIT=7000
   ```
   - `GITHUB_TOKEN`: Your Personal Access Token from step 2
   - `GITHUB_USERNAME`: Your GitHub username
   - `PLAN_LIMIT`: Based on your plan (Free: `50`, Pro: `300`, Pro+: `7000`)

4. **(Optional) Configure OpenRouter:**
   ```env
   OPENROUTER_API_KEY=sk_your_openrouter_key
   OPENROUTER_MONTHLY_BUDGET=20
   ```
   - Get your key from [OpenRouter settings](https://openrouter.ai/settings/keys)
   - `OPENROUTER_MONTHLY_BUDGET`: Display monthly budget progress bar (leave empty to disable)

**Note:** `.env` is never committed to git (see `.gitignore`). Safe for local use only!

### 4. Install to SwiftBar

```bash
# Make executable
chmod +x copilot-spending.py

# Copy to SwiftBar plugins folder
cp copilot-spending.py "$HOME/Library/Application Support/SwiftBar/Plugins/"
```

Or create a symlink (recommended for development):
```bash
ln -s "$(pwd)/copilot-spending.py" "$HOME/Library/Application Support/SwiftBar/Plugins/"
```

### 5. Refresh SwiftBar

Click the SwiftBar icon → Refresh All

## Refresh Interval

The refresh interval is controlled by the `swiftbar.schedule` header in the script (default: every 1 minute).
To change, edit the header at the top of `copilot-spending.py`:
```python
# <swiftbar.schedule>1 * * * *</swiftbar.schedule>
```
(Cron format: `minute hour day month weekday`)

## API Endpoints Used

### GitHub Copilot
- `GET /users/{username}/settings/billing/ai_credit/usage` — AI Credits usage per model
- Per-month breakdown with costs in USD

### OpenRouter (Optional)
- `GET /api/v1/key` — Current balance, monthly usage, key limits
- Returns monthly spend and remaining credits (if key limit set)

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

