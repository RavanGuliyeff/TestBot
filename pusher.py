#!/usr/bin/env python3

import os
import subprocess
import time
from datetime import datetime
import sys

# UTF-8 fix (Windows üçün)
sys.stdout.reconfigure(encoding='utf-8')

# Configuration
README_PATH = "README.md"
COMMIT_MESSAGE_PREFIX = "Auto-update README"
UPDATE_INTERVAL = 10  # saniyə (1 yox, 10 daha təhlükəsizdir)

def run_git_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def update_readme():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if os.path.exists(README_PATH):
        with open(README_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = "# Auto-Updated README\n\n"

    updated_marker = "Last updated:"
    lines = content.split('\n')

    updated = False
    for i, line in enumerate(lines):
        if updated_marker in line:
            lines[i] = f"{updated_marker} {timestamp}"
            updated = True
            break

    if not updated:
        lines.append(f"\n{updated_marker} {timestamp}")

    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"[OK] README updated at {timestamp}")


def commit_and_push():
    status = run_git_command("git status --porcelain")

    if not status:
        print("[INFO] No changes to commit")
        return

    if run_git_command(f"git add {README_PATH}") is not None:
        print("[OK] Changes staged")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"{COMMIT_MESSAGE_PREFIX} - {timestamp}"

    if run_git_command(f'git commit -m "{commit_msg}"') is not None:
        print(f"[OK] Committed: {commit_msg}")

    if run_git_command("git push") is not None:
        print("[OK] Pushed to GitHub")
    else:
        print("[ERROR] Push failed")


def main():
    print("Starting auto-commit README updater...")
    print(f"Update interval: {UPDATE_INTERVAL} seconds")
    print("Press Ctrl+C to stop\n")

    if run_git_command("git rev-parse --git-dir") is None:
        print("[ERROR] Not a git repository!")
        return

    try:
        while True:
            print(f"\n--- Cycle at {datetime.now().strftime('%H:%M:%S')} ---")

            update_readme()
            commit_and_push()

            print(f"[WAIT] Sleeping {UPDATE_INTERVAL} sec...")
            time.sleep(UPDATE_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()