import json

def update_context(ngsild_context):
    ngsild_context = json.loads(ngsild_context)
    with open('./var/context.jsonld', 'r') as file:
        existing_context = json.load(file)
        
        for field in ngsild_context["@context"]:
            if field not in existing_context["@context"]:
                sub_context = {field: ngsild_context["@context"][field]}
                existing_context["@context"].update(sub_context)

        with open('./var/context.jsonld', 'w') as file:
            json.dump(existing_context, file, indent=2)