import os
import sys
import json

CONFIG_DIR = os.path.expanduser("~/.ws-cli")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def save_token(token: str):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"jwt": token}, f)
    os.chmod(CONFIG_FILE, 0o600)  # only owner can read/write


def load_token() -> str | None:
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        jwt = data.get("jwt")
    if not jwt:
        print("Please set your JWT token: ws token \"YOUR TOKEN\"")
        sys.exit()

    return jwt
