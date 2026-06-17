"""Auto-update module for GitHub-hosted project."""
import os
import sys
import subprocess
import requests
from modules.ui import print_info, print_error, print_success, print_warning

LOCAL_VERSION_FILE = 'version.txt'
REMOTE_VERSION_URL = 'https://raw.githubusercontent.com/yourusername/USMAN-TikTok-Analyzer/main/version.txt'  # Replace with your repo

def get_local_version():
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, 'r') as f:
            return f.read().strip()
    return "0.0.0"

def get_remote_version():
    try:
        resp = requests.get(REMOTE_VERSION_URL, timeout=5)
        if resp.status_code == 200:
            return resp.text.strip()
        else:
            return None
    except requests.RequestException:
        return None

def check_for_updates():
    local = get_local_version()
    remote = get_remote_version()
    if remote and remote != local:
        print_warning(f"Update available: {local} → {remote}")
        return True
    return False

def update_app():
    """Pull latest changes from GitHub if repository is a git clone."""
    if not os.path.isdir('.git'):
        print_error("Update failed: Not a git repository. Please re-clone the project.")
        return
    try:
        print_info("Checking for updates...")
        # Fetch latest
        subprocess.run(['git', 'fetch', 'origin'], check=True)
        # Check status
        result = subprocess.run(['git', 'status', '-uno'], capture_output=True, text=True)
        if 'Your branch is behind' in result.stdout:
            print_warning("New updates found. Pulling latest changes...")
            subprocess.run(['git', 'pull', 'origin', 'main'], check=True)
            print_success("Updated successfully! Please restart the app if necessary.")
        else:
            print_success("Already up-to-date.")
    except subprocess.CalledProcessError as e:
        print_error(f"Update failed: {e}")
    except Exception as e:
        print_error(f"Unexpected error: {e}")
