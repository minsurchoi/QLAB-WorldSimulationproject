from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.QLAB
collist = db.list_collection_names()

# Verify the connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def reformat_cities_data(collection_to_reformat, outputted_collection):
    source_collection = db[collection_to_reformat]
    dest_collection = db[outputted_collection]
    
    # Clear the destination collection if it exists
    dest_collection.drop()
    
    for item in source_collection.find():

        if "_id" in item and isinstance(item["_id"], dict) and "Name" in item["_id"]:
            item["Name"] = item["_id"].pop("Name")
        
        if "Optimized_Trade" in item:
            item["Trade"] = item.pop("Optimized_Trade")
        
        if "Trade" in item:
            new_trade_data = {}
            for trade_type in ["Exports", "Imports"]:
                if trade_type in item["Trade"]:
                    for category, values in item["Trade"][trade_type].items():
                        for year, value in enumerate(values, start=1900):
                            # Had to convert year to string for MongoDB compatibility
                            year_str = str(year)
                            if year_str not in new_trade_data:
                                new_trade_data[year_str] = {"Exports": {}, "Imports": {}}
                            new_trade_data[year_str][trade_type][category] = value
            
            item["Trade"] = new_trade_data
        
        dest_collection.insert_one(item)
        print("Success")
    

reformat_cities_data("Cities_Opt_1","Restructured_Cities_Opt_1")
client.close()