import time
import subprocess
import random
from datetime import datetime

FILE_NAME = "data.txt"
BRANCH = "main"

# Random mətnlər
RANDOM_TEXTS = [
    "Hello world 🚀",
    "Bug fixed!",
    "New update coming soon",
    "Random thought of the day",
    "Python is awesome 🐍",
    "Auto commit in progress...",
    "Another line added",
    "Keep pushing forward 💪",
    "Coding mode ON 🔥",
    "Small change, big impact"
]

def run_git_command(command):
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Error running: {command}")

def generate_random_text():
    text = random.choice(RANDOM_TEXTS)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{timestamp} - {text}"

def append_to_file():
    with open(FILE_NAME, "a", encoding="utf-8") as f:
        f.write(generate_random_text() + "\n")

def git_push():
    run_git_command("git add .")
    run_git_command(f'git commit -m "Auto: {generate_random_text()}"')
    run_git_command(f"git push origin {BRANCH}")

print("Random Auto Push Bot started...")

while True:
    append_to_file()
    git_push()
    time.sleep(1)  # 2-15 saniyə arası random interval