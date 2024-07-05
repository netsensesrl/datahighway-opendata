import json
from module.geo_requests import g_request

def prune(missing_names):
    json_prune = {"results" : []}
    count_geo=0
    for result in missing_names["result"]:
        var_id = result["id"]
        spatial = "null"
        holder_name = result["holder_name"]
        holder_name_key = "null"
        tags = []
        groups = []
        for tag in result["tags"]:
            tags.append(tag["name"])
        for group in result["groups"]:
            groups.append(group["display_name"])
        for key in result["extras"]:
            if(key["key"]=="spatial"):
                try:
                    spatial_coords = json.loads(key.get("value"))
                    coordinates = spatial_coords.get("coordinates")
                    spatial = spatial.get("coordinates")
                except:
                    continue
            if(key.get("key")=="holder_name"):
                holder_name_key = key["value"]
        if holder_name_key=="null":
            try:
                holder_name_key = result["publisher_name"]
            except:
                pass
        try:
            geo_data = g_request(holder_name, holder_name_key)
            count_geo+=1
        except:
            holder_name_key = result["organization"]["title"]
            geo_data = g_request(holder_name, holder_name_key)
            count_geo+=1
        if(spatial=="null"):
            spatial=geo_data["spatial"]
        if(not geo_data["spatial"]):
            print(f"Error pruning {var_id} : {holder_name}")
        data_to_save = {
            "id": var_id,
            "holder_name" : holder_name,
            "holder_name_key" : holder_name_key,
            "spatial" : spatial,
            "spatial_uri" : geo_data["spatial_uri"],
            "tags" : tags,
            "groups" : groups
        }
        json_prune["results"].append(data_to_save)
    return (json_prune)
    