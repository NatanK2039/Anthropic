import os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "log.txt")

def log(text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {text}\n")