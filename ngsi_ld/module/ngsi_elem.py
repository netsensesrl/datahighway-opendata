
def elem_form_osm(entity_type, entity_hash, element):
    ngsi_ld_elem = {
        "@context": [
            "https://raw.githubusercontent.com/netsensesrl/datahighway-opendata/main/ngsi_ld/context.jsonld",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context-v1.7.jsonld"
            ],
        "id": "urn:ngsi-ld:"+entity_type+":"+entity_hash,
        "type": entity_type
    }

    tags = element["tags"]
    
    for key, value in tags.items():
        if value is not None:
            ngsi_ld_elem[key] = {
                "type": "Property",
                "value": value
            }
    
    if element.get("lat") is not None:
        ngsi_ld_elem["lat"] = {
            "type": "Property",
            "value": element["lat"]
        }
    if element.get("lon") is not None:
        ngsi_ld_elem["lon"] = {
            "type": "Property",
            "value": element["lon"]
        }
        
    return ngsi_ld_elem
