# DNAC API

Authentication [reference](https://community.cisco.com/t5/networking-blogs/authenticating-rest-api-calls-to-dnac-getting-started/ba-p/3658058)

and also [here](https://developer.cisco.com/docs/dna-center/authentication-api/)

## Authentication

Need to create a local `.env` file with:

```bash
# DNAC connection details
DNAC_HOST = <IP address>
DNAC_USERNAME = <some username having enough READ privileges>
DNAC_PASSWORD = <and its password>
# Splunk Credentials
SPLUNK_USERNAME = <username>>
SPLUNK_PASSWORD = <password>
SPLUNK_HEC_TOKEN = <HEC token>
````

## Splunkbase apps required

- Cisco add-on (7538)
- Cisco App (7539)
- Config Explorer (4353)
