import pymongo
import json
from pymongo import MongoClient, InsertOne
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


client = pymongo.MongoClient(r"mongodb+srv://minsurchoi:Minsur2003@cluster0.fbawjgk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

uri = "mongodb+srv://minsurchoi:Minsur2003@cluster0.fbawjgk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
db = client.Cities
collection = db.Abuja
requesting = []

with open(r"C:\Users\choim\OneDrive\Desktop\QLAB\project\Cities\Abuja.json") as f:
    myDict = json.load(f)
    requesting.append(InsertOne(myDict))

result = collection.bulk_write(requesting)
client.close()



