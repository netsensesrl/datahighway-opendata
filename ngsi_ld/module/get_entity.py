import requests

def get_ent(entity_id):
    reqUrl = f"http://localhost:1026/ngsi-ld/v1/entities/{entity_id}/"

    response = requests.request("GET", reqUrl)

    entity_list = response.json()["typeList"]
    return entity_list