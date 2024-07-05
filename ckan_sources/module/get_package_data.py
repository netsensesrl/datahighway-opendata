import requests
import json
import logging
import time

logging.basicConfig(level=logging.INFO)

def fetch_package_id(name, cl_url, mode):
    package_search_url = f'{cl_url}/api/3/action/package_show?id={name}'
    retries = 0
    package_response = None
    while retries < 600:
        try:
            package_response = requests.get(package_search_url, timeout=60)
            package_response.raise_for_status()
        except requests.exceptions.Timeout:
            logging.warning(f"Timeout error fetching data for {name}. Retrying...")
            retries += 1
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data for {name}: {e}")
            retries += 1
            time.sleep(1)
        else:
            break
    if package_response and package_response.status_code == 200:
        package_json = package_response.json()
        try:
            if package_json["result"]["type"]!="harvest":#
                if package_json["result"]["holder_name"]!="None":
                    if package_json["result"]["holder_name"] == "Comune di Catania" and mode==0:
                        return None
                    result = package_json
                    return result["result"]
                else:
                    logging.error(f"No holder_name in {name}")
                    return None
            else:
                logging.warning(f"Harvest data: {name}")
                return None
        except Exception as e:
            logging.error(e)
            return None
    return None

def fetch_package_data(name, cl_url, mode):
    package_search_url = f'{cl_url}/api/3/action/package_search?q=name:"{name}"'
    retries = 0
    package_response = None
    while retries < 10:
        try:
            package_response = requests.get(package_search_url, timeout=60)
            package_response.raise_for_status()
        except requests.exceptions.Timeout:
            logging.warning(f"Timeout error fetching data for {name}. Retrying...")
            retries += 1
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data for {name}: {e}")
            break
        except requests.exceptions.ConnectionError as ce:
            logging.error(f"Connection error: {ce}")
            break
        else:
            break
    if package_response.status_code == 200:
        package_json = package_response.json()
        if package_json["result"]["count"] == 0:
            logging.warning(f"{name} not found. Trying with id API")
            fetch_package_id(name, cl_url, mode)
        else:
            result = package_json["result"]["results"]
            if result[0]["holder_name"] == "Comune di Catania" and mode==0:
                return None
            return result[0]
    else:
        logging.error(package_response.status_code)
        return None