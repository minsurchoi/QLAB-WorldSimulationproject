import pymongo
import json
import sys
import os
from pymongo import MongoClient, InsertOne
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


client = pymongo.MongoClient(r"mongodb+srv://minsurchoi:Minsur2003@cluster0.fbawjgk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

uri = "mongodb+srv://minsurchoi:Minsur2003@cluster0.fbawjgk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
db = client.QLAB
collection = db.Cities

#clear database to update any file changes 

collection.drop()

requesting = []

def city_add(city_name):
    city_path = "/Users/minsurchoi/Desktop/QLAB/project/Cities/" + city_name + ".json"
    with open(city_path) as f:
        myDict = json.load(f)
        requesting.append(InsertOne(myDict))

directory = '/Users/minsurchoi/Desktop/QLAB/project/Cities'
 
for filename in os.scandir(directory):
    if filename.is_file() and filename.name.endswith('.json'):
        city_name = os.path.splitext(filename.name)[0] 
        city_add(city_name)

result = collection.bulk_write(requesting)
client.close()                                                  