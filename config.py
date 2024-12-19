import os
from dotenv import load_dotenv


def load_connection_details():
    load_dotenv()
    return {
        # DNAC connection details
        "dnac_host": os.getenv("DNAC_HOST", "localhost"),
        "dnac_username": os.getenv("DNAC_USERNAME", "user"),
        "dnac_password": os.getenv("DNAC_PASSWORD", ""),
    }
