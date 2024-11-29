import json
from dnac_client import DNACClient, DNAC_HOST
from splunk_hec import SplunkHEC


def main():
    # Print the list of all network devices
    # One a t the time in a compact way

    # Create a HEC Connection
    splunk_hec = SplunkHEC(splunk_host="localhost", splunk_port="8088")

    # Call the individual APIs and send the results to Splunk
    device_health_client = DNACClient("/dna/intent/api/v1/device-health")
    device_health_data = device_health_client.get_data()

    for item in device_health_data:
        event = json.dumps(item, indent=None, separators=(",", ":"))
        splunk_hec.send_event(
            event, source=DNAC_HOST, sourcetype="cisco:dnac:device_health"
        )

    client_health_client = DNACClient("/dna/intent/api/v1/client-health")
    client_health_data = client_health_client.get_data()
    for item in client_health_data:
        event = json.dumps(item, indent=None, separators=(",", ":"))
        splunk_hec.send_event(
            event, source=DNAC_HOST, sourcetype="cisco:dnac:client_health"
        )

    network_device_client = DNACClient("/dna/intent/api/v1/network-device")
    network_device_data = network_device_client.get_data()
    for item in network_device_data:
        event = json.dumps(item, indent=None, separators=(",", ":"))
        splunk_hec.send_event(
            event, source=DNAC_HOST, sourcetype="cisco:dnac:network_devices"
        )


if __name__ == "__main__":
    main()
