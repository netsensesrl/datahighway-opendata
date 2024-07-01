import requests
from module.get_types import get_ngsild_types

def get_dup():
    string_entities = ""
    entities_list = get_ngsild_types()

    headersList = {
        "Accept": "application/json",
        "Link": '<https://raw.githubusercontent.com/netsensesrl/datahighway-opendata/main/ngsi_ld/context.jsonld>;rel="http://www.w3.org/ns/jsonld#context";type="application/ld+json"'
    }

    for elem in entities_list:
        reqUrl = f"http://localhost:1026/ngsi-ld/v1/entities?type={elem}&limit=1000"

        response = requests.request("GET", reqUrl,  headers=headersList)

        json_data = response.json()
        json_extract=[]
        for entity in json_data:    
            try:
                if "Catania" in entity["address"]["value"]:
                    json_extract.append(entity)
            except Exception as e:
                try:
                    if entity["addr:city"]["value"]=="Catania":
                        json_extract.append(entity)
                except:
                    pass

        data = json_extract
        duplicates_ids = []
        
        for i, entity in enumerate(data):
            for j, other_entity in enumerate(data[i+1:], start=i+1):
                if abs(entity['lat']['value'] - other_entity['lat']['value']) <= 0.00003 and \
                (entity.get('lon') and other_entity.get('lon') and abs(entity['lon']['value'] - other_entity['lon']['value']) < 0.00003):
                    try:
                        #filter for lat and lon (about 3 meters of difference)
                        string_entities += f'["{entity["name"].get("value")}", "{other_entity["name"].get("value")}"]\n'
                    except Exception as e:
                        pass
    return string_entities
