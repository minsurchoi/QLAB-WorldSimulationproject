import pymongo
import json
import sys
import certifi
import os

from pymongo import MongoClient, InsertOne
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, render_template, request

client = MongoClient('mongodb://localhost:27017/')
app = Flask(__name__, template_folder ='templates')

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
    
    city_data = []
    for city_document in cities:
        if "Name" in city_document and "co-ordinates" in city_document and "Trade" in city_document:
            city_data.append({
                "name": city_document["Name"],
                "latitude": city_document["co-ordinates"]["latitude"],
                "longitude": city_document["co-ordinates"]["longitude"],
                "trade": city_document["Trade"]
            })
    
    return render_template('index.j2', cities=city_data)
    
@app.route('/submit_suggestion', methods=['POST'])
def submit_suggestion():
    suggestion = request.get_data(as_text=True)  # Get the raw text suggestion
    if suggestion:
        db = client["QLAB"]
        suggestions_collection = db["Suggestions"]
        suggestions_collection.insert_one({"suggestion": suggestion})
        return "Suggestion submitted successfully"
    else:
        return "No suggestion provided"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

client.close()                                                  


