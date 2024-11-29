import json
import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning

# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Load environment variables from the .env file (if present)
load_dotenv()

# DNAC connection details
DNAC_HOST = os.getenv("DNAC_HOST", "localhost")
DNAC_USERNAME = os.getenv("DNAC_USERNAME", "user")
DNAC_PASSWORD = os.getenv("DNAC_PASSWORD")


class DNACClient:
    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint
        self.headers = {"content-type": "application/json"}
        self.token = self.get_token()

    def get_token(self):
        self.auth_api = "/dna/system/api/v1/auth/token"
        self.url = f"https://{DNAC_HOST}{self.auth_api}"
        resp = requests.post(
            self.url,
            auth=HTTPBasicAuth(username=DNAC_USERNAME, password=DNAC_PASSWORD),
            headers=self.headers,
            verify=False,
        )
        return resp.json()["Token"]

    def refresh_token(self):
        self.token = self.get_token()

    def get_data(self, offset=1, limit=10):
        all_data = []
        while True:
            url = (
                f"https://{DNAC_HOST}{self.api_endpoint}?offset={offset}&limit={limit}"
            )
            headers = {"x-auth-token": self.token}
            with requests.get(url, headers=headers, verify=False) as response:
                try:
                    response.raise_for_status()
                    data = response.json()
                    all_data.extend(data["response"])
                    if len(data["response"]) < limit:
                        break
                    offset += limit
                except requests.exceptions.HTTPError as e:
                    if response.status_code == 401:  # Unauthorized, token expired
                        self.refresh_token()
                        continue
                    else:
                        raise e
        return all_data


if __name__ == "__main__":

    # Print the list of all network devices
    # One at the time in a compact way

    network_device_client = DNACClient("/dna/intent/api/v1/network-device")
    network_device_data = network_device_client.get_data()
    for item in network_device_data:
        event = json.dumps(item, indent=None, separators=(",", ":"))
        print(event)
