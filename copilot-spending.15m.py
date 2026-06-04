#!/Library/Frameworks/Python.framework/Versions/3.12/bin/python3

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
    """Load environment variables from .env file."""
    env_vars = {}
    env_file = Path(__file__).parent / env_path
    
    if not env_file.exists():
        return env_vars
    
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
    except Exception:
        pass
    
    return env_vars


# Load configuration from .env or environment variables
env_vars = load_env_file()
GITHUB_TOKEN = env_vars.get("GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
GITHUB_USERNAME = env_vars.get("GITHUB_USERNAME") or os.environ.get("GITHUB_USERNAME", "")
PLAN_LIMIT = int(env_vars.get("PLAN_LIMIT", os.environ.get("PLAN_LIMIT", 7000)))

# ===================================

def fetch_ai_credits():
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


def get_days_until_reset():
    """Calculate days until monthly reset (end of current month)."""
    today = datetime.now()
    _, last_day = monthrange(today.year, today.month)
    reset_date = datetime(today.year, today.month, last_day)
    days_left = (reset_date - today).days + 1
    return max(0, days_left)


def format_number(num):
    """Format number with thousands separator."""
    return f"{int(num):,}".replace(",", " ")


def get_color(percentage):
    """Return hex color based on usage percentage."""
    if percentage < 50:
        return "#3fb950"  # Green
    elif percentage < 80:
        return "#d29922"  # Yellow
    else:
        return "#f85149"  # Red


# Fetch data
data = fetch_ai_credits()

if not GITHUB_TOKEN or not GITHUB_USERNAME:
    print("⚙️  Setup | sfcolor=#f85149")
    print("---")
    print("Configuration missing!")
    print("---")
    print("1. Create .env file from .env.example:")
    print("   cp .env.example .env")
    print("2. Edit .env and add your:")
    print("   - GITHUB_TOKEN")
    print("   - GITHUB_USERNAME")
    print("---")
    print("More info | href=https://github.com/pae46/copilot-usage-tracker#setup")
    print("Refresh | refresh=true")
elif "error" in data:
    print(f"⚠️  Error | sfcolor=#f85149")
    print("---")
    print(f"HTTP {data['error']}")
    print("Refresh | refresh=true")
else:
    # Calculate totals and per-model usage
    items = data.get("usageItems", [])
    total_credits = sum(item["grossQuantity"] for item in items)
    total_cost = sum(item["grossAmount"] for item in items)
    
    percentage = (total_credits / PLAN_LIMIT) * 100
    percentage_clamped = min(percentage, 100)
    color = get_color(percentage_clamped)
    
    # Build progress bar
    bar_length = 10
    filled = int(percentage_clamped * bar_length / 100)
    empty = bar_length - filled
    progress_bar = "▓" * filled + "░" * empty
    
    # Sort items by usage (descending)
    sorted_items = sorted(items, key=lambda x: x["grossQuantity"], reverse=True)
    
    # Days until reset
    days_left = get_days_until_reset()
    
    # Menu bar text
    print(f"{percentage_clamped:.1f}% | color={color} sfcolor={color}")
    
    # Dropdown menu
    print("---")
    print(f"AI Credits — June 2026 | size=13 weight=bold")
    print(f"{progress_bar} {format_number(int(total_credits))}/{format_number(PLAN_LIMIT)} | size=11")
    print("---")
    
    # Per-model breakdown
    print("By Model | size=11 color=gray")
    for item in sorted_items:
        model_name = item["model"]
        quantity = int(item["grossQuantity"])
        print(f"{model_name}: {format_number(quantity)} | size=10")
    
    print("---")
    print(f"Total Cost: ${total_cost:.2f} | size=11 color=gray")
    print(f"Resets in {days_left} days | size=11 color=gray")
    print("---")
    print("View on GitHub | href=https://github.com/settings/copilot/features")
    print("Refresh | refresh=true")
