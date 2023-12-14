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
    print(filename)
    with open(path, 'r') as file:
        content = json.load(file)
        for i in range (100):
            spatial = "null"
            spatial_uri = "null"
            geo_name = "null"
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
                            print(spatial)
                    except:
                        print("Error in " + filename + " result " + str(i))
                if(key.get("key")=="Coordinate Spaziali"):
                    spatial = key["value"]
                    spatial_json = json.loads(spatial)
                    spatial = spatial_json["coordinates"]
                    print(spatial)
                if(key.get("key")=="spatial" and spatial==''):
                    try:
                        spatial = json.loads(key.get("value"))
                        spatial = spatial.get("coordinates")
                        
                    except:
                        continue
            if(spatial=="null" or spatial_uri=="null"):
                try: #Per evitare Geodati gov, al momento
                    print(i)
                    if req_count == 900:
                        print("changing account... " + str(count+1))
                        count = count+1
                        req_count = 0 
                    holder_name = content["result"][i]["holder_name"].replace(" ", "+")
                    print(holder_name)
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
                    print(spatial)
                except:
                    pass
                    
            data_to_save = {
                "id": content["result"][i]["id"],
                "holder_name" : content["result"][i]["holder_name"],
                "geo_name" : geo_name,
                "spatial" : spatial,
                "spatial_uri" : spatial_uri
            }
            json_prune["results"].append(data_to_save)

        with open('./prune/'+filename.replace(".json", '')+"_pruned.json", 'w') as output:
            json.dump(json_prune, output, indent=2)
            json_prune = {"results" : []}
                    
