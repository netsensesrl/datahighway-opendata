import requests
from module.convert_bbox import c_bbox

def g_request(var, count, mode):
    try:
        geo_name = "null"
        geo_id = "null"
        if(mode == 1):
            r = requests.get("http://api.geonames.org/childrenJSON?formatted=true&geonameId="+var+"&username=pruned"+str(count)+"&style=full")
            geo_id = var
        if(mode == 2):
            if "Regione" in var:
                var = var.replace("Regione ", "")
            if "Comune di" in var:
                var = var.replace("Comune di ", "")
            r = requests.get("http://api.geonames.org/searchJSON?formatted=true&q="+var+"&maxRows=10&lang=es&username=pruned"+str(count)+"&style=full")
        r_json= r.json()
        spatial = c_bbox(r_json["geonames"][0]["bbox"]["east"], r_json["geonames"][0]["bbox"]["south"], r_json["geonames"][0]["bbox"]["north"], r_json["geonames"][0]["bbox"]["west"])
        temp_geo_name=r_json["geonames"][0]["asciiName"]
        geo_id = r_json["geonames"][0]["geonameId"]
        for key in r_json["geonames"][0]["alternateNames"]:
            if(key.get("lang")=="it"):
                geo_name = key.get("name")
        geo_data = {
            "spatial" : spatial,
            "temp_geo_name" : temp_geo_name,
            "geo_name" : geo_name,
            "geo_id" : geo_id
        }
    except Exception as e: 
        print(e)
    return geo_data