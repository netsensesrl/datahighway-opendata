import requests
import json

def add(entity):
    reqUrl = "http://localhost:1026/ngsi-ld/v1/entities/"

    headersList = {
    "Content-Type": "application/ld+json" 
    }
    payload = json.dumps(entity)
    
    response = requests.request("POST", reqUrl, data=payload,  headers=headersList)
    print(response.text)