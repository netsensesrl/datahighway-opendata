import requests

def check(entity_type, entity_id):
    reqUrl = "http://localhost:1026/ngsi-ld/v1/entities?type=\""+entity_type+"\"&q=id==\""+entity_id+"\""
    print(reqUrl)

    headersList = {
     "Accept": "*/*",
    }


    response = requests.request("GET", reqUrl, headers=headersList)

    return response.text