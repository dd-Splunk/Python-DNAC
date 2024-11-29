import os
from dotenv import load_dotenv
import requests
import time
from urllib3.exceptions import InsecureRequestWarning

# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

load_dotenv()


class SplunkHEC:
    def __init__(self, splunk_host, splunk_port):

        self.splunk_host = splunk_host
        self.splunk_port = splunk_port
        self.splunk_username = os.getenv("SPLUNK_USERNAME")
        self.splunk_password = os.getenv("SPLUNK_PASSWORD")
        self.hec_token = os.getenv("SPLUNK_HEC_TOKEN")

    def send_event(self, event_data, index="main", source=None, sourcetype=None):
        """
        Sends an event to the Splunk HTTP Event Collector.

        Args:
            event_data (dict): The event data to be sent.
            index (str): The Splunk index to send the event to (default is 'main').
            source (str): The source of the event (optional).
            sourcetype (str): The source type of the event (optional).
        """
        url = f"https://{self.splunk_host}:{self.splunk_port}/services/collector/event"
        headers = {
            "Authorization": f"Splunk {self.hec_token}",
            "Content-Type": "application/json",
        }
        data = {"event": event_data, "index": index, "time": int(time.time())}

        if source:
            data["source"] = source
        if sourcetype:
            data["sourcetype"] = sourcetype

        try:
            response = requests.post(url, headers=headers, json=data, verify=False)
            response.raise_for_status()
            print(f"Event sent successfully to Splunk: {event_data}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending event to Splunk: {e}")


if __name__ == "__main__":
    splunk_hec = SplunkHEC(splunk_host="localhost", splunk_port="8088")
    event_data = {
        "event": "something happened",
        "details": {"severity": "INFO", "category": ["foo", "bar"]},
    }

    splunk_hec.send_event(event_data, source="python-app", sourcetype="python-app-logs")
