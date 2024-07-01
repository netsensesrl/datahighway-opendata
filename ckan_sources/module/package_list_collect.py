import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

def pl_collect(url):
    for i in range(60):
        try:
            package_list = requests.get(url, timeout=60).json()
            return package_list["result"]
        except requests.exceptions.Timeout:
            logging.warning(f"Timeout error fetching data for {url}. Retrying...")
        except Exception as e:
            logging.error(f"Exception: {e}")
    return None