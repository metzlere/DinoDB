from azure.cosmos import CosmosClient, PartitionKey, exceptions
import os
import configparser
from gtts import gTTS
import re

# Read config file
config = configparser.ConfigParser()
config.read(r'C:\Users\ericm\OneDrive\Documents\Data Engineering Projects\DinoDB\DinoDB\config.ini')


# Azure Cosmos DB setup
url = config.get('cosmosdb', 'url')
key = config.get('cosmosdb', 'key')
client = CosmosClient(url, credential=key)
database_name = config.get('cosmosdb', 'database')
container_name = config.get('cosmosdb', 'container')

database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

# Query the database for all items
query = "SELECT * FROM c"
items = list(container.query_items(
    query=query,
    enable_cross_partition_query=True
))

# Establish base directory
base_dir = r'C:\Users\ericm\OneDrive\Documents\Data Engineering Projects\DinoDB\audio_files'

# Create a directory for each dinosaur and save a fun fact as an mp3 file
for item in items:
    dinosaur_name = item['dinosaur']
    fun_facts = item['fun_facts']

    dir_path = os.path.join(base_dir, dinosaur_name)
    os.makedirs(dir_path, exist_ok=True)

    for i, fact in enumerate(fun_facts, start=1):
        fact = re.sub(r'\d+\.\s', '', fact)
        tts = gTTS(fact)
        file_path = os.path.join(dir_path, f'{dinosaur_name}_fun_fact_{i}.mp3')
        tts.save(file_path)