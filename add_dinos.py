import openai
from azure.cosmos import CosmosClient, PartitionKey, exceptions
import os
import configparser

# Read config file
config = configparser.ConfigParser()
config.read('config.ini')

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

# List of dinosaurs to add to the database
dinosaurs = ['T-Rex', 'Triceratops', 'Velociraptor'] 

for dinosaur in dinosaurs:
    # Generate fun fact with OpenAI API
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=f"Tell me between 5 to 10 fun facts about {dinosaur}. The audience is 8-12 year old's",
      temperature=0.5,
      max_tokens=400
    )

    facts = response.choices[0].text.strip().split('\n')[1:]

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
    except:
        print(f'Failed to insert fun fact for {dinosaur}')