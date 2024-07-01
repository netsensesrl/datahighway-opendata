import json

def get_context():
    with open("./var/context.jsonld", 'r') as file:
        data = json.load(file)
        return data