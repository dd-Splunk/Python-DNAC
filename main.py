from config import load_connection_details
from dnac_client import DNACClient
from splunk_hec import SplunkHEC


def get_and_send_data(dnac_connection, dnac_endpoint, splunk_hec, source, sourcetype):
    client = DNACClient(dnac_connection, dnac_endpoint)
    data = client.get_data()
    splunk_hec.send_events_batch(data, source=source, sourcetype=sourcetype)


def main():
    # Create a HEC Connection
    splunk_hec = SplunkHEC(splunk_host="localhost", splunk_port="8088")

    # Load DNAC details
    dnac_connection = load_connection_details()
    source = dnac_connection["dnac_host"]

    # Define the common base URL for the API calls
    base_url = "/dna/intent/api/v1"

    # Define the list of endpoints and their corresponding sourcetype
    endpoints = [
        (f"{base_url}/device-health", "cisco:dnac:devicehealth"),
        (f"{base_url}/client-health", "cisco:dnac:clienthealth"),
        (f"{base_url}/network-device", "cisco:dnac:networkhealth"),
        (f"{base_url}/compliance", "cisco:dnac:compliance")
    ]

    # Call the individual APIs and send the results to Splunk
    for endpoint, sourcetype in endpoints:
        get_and_send_data(dnac_connection, endpoint, splunk_hec, source, sourcetype)

if __name__ == "__main__":
    main()
