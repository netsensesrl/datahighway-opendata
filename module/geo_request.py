import json
from module.convert_bbox import c_bbox
from var.bbox import geonames_bbox
from var.bbox_keys import geonames_bbox_keys
from var.holder_names import holder_names
from var.holder_names_key import holder_names_key

def g_request(holder_name, holder_name_key):
    geo_data = {}
    if holder_name_key in geonames_bbox_keys:
        bbox = geonames_bbox_keys[holder_name_key]
        bbox_values = json.loads(bbox)
        geo_id = holder_names_key[holder_name_key]
        geo_term = holder_names_key
            
    else:
        try:
            bbox = geonames_bbox[holder_name]
            bbox_values = json.loads(bbox)
            geo_id = holder_names[holder_name]
            geo_term = holder_names
        except:
            bbox = geonames_bbox_keys[holder_name]
            bbox_values = json.loads(bbox)
            geo_id = holder_names_key[holder_name]
            geo_term = holder_name
    spatial = c_bbox(bbox_values["east"], bbox_values["south"], bbox_values["north"], bbox_values["west"])
    geo_data = {
        "spatial": spatial,
        "spatial_uri" : "https://www.geonames.org/" + geo_id
    }

    return geo_data
