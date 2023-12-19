import json
import os
import requests
from module.geo_requests import g_request

folder = 'json'

json_prune = {"results" : []}
count = 0
req_count = 0

for filename in os.listdir(folder):
    path = os.path.join(folder, filename)
    with open(path, 'r') as file:
        content = json.load(file)
        for i in range (100):
            spatial = "null"
            spatial_uri = "null"
            geo_name = "null"
            temp_geo_name = "null"
            holder_name_key = "null"
            geo_term = "null"
            for key in content["result"][i]["extras"]:
                if req_count > 900:
                        print("account switch... " + str(count+1))
                        count = count+1
                        req_count = 0 
                if(key.get("key")=="spatial_uri"):
                    spatial_uri = key.get("value")
                    req_count=req_count+1
                    try:
                        if("geonames" in spatial_uri):
                            geoid = spatial_uri.split("/")[3]
                            geo_data = g_request(geoid, count, 1)
                            spatial = geo_data['spatial']
                            temp_geo_name = geo_data['temp_geo_name']
                            geo_name = geo_data['geo_name']
                            geo_term = geo_data['geo_term']
                    except Exception as e: 
                        print(e)
                if(key.get("key")=="Coordinate Spaziali"):
                    spatial = key["value"]
                    try:
                        spatial_json = json.loads(spatial)
                        spatial = spatial_json["coordinates"]
                    except:
                        spatial = key["value"]
                        spatial = spatial["coordinates"]
                if(key.get("key")=="holder_name"):
                    holder_name_key = key["value"]
                if(key.get("key")=="spatial" and spatial==''):
                    try:
                        spatial = json.loads(key.get("value"))
                        spatial = spatial.get("coordinates")
                    except:
                        continue
            if(spatial=="null"):
                req_count=req_count+1
                try: #Per evitare Geodati gov, al momento
                    holder_name = content["result"][i]["holder_name"].replace(" ", "+")
                    geo_data = g_request(holder_name_key, count, 2)
                    spatial = geo_data['spatial']
                    temp_geo_name = geo_data['temp_geo_name']
                    geo_name = geo_data['geo_name']
                    geo_id=geo_data["geo_id"]
                    spatial_uri = "https://www.geonames.org/"+ str(geo_data['geo_id'])
                    geo_term = geo_data['geo_term']
                except:
                    pass
            if(spatial_uri=="null"):
                req_count=req_count+1
                try:
                    holder_name = content["result"][i]["holder_name"].replace(" ", "+")
                    geo_data = g_request(holder_name, count, 2)
                    if(spatial=="null"):
                        spatial = geo_data['spatial']
                    temp_geo_name = geo_data['temp_geo_name']
                    geo_name = geo_data['geo_name']
                    geo_id=geo_data["geo_id"]
                    spatial_uri = "https://www.geonames.org/"+ str(geo_data['geo_id'])
                    geo_term = geo_data['geo_term']
                except:
                    pass
            if geo_name=="null":
                geo_name = temp_geo_name           
            data_to_save = {
                "id": content["result"][i]["id"],
                "holder_name" : content["result"][i]["holder_name"],
                "holder_name_key" : holder_name_key,
                "geo_name" : geo_name,
                "spatial" : spatial,
                "spatial_uri" : spatial_uri,
                "geoname_query_term" : geo_term
            }
            json_prune["results"].append(data_to_save)

        with open('./prune/'+filename.replace(".json", '')+"_pruned.json", 'w') as output:
            json.dump(json_prune, output, indent=2)
            json_prune = {"results" : []}
                    
