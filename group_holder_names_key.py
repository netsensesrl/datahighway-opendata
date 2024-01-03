import json
import os
import requests

def get_geonames_id(place_name, user_id):
    username = 'pruned'+ str(user_id)
    base_url = 'http://api.geonames.org/searchJSON'

    if "Comune" in place_name or "comune" in place_name or "Città metropolitana" in place_name or "Citta' metropolitana" in place_name:
        params = {
            'q': place_name,
            'maxRows': 3,
            'username': username,
            'featureCode': 'P',
            'country': 'IT'
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        if 'geonames' in data and len(data['geonames']) > 0:
            for entry in data['geonames']:
                if entry.get('fcl') == 'P' and entry.get('fcode').startswith('PPLA'):
                    return entry['geonameId']
            return None
        else:
            return None
    else:
        params = {
            'q': place_name,
            'maxRows': 10,
            'username': username,
            'featureCode': 'A',
            'country': 'IT'
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if 'geonames' in data and len(data['geonames']) > 0:
            for entry in data['geonames']:
                if entry.get('fcl') == 'A' and entry.get('fcode').startswith('ADM'):
                    return entry['geonameId']
            return None
        else:
            return None

holder_names_key = {}

def check_hl(folder):
    count = 0
    user_id = 0
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        with open(path, 'r') as file:
            content = json.load(file)
            for i in range(100):
                if "result" in content and i < len(content["result"]) and "extras" in content["result"][i]:
                    for key in content["result"][i]["extras"]:
                        if key.get("key") == "holder_name":
                            holder_name_key = key["value"]
                            if holder_name_key not in holder_names_key:
                                holder_names_key[holder_name_key] = ""
    
    for holder_name_key in holder_names_key:
        if count>800:
            user_id = user_id+1
            count=0
        geoname_id = get_geonames_id(holder_name_key, user_id)
        count = count+1

        if geoname_id:
            print(f"Place: {holder_name_key}, Geoname ID: {geoname_id}")
            holder_names_key[holder_name_key] = str(geoname_id)
        else:
            print(f"Geoname ID non trovato per {holder_name_key}")

check_hl('json')
check_hl('no_geo')

with open('./var/holder_names_key.py', 'w', encoding='utf-8') as file:
    file.write('holder_names_key = ')
    json.dump(holder_names_key, file, indent=4, ensure_ascii=False)
