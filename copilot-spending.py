#!/Library/Frameworks/Python.framework/Versions/3.12/bin/python3

# <xbar.title>Copilot AI Credits</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>pae46</xbar.author>
# <xbar.author.github>pae46</xbar.author.github>
# <xbar.desc>GitHub Copilot AI Credits usage tracking with per-model breakdown and monthly reset countdown.</xbar.desc>
# <xbar.dependencies>python3</xbar.dependencies>
# <xbar.abouturl>https://github.com/pae46/copilot-usage-tracker</xbar.abouturl>

# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>
# <swiftbar.schedule>01 * * * *</swiftbar.schedule>

"""
SwiftBar plugin for GitHub Copilot AI Credits usage tracking.
Displays AI Credits consumption with per-model breakdown and monthly reset countdown.
Configuration loaded from .env file.
"""

import json
import urllib.request
import urllib.error
import os
from datetime import datetime, timedelta
from calendar import monthrange
from pathlib import Path


def load_env_file(env_path=".env"):
    """Load environment variables from .env file.
    Searches in multiple locations:
    1. Same directory as script (repo root when via symlink)
    2. Symlink's parent directory (plugins folder)
    3. User's home directory
    """
    env_vars = {}
    script_dir = Path(__file__).parent
    
    # List of places to search for .env
    search_paths = [
        script_dir / env_path,  # Where script is located
        script_dir.parent / env_path if script_dir.name == "Plugins" else None,  # Parent of Plugins folder
        Path.home() / ".copilot-tracker" / env_path,  # ~/.copilot-tracker/.env
    ]
    
    for env_file in search_paths:
        if env_file and env_file.exists():
            try:
                with open(env_file, "r") as f:
                    for line in f:
                        line = line.strip()
                        # Skip comments and empty lines
                        if not line or line.startswith("#"):
                            continue
                        # Parse KEY=VALUE
                        if "=" in line:
                            key, value = line.split("=", 1)
                            env_vars[key.strip()] = value.strip()
                # Found and loaded successfully
                return env_vars
            except Exception:
                continue
    
    return env_vars


# Load configuration from .env or environment variables
env_vars = load_env_file()
GITHUB_TOKEN = env_vars.get("GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
GITHUB_USERNAME = env_vars.get("GITHUB_USERNAME") or os.environ.get("GITHUB_USERNAME", "")
PLAN_LIMIT = int(env_vars.get("PLAN_LIMIT", os.environ.get("PLAN_LIMIT", 7000)))

# OpenRouter configuration (optional — requires management key)
OPENROUTER_MANAGEMENT_KEY = env_vars.get("OPENROUTER_MANAGEMENT_KEY") or os.environ.get("OPENROUTER_MANAGEMENT_KEY", "")

# ===================================

def fetch_copilot_data():
    """Fetch AI Credits usage from GitHub API."""
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/settings/billing/ai_credit/usage"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": e.code}
    except Exception as e:
        return {"error": str(e)}


def fetch_openrouter_data():
    """Fetch OpenRouter account credits from management API."""
    if not OPENROUTER_MANAGEMENT_KEY:
        return None
    
    url = "https://openrouter.ai/api/v1/credits"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_MANAGEMENT_KEY}",
        "Accept": "application/json"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            return result.get("data", result)
    except urllib.error.HTTPError as e:
        return {"error": e.code}
    except Exception as e:
        return {"error": str(e)}


def get_days_until_reset():
    """Calculate days until monthly reset (end of current month)."""
    today = datetime.now()
    _, last_day = monthrange(today.year, today.month)
    reset_date = datetime(today.year, today.month, last_day)
    days_left = (reset_date - today).days + 1
    return max(0, days_left)


def format_number(num):
    """Format number with space thousands separator (for titles)."""
    return f"{int(num):,}".replace(",", " ")


def format_badge(num):
    """Format number with comma separator (safe for SwiftBar badge param)."""
    return f"{int(num):,}"


def get_color(percentage):
    """Return hex color based on usage percentage."""
    if percentage < 60:
        return "#3fb950"  # Green
    elif percentage < 85:
        return "#d29922"  # Yellow
    else:
        return "#f85149"  # Red


def render_copilot(data):
    """Render GitHub Copilot AI Credits section to stdout (dropdown part only)."""
    # Calculate totals and per-model usage
    items = data.get("usageItems", [])
    total_credits = sum(item["grossQuantity"] for item in items)
    total_cost = sum(item["grossAmount"] for item in items)
    
    percentage = (total_credits / PLAN_LIMIT) * 100
    percentage_clamped = min(percentage, 100)
    color = get_color(percentage_clamped)
    
    # Build progress bar
    bar_length = 20
    filled = int(percentage_clamped * bar_length / 100)
    empty = bar_length - filled
    progress_bar = "█" * filled + "░" * empty
    
    # Sort items by usage (descending)
    sorted_items = sorted(items, key=lambda x: x["grossQuantity"], reverse=True)
    
    # Days until reset
    days_left = get_days_until_reset()
    
    # Dropdown content for Copilot
    month_label = datetime.now().strftime("%B %Y")
    print("---")
    print(f"**AI Credits — {month_label}** | size=13 md=true")
    print(f"{progress_bar}  {format_number(int(total_credits))} / {format_number(PLAN_LIMIT)} credits  ({percentage_clamped:.1f}%) | size=12 color={color} font=Menlo")
    print("---")
    
    # Per-model breakdown
    max_name_len = max((len(item["model"]) for item in sorted_items), default=0)
    max_qty_len = max((len(format_badge(int(item["grossQuantity"]))) for item in sorted_items), default=0)
    print("By Model | size=11 color=gray")
    for item in sorted_items:
        model_name = item["model"]
        quantity = int(item["grossQuantity"])
        pct = (quantity / total_credits * 100) if total_credits > 0 else 0
        mini_filled = int(pct * 8 / 100)
        mini_bar = "█" * mini_filled + "░" * (8 - mini_filled)
        padded_name = model_name.ljust(max_name_len)
        padded_qty = format_badge(quantity).rjust(max_qty_len)
        print(f"{padded_name}  {mini_bar}  {pct:5.1f}%  {padded_qty} cr | size=11 font=Menlo")
    
    print("---")
    print(f"Total Cost: ${total_cost:.2f} | size=11 font=Menlo")
    print(f"Resets in {days_left} days | size=11 font=Menlo")
    print("View on GitHub | href=https://github.com/settings/copilot/features")


def render_openrouter(data):
    """Render OpenRouter credits section to stdout."""
    print("---")
    
    if data is None or "error" in data:
        if data and "error" in data:
            print("**OpenRouter** | size=13 md=true")
            print(f"Error (HTTP {data['error']}) | size=11 color=#f85149")
        return
    
    # /api/v1/credits returns total_credits (loaded) and total_usage (spent, all-time)
    total_credits = data.get("total_credits", 0)
    total_usage = data.get("total_usage", 0)
    remaining = max(total_credits - total_usage, 0)
    
    print("**OpenRouter** | size=13 md=true")
    
    # Balance progress bar (spent vs loaded, all-time)
    if total_credits > 0:
        spent_pct = (total_usage / total_credits) * 100
        spent_pct_clamped = min(spent_pct, 100)
        color = get_color(spent_pct_clamped)
        
        bar_length = 20
        filled = int(spent_pct_clamped * bar_length / 100)
        empty = bar_length - filled
        progress_bar = "█" * filled + "░" * empty
        
        print(f"{progress_bar}  ${remaining:.2f} remaining  ({100 - spent_pct_clamped:.1f}%) | size=12 color={color} font=Menlo")
        print(f"Spent: ${total_usage:.2f} / Loaded: ${total_credits:.2f} | size=11 font=Menlo")
    else:
        print(f"Balance: ${remaining:.2f} | size=12 font=Menlo")
    
    print("View on OpenRouter | href=https://openrouter.ai/activity")
    print("View Logs | href=https://openrouter.ai/logs")


# Fetch data from both providers
copilot_data = fetch_copilot_data()
openrouter_data = fetch_openrouter_data()

# Render outputs
if not GITHUB_TOKEN or not GITHUB_USERNAME:
    print("Setup | color=#f85149")
    print("---")
    print("Configuration missing | size=12 color=#f85149")
    print("---")
    print("1. Create .env file from .env.example:")
    print("   cp .env.example .env")
    print("2. Edit .env and add your:")
    print("   - GITHUB_TOKEN")
    print("   - GITHUB_USERNAME")
    print("---")
    print("More info | href=https://github.com/pae46/copilot-usage-tracker#setup")
    print("Refresh | refresh=true")
elif "error" in copilot_data:
    # Copilot API error
    print("Error | color=#f85149")
    print("---")
    print(f"HTTP {copilot_data['error']} | size=11 color=#f85149")
    print("Refresh | refresh=true")
else:
    # Successful Copilot data fetch - calculate menu bar color
    items = copilot_data.get("usageItems", [])
    total_credits = sum(item["grossQuantity"] for item in items)
    percentage = (total_credits / PLAN_LIMIT) * 100
    percentage_clamped = min(percentage, 100)
    color = get_color(percentage_clamped)
    
    # Menu bar title
    print(f"{percentage_clamped:.1f}% | color={color}")
    
    # Render Copilot section (dropdown)
    render_copilot(copilot_data)
    
    # Render OpenRouter section if available (dropdown)
    if openrouter_data:
        render_openrouter(openrouter_data)
    
    # Footer
    print("---")
    print("Refresh | refresh=true")
