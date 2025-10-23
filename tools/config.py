import os
import re
import sys
import json
import base64

CONFIG_DIR = os.path.expanduser("~/.config/ws-cli")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

class Config:
    def __init__(self):
        check_config() 
        self.load_config()


    def load_config(self) -> str | None:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            self.jwt = data.get("jwt")
            self.vco = data.get("vco")
            self.customer = data.get("customer")

def check_config():
    if not os.path.exists(CONFIG_FILE):
        print("Please create a config using: ws config set_token <<JWT>>")
        sys.exit()

def get_jwt_payload(jwt_token):
    # Convert JWT to decoded python dict
    header, payload, signature = jwt_token.split('.')
    padded_payload = payload + '=' * (-len(payload) % 4)
    decoded_bytes = base64.urlsafe_b64decode(padded_payload)
    decoded_json = decoded_bytes.decode('utf-8')
    payload =  json.loads(decoded_json)

    # Grab the VCO
    vco = payload['azp'].replace("-",".")

    # Grab the customers
    data = payload['scope']
    pattern = re.compile(r"^user:memberof:[^.]+\.customers\.[^.]+$")
    filtered = [line for line in data if pattern.match(line)]
    customers = [line.rsplit('.', 1)[-1] for line in filtered]
    
    return vco, customers

def create_config(jwt):
    """ (Re)create configuration """

    vco, customers = get_jwt_payload(jwt)
    customer = customers[0]

    print(f"Defaulting {customer} out of customers: {customers}")
    
    config = {
        "jwt": jwt,
        "vco": vco,
        "customer": customer
    }
    
    # Create file
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
    os.chmod(CONFIG_FILE, 0o600)

    print(f"(Re)generated config file at {CONFIG_FILE}")

def set_customer(_, args):
    check_config()

    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    config['customer'] = args.customer

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
    print(f"Set customer to {args.customer}")

