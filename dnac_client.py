import json
import requests
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning

# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class DNACClient:
    def __init__(self, dnac_connection, api_endpoint):
        self.dnac_host = dnac_connection["dnac_host"]
        self.dnac_username = dnac_connection["dnac_username"]
        self.dnac_password = dnac_connection["dnac_password"]
        self.api_endpoint = api_endpoint
        self.headers = {"content-type": "application/json"}
        self.token = self.get_token()

    def get_token(self):
        self.auth_api = "/dna/system/api/v1/auth/token"
        self.url = f"https://{self.dnac_host}{self.auth_api}"
        resp = requests.post(
            self.url,
            auth=HTTPBasicAuth(
                username=self.dnac_username, password=self.dnac_password
            ),
            headers=self.headers,
            verify=False,
        )
        return resp.json()["Token"]

    def refresh_token(self):
        self.token = self.get_token()

    def get_data(self, offset=1, limit=10):
        all_data = []
        while True:
            url = f"https://{self.dnac_host}{self.api_endpoint}?offset={offset}&limit={limit}"
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

    from config import load_connection_details

    # Print the list of all network devices
    # One at the time in a compact way

    dnac_connection = load_connection_details()

    network_device_client = DNACClient(dnac_connection, "/dna/intent/api/v1/network-device")
    network_device_data = network_device_client.get_data()
    for item in network_device_data:
        event = json.dumps(item, indent=None, separators=(",", ":"))
        print(event)
