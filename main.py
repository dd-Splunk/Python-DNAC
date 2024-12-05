import json
from dnac_client import DNACClient, DNAC_HOST
from splunk_hec import SplunkHEC


def get_and_send_data(endpoint, splunk_hec, source, sourcetype):
    client = DNACClient(endpoint)
    data = client.get_data()
    splunk_hec.send_events_batch(data, source=source, sourcetype=sourcetype)


def main():
    # Create a HEC Connection
    splunk_hec = SplunkHEC(splunk_host="localhost", splunk_port="8088")

    # Call the individual APIs and send the results to Splunk
    get_and_send_data(
        "/dna/intent/api/v1/device-health",
        splunk_hec,
        DNAC_HOST,
        "cisco:dnac:devicehealth",
    )
    get_and_send_data(
        "/dna/intent/api/v1/client-health",
        splunk_hec,
        DNAC_HOST,
        "cisco:dnac:clienthealth",
    )
    get_and_send_data(
        "/dna/intent/api/v1/network-device",
        splunk_hec,
        DNAC_HOST,
        "cisco:dnac:networkhealth",
    )


if __name__ == "__main__":
    main()
