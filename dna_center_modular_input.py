#!/usr/bin/env python3
import sys
import json
import requests
from splunklib.modularinput import *

class DNACenterDeviceHealthInput(Script):
    def get_scheme(self):
        """
        Define the scheme for the modular input, specifying required configuration parameters
        """
        scheme = Scheme("dna_center_device_health")
        scheme.description = "Retrieve device health information from Cisco DNA Center"
        scheme.use_external_validation = True
        scheme.streaming_mode = Scheme.StreamingMode.XML

        # DNA Center API connection parameters
        scheme.add_argument(Argument(
            name="dna_center_url",
            title="DNA Center URL",
            description="Base URL for DNA Center API (e.g., https://dna.example.com)",
            required_on_create=True,
            required_on_edit=True
        ))
        scheme.add_argument(Argument(
            name="username",
            title="Username",
            description="DNA Center API username",
            required_on_create=True,
            required_on_edit=True
        ))
        scheme.add_argument(Argument(
            name="password",
            title="Password",
            description="DNA Center API password",
            required_on_create=True,
            required_on_edit=True,
            encrypted=True
        ))

        return scheme

    def validate_input(self, validation_definition):
        """
        Validate the input configuration before saving
        """
        # Extract configuration parameters
        dna_center_url = validation_definition.parameters.get("dna_center_url")
        username = validation_definition.parameters.get("username")
        password = validation_definition.parameters.get("password")

        # Perform a test API call to validate credentials
        try:
            # Create an authentication token
            auth_url = f"{dna_center_url}/dna/system/api/v1/auth/token"
            auth_response = requests.post(
                auth_url, 
                auth=(username, password), 
                verify=False  # Disable SSL verification for example (not recommended in production)
            )
            auth_response.raise_for_status()
        except Exception as e:
            # Raise a validation error if authentication fails
            raise ValueError(f"Authentication failed: {str(e)}")

    def stream_events(self, inputs, ew):
        """
        Stream device health events to Splunk
        """
        # Iterate through all input configurations
        for input_name, input_item in inputs.inputs.items():
            # Extract configuration parameters
            dna_center_url = input_item.get("dna_center_url")
            username = input_item.get("username")
            password = input_item.get("password")

            try:
                # Create an authentication token
                auth_url = f"{dna_center_url}/dna/system/api/v1/auth/token"
                auth_response = requests.post(
                    auth_url, 
                    auth=(username, password), 
                    verify=False  # Disable SSL verification for example (not recommended in production)
                )
                auth_token = auth_response.json().get("Token")

                # Fetch device health information
                device_health_url = f"{dna_center_url}/dna/intent/api/v1/device-health"
                headers = {
                    "X-Auth-Token": auth_token,
                    "Content-Type": "application/json"
                }
                
                device_health_response = requests.get(
                    device_health_url, 
                    headers=headers, 
                    verify=False  # Disable SSL verification for example (not recommended in production)
                )
                device_health_data = device_health_response.json()

                # Stream events to Splunk
                for device in device_health_data.get('response', []):
                    event = Event()
                    event.stanza = input_name
                    event.data = json.dumps(device)
                    ew.write_event(event)

            except Exception as e:
                # Log any errors
                ew.log("ERROR", f"Error retrieving DNA Center device health: {str(e)}")

if __name__ == '__main__':
    sys.exit(DNACenterDeviceHealthInput().run(sys.argv))
