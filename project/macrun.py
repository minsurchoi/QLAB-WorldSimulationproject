import pymongo
import json
import sys
import certifi

from pymongo import MongoClient, InsertOne
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, render_template

client = pymongo.MongoClient(r"mongodb+srv://minsurchoi:Minsur2003@cluster0.fbawjgk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
app = Flask('QLAB', template_folder='templates')

uri = "mongodb+srv://minsurchoi:Minsur2003@cluster0.fbawjgk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.route('/')
def index():
    db = client["QLAB"]
    cities_collection = db["Cities"]
    cities = cities_collection.find().sort("Name", pymongo.ASCENDING)
    latitude_array = []
    longitude_array = []
    names_array = []

    for city_document in cities:
        if "Name" in city_document:
            name = city_document["Name"]
            names_array.append(name)
            
            if "co-ordinates" in city_document:
                latitude = city_document["co-ordinates"]["latitude"]
                longitude = city_document["co-ordinates"]["longitude"]
                longitude_array.append(longitude)
                latitude_array.append(latitude)

            
            
    return render_template('index.j2', len = len(latitude_array),latitude_array = latitude_array, longitude_array = longitude_array, names_array = names_array)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

client.close()                                                  


