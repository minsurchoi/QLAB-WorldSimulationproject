import pymongo
import json
import logging
import io

from pymongo import MongoClient 
from pymongo.mongo_client import MongoClient
from flask import Flask, render_template, request
from bson import json_util
from flask import Flask, render_template, request, send_file



client = MongoClient('mongodb://localhost:27017/')
app = Flask(__name__, template_folder ='templates')
logging.basicConfig(level=logging.DEBUG)

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
    suggestion = request.get_data(as_text=True)  
    if suggestion:
        db = client["QLAB"]
        suggestions_collection = db["Suggestions"]
        suggestions_collection.insert_one({"suggestion": suggestion})
        return "Suggestion submitted successfully"
    else:
        return "No suggestion provided"
    
@app.route('/city/<city_name>')
def city_details(city_name):
    db = client["QLAB"]
    cities_collection = db["Cities"]
    city = cities_collection.find_one({"Name": city_name})
    if city:
        city_data = {
            "name": city.get("Name", "N/A"),
            "latitude": city.get("co-ordinates", {}).get("latitude", "N/A"),
            "longitude": city.get("co-ordinates", {}).get("longitude", "N/A"),
            "trade": city.get("Trade", "N/A")
        }
        return render_template('city_details.j2', city=city_data)
    else:
        return "City not found", 404
    
@app.route('/city/<city_name>/<int:year>')
def city_trade_details(city_name, year):
    db = client["QLAB"]
    cities_collection = db["Cities"]
    city = cities_collection.find_one({"Name": city_name})
    if city and str(year) in city.get("Trade", {}):
        city_data = {
            "name": city["Name"],
            "year": year,
            "trade": city["Trade"][str(year)]
        }
        return render_template('city_trade_details.j2', city=city_data)
    else:
        return "Trade data not found", 404

@app.route('/city/<city_name>/randomised/<int:year>')
def randomised_city_trade_details(city_name, year):
    db = client["QLAB"]
    randomised_cities_collection = db["Randomised_Cities"]
    city = randomised_cities_collection.find_one({"Name": city_name})
    if city and str(year) in city.get("Trade", {}):
        city_data = {
            "name": city["Name"],
            "year": year,
            "trade": city["Trade"][str(year)],
            "is_randomised": True
        }
        return render_template('city_trade_details.j2', city=city_data)
    else:
        return "Randomised trade data not found", 404
    
@app.route('/download_full_database')
def download_full_database():
    db = client["QLAB"]
    
    database_dict = {}
    
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        database_dict[collection_name] = list(collection.find())
    
    database_json = json.dumps(database_dict, default=json_util.default)
    
    file_obj = io.BytesIO(database_json.encode('utf-8'))
 
    return send_file(
        file_obj,
        mimetype='application/json',
        as_attachment=True,
        download_name='QLAB_full_database.json'
    )   
     
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

client.close()                                                  


