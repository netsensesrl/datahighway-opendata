import requests
import json
import pandas as pd
import time
import signal
import sys

def save_to_properties(offset):
    data_to_save = {
        "offset": offset
    }
    with open("properties.json", "w") as json_file:
        json.dump(data_to_save, json_file)

def load_from_properties():
    try:
        with open("properties.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {"offset": 0, "server_errors": 0}

def signal_handler(sig, frame):
    print("\nCTRL+C pressed. Saving current offset to 'properties.json'.")
    save_to_properties(offset)
    sys.exit(0)

total_requests = 67529
completed_requests = 0
start_time = time.time()

properties = load_from_properties()
offset = properties["offset"]
end_of_data=0

if offset < 0:
    print("Start index not valid.")
else:
    signal.signal(signal.SIGINT, signal_handler)

    while(end_of_data==0):
        completed_requests = offset
        print(offset)
        ids = requests.get('https://dati.gov.it/opendata/api/3/action/current_package_list_with_resources?limit=100&offset=' + str(offset))
        completion_percentage = (completed_requests / total_requests) * 100
        if ids.status_code == 200:
            raw = ids.text
            if("resources" in raw):
                entry_json = ids.json()
                with open('./json/' + str(int(offset/100)) + '.json', 'w') as en:
                    json.dump(entry_json, en)
                    print(f"[{completion_percentage:.2f}%] dumped")
                save_to_properties(offset)
                offset=offset+100
            else:
                print("end of data")
                end_of_data=1
        else:
            print(ids.status_code)
    save_to_properties(offset)
    print("Done.")
