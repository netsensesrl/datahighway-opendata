import os
import json
from module.get_ngsild_context import get_context
from module.update_ngsild_context import update_context
from module.hashing import hash_string
from module.entity_type_json import gpt_req
from module.ngsi_elem import elem_form_osm
from module.check_ent_broker import check
from module.add_entity import add
from module.get_duplicates import get_dup
from module.gpt_check_dup import check_dup
from module.gpt_create_entity import create_entity

resources_folder = "./resources"

def main():
    ngsild_context = get_context()
    entities_list = []
    for filename in os.listdir(resources_folder):
        if filename.endswith(".json"):
            json_file = os.path.join(resources_folder, filename)
            json_data = json.load(open(json_file))
            if filename.startswith("osm"):
                json_data_gpt = json_data.get("elements", [])[:20]
                response = gpt_req(json_data_gpt, json_file, ngsild_context)
                for element in json_data["elements"]:
                    entity = str(element["id"])+str(element["lat"])+str(element["lon"])+element["tags"].get("addr:street")
                    entity_hash = hash_string(entity)
                    if (check(response[0], entity_hash) == "[]"):
                        ngsi_elem = elem_form_osm(response[0], entity_hash, element)
                        add(ngsi_elem)
            else: #ckan case
                json_data_gpt = json_data[:20] #get first 20 elements of the json file
                response = gpt_req(json_data_gpt, json_file, ngsild_context)
                update_context(response[1])
                ngsild_context = get_context()
                for element in json_data:
                    ngsi_ld_entity = json.loads(create_entity(str(element), response[0], ngsild_context))
                    add(ngsi_ld_entity)
        elif filename.endswith(".geojson"):
            geojson_file = os.path.join(resources_folder, filename)
            geojson_data = json.load(open(geojson_file))
            response = gpt_req(geojson_data, geojson_file, ngsild_context)
            update_context(response[1])
            ngsild_context = get_context()
            ngsi_ld_entity = json.loads(create_entity(str(geojson_data), response[0], ngsild_context))
            add(ngsi_ld_entity)
    
        
    gpt_response = check_dup(get_dup())
    print(gpt_response)
    for line in gpt_response.split("\n"):
        #transform the string ["<entity1>", "<entity2>"] into a list of entities
        entities = line[1:-1].split(", ")
        

if __name__ == "__main__":
    main()
