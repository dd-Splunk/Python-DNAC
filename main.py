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

    # Call the individual APIs and send the results to Splunk
    get_and_send_data(
        dnac_connection,
        "/dna/intent/api/v1/device-health",
        splunk_hec,
        dnac_connection["dnac_host"],
        "cisco:dnac:devicehealth",
    )
    get_and_send_data(
        dnac_connection,
        "/dna/intent/api/v1/client-health",
        splunk_hec,
        dnac_connection["dnac_host"],
        "cisco:dnac:clienthealth",
    )
    get_and_send_data(
        dnac_connection,
        "/dna/intent/api/v1/network-device",
        splunk_hec,
        dnac_connection["dnac_host"],
        "cisco:dnac:networkhealth",
    )
    get_and_send_data(
        dnac_connection,
        "/dna/intent/api/v1/compliance",
        splunk_hec,
        dnac_connection["dnac_host"],
        "cisco:dnac:compliance",
    )


if __name__ == "__main__":
    main()
