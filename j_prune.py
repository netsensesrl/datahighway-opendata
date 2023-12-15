import json
import os
import requests
import time
from convert_bbox import c_bbox

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
            holder_name_key = "null"
            for key in content["result"][i]["extras"]:
                if(key.get("key")=="spatial_uri"):
                    spatial_uri = key.get("value")
                    if req_count == 900:
                        print("account switch... " + str(count+1))
                        count = count+1
                        req_count = 0 
                    try:
                        if("geonames" in spatial_uri):
                            geoid = spatial_uri.split("/")[3]
                            r = requests.get("http://api.geonames.org/childrenJSON?formatted=true&geonameId="+geoid+"&username=pruned"+str(count)+"&style=full")
                            req_count=req_count+1
                            r_json= r.json()
                            east = r_json["geonames"][0]["bbox"]["east"]
                            south = r_json["geonames"][0]["bbox"]["south"]
                            north = r_json["geonames"][0]["bbox"]["north"]
                            west = r_json["geonames"][0]["bbox"]["west"]
                            spatial = c_bbox(east, south, north, west)
                            geo_name=r_json["geonames"][0]["asciiName"]
                    except:
                        print("Error in " + filename + " result " + str(i))
                if(key.get("key")=="Coordinate Spaziali"):
                    spatial = key["value"]
                    spatial_json = json.loads(spatial)
                    spatial = spatial_json["coordinates"]
                if(key.get("key")=="holder_name"):
                    holder_name_key = key["value"]
                if(key.get("key")=="spatial" and spatial==''):
                    try:
                        spatial = json.loads(key.get("value"))
                        spatial = spatial.get("coordinates")
                    except:
                        continue
            if(spatial=="null" or spatial_uri=="null"):
                try: #Per evitare Geodati gov, al momento
                    if req_count == 900:
                        print("account switch... " + str(count+1))
                        count = count+1
                        req_count = 0 
                    holder_name = content["result"][i]["holder_name"].replace(" ", "+")
                    r = requests.get("http://api.geonames.org/searchJSON?formatted=true&q="+holder_name+"&maxRows=10&lang=es&username=pruned"+str(count)+"&style=full")
                    req_count=req_count+1
                    r_json= r.json()
                    east = r_json["geonames"][0]["bbox"]["east"]
                    south = r_json["geonames"][0]["bbox"]["south"]
                    north = r_json["geonames"][0]["bbox"]["north"]
                    west = r_json["geonames"][0]["bbox"]["west"]
                    spatial = c_bbox(east, south, north, west)
                    geo_name=r_json["geonames"][0]["asciiName"]
                    spatial_uri = "https://www.geonames.org/"+ str(r_json["geonames"][0]["geonameId"])
                except:
                    pass
                    
            data_to_save = {
                "id": content["result"][i]["id"],
                "holder_name" : content["result"][i]["holder_name"],
                "holder_name_key" : holder_name_key,
                "geo_name" : geo_name,
                "spatial" : spatial,
                "spatial_uri" : spatial_uri
            }
            json_prune["results"].append(data_to_save)

        with open('./prune/'+filename.replace(".json", '')+"_pruned.json", 'w') as output:
            json.dump(json_prune, output, indent=2)
            json_prune = {"results" : []}
                    
