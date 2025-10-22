import os
import sys
import json
import base64

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

def load_user():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        vco = data.get("vco")
        customer = data.get("customer")
    if not vco:
        print("Please set your vco")
        sys.exit()
    elif not customer:
        print("Please set your customer")
        sys.exit()
    else:
        return vco, customer

def decode_jwt_payload(jwt_token):
    # Split the JWT into its three parts
    header, payload, signature = jwt_token.split('.')

    # JWTs use base64url encoding (replace - and _)
    # Also pad with '=' if needed
    padded_payload = payload + '=' * (-len(payload) % 4)

    # Decode from Base64URL
    decoded_bytes = base64.urlsafe_b64decode(padded_payload)
    decoded_json = decoded_bytes.decode('utf-8')

    # Convert JSON string to a Python dict
    return json.loads(decoded_json)

    # Config
    payload = decode_jwt_payload(user.jwt)
    print(json.dumps(payload, indent=4))

