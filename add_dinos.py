import openai
from azure.cosmos import CosmosClient, PartitionKey, exceptions
import os
import configparser
import re

# Read config file
config = configparser.ConfigParser()
config.read(r'C:\Users\ericm\OneDrive\Documents\Data Engineering Projects\DinoDB\DinoDB\config.ini')

# OpenAI API setup
openai.api_key = config.get('openai', 'api_key')

# Azure Cosmos DB setup
url = config.get('cosmosdb', 'url')
key = config.get('cosmosdb', 'key')
client = CosmosClient(url, credential=key)
database_name = config.get('cosmosdb', 'database')
container_name = config.get('cosmosdb', 'container')

database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

# List of dinosaurs to add to the database (MUST BE LOWER CASE WITHOUT SPECIAL CHARACTERS EXLUDING '-')
dinosaurs = ['carnotaurus', 'stegosaurus', 'allosaurus'] 

for dinosaur in dinosaurs:
    # Generate fun fact with OpenAI API
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=f"Tell me between 5 to 10 fun facts about {dinosaur}. Output the facts as a single coherent paragraph. The audience is 8-12 year old's.",
      temperature=0.5,
      max_tokens=400
    )
    
    facts = response.choices[0].text.strip().split('\n')

    # If the first fact is empty or not a fact, remove it
    if not facts[0]:
        facts = facts[1:]

    facts = [fact for fact in facts if fact]


    # Create an item (JSON document) to be stored in Cosmos DB
    item = {
        'id': 'DINO'+str(dinosaur),  
        'dinosaur': dinosaur,
        'fun_facts': facts
    }

    try:
        # Store the item in the database
        container.upsert_item(item)
        print(f'Successfully inserted fun fact for {dinosaur}')
        print(facts)
    except:
        print(f'Failed to insert fun fact for {dinosaur}')