import pymongo 
import json 
from pymongo import MongoClient, InsertOne
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

client = pymongo.MongoClient(r"mongodb+srv://minsurchoi:Minsur2003@cluster0.fbawjgk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

uri = "mongodb+srv://minsurchoi:Minsur2003@cluster0.fbawjgk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["QLAB"]
cities_collection = db["Cities"]
cities = cities_collection.find()
latitude_array = []
longitude_array = []

for city_document in cities:
    latitude = city_document["co-ordinates"]["latitude"]
    longitude = city_document["co-ordinates"]["longitude"]
            # Append the coordinates to the array as a list
    latitude_array.append(latitude)
    longitude_array.append(longitude)

    # Print the coordinates array
print(latitude_array)
print(longitude_array)
client.close()