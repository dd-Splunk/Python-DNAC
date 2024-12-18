#!/bin/bash
echo "Initialize the Catalyst add-on"

BASE_URL="https://${SPLUNK_HOST}:8089/servicesNS/-/TA_cisco_catalyst"
DNAC_HOST="https://${DNAC_HOST}"
DNAC_USER="DNAC_Administrator"
INDEX_NAME="dnac"

echo "Create specific index: ${INDEX_NAME}"
curl -k -s -u ${SPLUNK_USERNAME}:${SPLUNK_PASSWORD} \
    -L "${BASE_URL}/data/indexes" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Accept: application/json" \
    -d "datatype=event" \
    -d "name=${INDEX_NAME}" \
    -d "coldPath=\$SPLUNK_DB/${INDEX_NAME}/colddb" \
    -d "homePath=\$SPLUNK_DB/${INDEX_NAME}/db" \
    -d "maxTotalDataSizeMB=512000" \
    -d "thawedPath=\$SPLUNK_DB/${INDEX_NAME}/thaweddb"

echo "Disable ssl_verify in settings"
curl -k -s -u ${SPLUNK_USERNAME}:${SPLUNK_PASSWORD} \
    -L "${BASE_URL}/TA_cisco_catalyst_settings/additional_parameters" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Accept: application/json" \
    -d "verify_ssl=FALSE"

echo "Create account"
curl -k -s -u ${SPLUNK_USERNAME}:${SPLUNK_PASSWORD} \
    -L "${BASE_URL}/TA_cisco_catalyst_account" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Accept: application/json" \
    -d "name=${DNAC_USER}" \
    -d "username=${DNAC_USERNAME}" \
    -d "password=${DNAC_PASSWORD}" \
    -d "copy_account_name=${DNAC_PASSWORD}"

echo "Create Client Health"
curl -k -s -u ${SPLUNK_USERNAME}:${SPLUNK_PASSWORD} \
    -L "${BASE_URL}/TA_cisco_catalyst_cisco_catalyst_dnac_clienthealth" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Accept: application/json" \
    -d "name=dnac_client_health" \
    -d "interval=300" \
    -d "index=${INDEX_NAME}" \
    -d "cisco_dna_center_host=${DNAC_HOST}" \
    -d "cisco_dna_center_account=${DNAC_USER}"

echo "Create Compliance"
curl -k -s -u ${SPLUNK_USERNAME}:${SPLUNK_PASSWORD} \
    -L "${BASE_URL}/TA_cisco_catalyst_cisco_catalyst_dnac_compliance" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Accept: application/json" \
    -d "name=dnac_compliance" \
    -d "interval=900" \
    -d "index=${INDEX_NAME}" \
    -d "cisco_dna_center_host=${DNAC_HOST}" \
    -d "cisco_dna_center_account=${DNAC_USER}"

echo "Create Device Health"
curl -k -s -u ${SPLUNK_USERNAME}:${SPLUNK_PASSWORD} \
    -L "${BASE_URL}/TA_cisco_catalyst_cisco_catalyst_dnac_devicehealth" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Accept: application/json" \
    -d "name=dnac_device_health" \
    -d "interval=300" \
    -d "index=${INDEX_NAME}" \
    -d "cisco_dna_center_host=${DNAC_HOST}" \
    -d "cisco_dna_center_account=${DNAC_USER}"

echo "Create Issue"
curl -k -s -u ${SPLUNK_USERNAME}:${SPLUNK_PASSWORD} \
    -L "${BASE_URL}/TA_cisco_catalyst_cisco_catalyst_dnac_issue" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Accept: application/json" \
    -d "name=dnac_issue" \
    -d "interval=900" \
    -d "index=${INDEX_NAME}" \
    -d "cisco_dna_center_host=${DNAC_HOST}" \
    -d "cisco_dna_center_account=${DNAC_USER}"

echo "Create Network Health"
curl -k -s -u ${SPLUNK_USERNAME}:${SPLUNK_PASSWORD} \
    -L "${BASE_URL}/TA_cisco_catalyst_cisco_catalyst_dnac_networkhealth" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Accept: application/json" \
    -d "name=dnac_network_health" \
    -d "interval=300" \
    -d "index=${INDEX_NAME}" \
    -d "cisco_dna_center_host=${DNAC_HOST}" \
    -d "cisco_dna_center_account=${DNAC_USER}"

echo "Create Security Advisory"
curl -k -s -u ${SPLUNK_USERNAME}:${SPLUNK_PASSWORD} \
    -L "${BASE_URL}/TA_cisco_catalyst_cisco_catalyst_dnac_securityadvisory" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Accept: application/json" \
    -d "name=dnac_security_advisory" \
    -d "interval=3600" \
    -d "index=${INDEX_NAME}" \
    -d "cisco_dna_center_host=${DNAC_HOST}" \
    -d "cisco_dna_center_account=${DNAC_USER}"

echo "Add-On initialized"
