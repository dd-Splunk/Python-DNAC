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
    dnac_host = dnac_connection["dnac_host"]

    # Define the list of endpoints and their corresponding source and sourcetype
    api_base = "/dna/intent/api/v1"
    endpoints = [
        (f"{api_base}/device-health", dnac_host, "cisco:dnac:devicehealth"),
        (f"{api_base}/client-health", dnac_host, "cisco:dnac:clienthealth"),
        (f"{api_base}/network-device", dnac_host, "cisco:dnac:networkhealth"),
        (f"{api_base}/compliance", dnac_host, "cisco:dnac:compliance"),
    ]

    # Call the individual APIs and send the results to Splunk
    for endpoint, source, sourcetype in endpoints:
        get_and_send_data(dnac_connection, endpoint, splunk_hec, source, sourcetype)


if __name__ == "__main__":
    main()
