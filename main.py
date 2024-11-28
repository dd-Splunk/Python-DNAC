import json
import os
import requests
import sys
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


# Authentication
auth = (DNAC_USERNAME, DNAC_PASSWORD)
AUTH_API = "/dna/system/api/v1/auth/token"
url = f"https://{DNAC_HOST}{AUTH_API}"


headers = {"content-type": "application/json"}
resp = requests.post(
    url,
    auth=HTTPBasicAuth(username=DNAC_USERNAME, password=DNAC_PASSWORD),
    headers=headers,
    verify=False,
)
token = resp.json()["Token"]

# API endpoint
API_ENDPOINT = "/dna/intent/api/v1/device-health"

# Initialize variables
headers["x-auth-token"] = token
payload = None
offset = 1
limit = 10
all_devices = []

# Retrieve network devices using pagination
while True:
    # Construct the API request URL with pagination parameters
    url = f"https://{DNAC_HOST}{API_ENDPOINT}?offset={offset}&limit={limit}"
    # Make the API request
    with requests.get(url, headers=headers,data=payload, verify=False) as response:
        # Check the response status code
        # This will raise an exception if the status code is not in the 2xx range.
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Append the retrieved devices to the list
        all_devices.extend(data["response"])


        # Check if there are more devices to retrieve
        if len(data["response"]) < limit:
            break

        # Update the offset for the next page
        offset += limit

# Print the list of all network devices
# One a t the time in a compact way
for item in all_devices:
    event=json.dumps(item, indent=None, separators=(',', ':'))
    print(f"{event}\n")
