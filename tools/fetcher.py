import requests
import sys

def get_cloudspaces(vco, customer, jwt):
    url = f"https://{vco}/api/1/customers/{customer}/cloudspaces"
    headers = {
        "Authorization": f"Bearer {jwt}"
    }

    response = requests.get(url, headers=headers)


    if response.status_code != 200:
        print(f"Failed to fetch cloudspaces: {response.status_code}, {response.text}")
        return

    return response.json()

def get_vms(vco, customer, jwt, cloudspace_id):
    url = f"https://{vco}/api/1/customers/{customer}/cloudspaces/{cloudspace_id}/vms?include_deleted=false&only_deleted=false&include_connected=false&exclude_internal=false"
    headers = {
        "Authorization": f"Bearer {jwt}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 400:
        print(f"Failed to fetch cloudspace with id: {cloudspace_id}.")
        sys.exit()

    elif response.status_code != 200:
        print(f"Failed to fetch virtual machines: {response.status_code}, {response.text}")
        return

    return response.json()
