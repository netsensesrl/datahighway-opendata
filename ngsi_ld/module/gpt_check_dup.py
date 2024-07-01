import yaml
from openai import OpenAI

with open("./var/gpt_key.yaml", 'r') as file:
        data = yaml.safe_load(file)
        api_key = data['key']
        
client = OpenAI(api_key=api_key)

prompt= """Please, in doing so, respect the following ruleset:

RULESET:
    Rule 0: evaluate names that are in the same list

    Rule 1: Ignore evident spelling errors, punctuation, capitalization. 

    Rule 2: If you find places or service names, ignore them for the evaluation.

    Rule 3: If two or more entities contains the same name as a place it does not mean that they are necessarily the same entities

    Rule 4: If two or more entities contains the same name as a service it does not mean that they are necessarily the same entities
    
    Example of wrong answer:
    1. **Galdieri Rent Catania Aeroporto Fontanarossa** and **Maggiore Car Rental, Catania Fontanarossa Airport**
    - Explanation: Both entities mention car rental services specifically at Catania Fontanarossa Airport. They are similar in terms of location and service type.
    
    Wrong because the answer is based on location and service type, which are not considered (Rule 2)

    Return an answer if entities are identical for sure.

    Here's an example of the input and output:
        input:
            ["<entity1>", "<entity2>"]
            ["<entity3>", "<entity4>"]
            ["<entity5>", "<entity6>"]
            .
            .
            .
        
        output:
            ["<entity1>", "<entity2>"]
            .
            .
            .
        
        
    """

def check_dup(elem):
    completion = client.chat.completions.create(
      model="gpt-4",
      messages=[
        {"role": "system", "content": "From this list of entities, find entities that refer to the same thing, based on similarity of their names, and return the results as in the example."},
        {"role": "user", "content": prompt + elem}
      ],
      temperature=0.1,
    )

    return completion.choices[0].message.content
