import json
import yaml
from openai import OpenAI
from module.get_types import get_ngsild_types

nl_description_system = """You are an expert data analyst helping us extract relevant informations for made a knowledge graph.
#the task is to get all elements and return a description of the entity"""

entity_retrieve_system = """You are an expert data analyst helping us extract relevant informations for made a knowledge graph.
#the task is to get the description of an entity and return the one or more entity type for each row,like this example:
    
    Entitytype: <entitytype>

#find the entity type analyzing the properties/values of the entity. 
#Entity type cannot be plural
#If you cannot extract the entity type from properties/values or different types of entities can be extracted, use the filename for extract the best entity type
#Entity type cannot have spaces. Use camelCase if needed
#Renturn entity type that is a word or a combination of words that make sense in natural language
#Do not write explanations
#The geometry of an element is not considered as an entity, but as a property of the entity.
#Translate the entity type in english if it is in italian or other languages
           
"""

context_retrieve_system = """You are an expert data-analyst. Generate a json-ld @context from input text provided, using exist schema.org vocabs. Identify fields that can be add as context.
            #You receive an input text and a pre-existing @context, you have to add the fields of the input text to the @context that are not already present in the @context.
            #Return a @context, based on json-ld standard defined in w3.org, @context structure and fields as shown in example:

                        {
                            "@context":
                            {
                                "<
                                
                                ">: "https://schema.org/<value1>",
                                "<propertyname2>": "https://schema.org/<value2>"
                                .
                                .
                                .
                            }
                        }
            
            RULESET:
                #DO NOT write details and explainations, return only @context structure. Be sure that schema.org vocab exists
                #DO NOT annidate the context, return only the fields and their values
                #DO NOT change Key names of properties, defining the @context fields. DO NOT change them in other languages
                #Number of fields in the @context must be equal to the number of properties in the input text
                #You must consider only the key and not the value, to retrieve the various fields of the @context. Consider the field of EntityType for define the context of the EntityType
                #DO NOT insert values for "id" and "type" fields, they are already defined in the json-ld standard
                #Each property in a file must have a unique IRI
                #Return only one @context, do not return multiple @context"""


file_prompt = """#This a part from a CSV document. You receive an input with following content:
                filename: <filename>
                content: <content>
"""

entity_prompt = """#This a description of an entity and a list of available entities just made, like this example:
                    <entityDescription>
                    ['<entity1>', '<entity2>', '<entity3>', '<entity4>', '<entity5>',...]
                #If you see that the entity is present in the list, return the entity type as one of the best from properties/values of the entity."""

row_entity_prompt = '''This is a entity and a row from a JSON document. You receive an input with following content:
            Entitytype: <entitytype>
            json: <jsonelement>
            '''

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
       
def gpt_req(json_data, json_file, ngsild_context):

    with open("./var/gpt_key.yaml", 'r') as file:
        data = yaml.safe_load(file)
        api_key = data['key']

    types = get_ngsild_types()

    client = OpenAI(api_key=api_key)
    
    response = run_gpt4_turbo(client, nl_description_system, file_prompt, f"filename: {json_file}\ncontent: {json_data}\n")

    entity = run_gpt4_turbo(client, entity_retrieve_system, entity_prompt, response+str(types))
    
    context = run_gpt4_turbo(client, context_retrieve_system, file_prompt+str(ngsild_context), f"filename: {json_file}\ncontent: {json_data}\n")

    return entity.split(": ")[1], context