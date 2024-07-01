import yaml
from openai import OpenAI

ngsild_system = """You are an expert data-analyst. Generate an NGSI-LD entity starting from csv row provided, using exist schema.org vocabs. Identify fields that represent the type of entity, properties and define the corrispondent NGSI-LD entity or entities and fill.
        An NGSI-LD entity is a JSON object that represents a real-world entity, such as a person, a building, a device, a sensor, etc. The entity is described by a set of properties, each of which has a name and a value. The entity also has a type, which defines the set of properties that the entity can have. Here is an example of an NGSI-LD entity structure:
        {
            "@context": [
            <contextfile>,
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context-v1.7.jsonld"
            ],
            "id": "urn:ngsi-ld:<entitytype>:<entitynumber>",
            "type": <entitytype>,
            "<propertyname1>": {
                "type": "Property",
                "value": "<rowvalue1>"
            },
            "<propertyname1>": {
                "type": "Property",
                "value": "<rowvalue2>"
            },
            .
            .
            .
        }
        #DO NOT write details and explainations, return only the NGSI-LD entity structure
        #DO NOT change Key names and values of properties, defining the NGSI-LD entity
        #DO NOT omit properties and values, define all the properties and values of the entity
        #if a value is null, insert an empty string
        """

prompt = """#This is a line from a document. You receive an input with entity type and a context file to use in the <contextfile> field during the creation of the entity."""

def run_gpt4_turbo(client, system, prompt, paragraph):
        completion = client.chat.completions.create(
        model="gpt-4-turbo",
        temperature=0.7,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt + paragraph}
        ]
        )

        print(completion.choices[0].message.content)
        return completion.choices[0].message.content

def create_entity(elem, entity_type, ngsild_context):
    with open("./var/gpt_key.yaml", 'r') as file:
        data = yaml.safe_load(file)
        api_key = data['key']

    client = OpenAI(api_key=api_key)
    
    entity = run_gpt4_turbo(client, ngsild_system, prompt, elem+entity_type+str(ngsild_context))
    return entity


