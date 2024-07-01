import requests
from collections import defaultdict

def get_ngsild_types():
    reqUrl = "http://localhost:1026/ngsi-ld/v1/types/"

    response = requests.request("GET", reqUrl)

    entity_list = response.json()["typeList"]
    return entity_list