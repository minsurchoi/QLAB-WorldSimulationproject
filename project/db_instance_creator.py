import random
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.QLAB

# Verify the connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# List the existing collections
collist = db.list_collection_names()

# Create the 'Cities_Randomised' collection if it doesn't exist
if "Cities_Randomised" not in collist:
    Cities_Randomised = db["Cities_Randomised"]

random.seed(1)  # Initialize the random seed

# Function to duplicate and randomize the values in a collection
def duplicate_and_randomize_collection(src_collection_name, dst_collection_name):
    src_collection = db[src_collection_name]
    dst_collection = db[dst_collection_name]
    dst_collection.drop()  # Drop the destination collection if it exists

    # Retrieve all documents from the source collection
    documents = list(src_collection.find())

    # Function to randomize the values in the "Trade" section
    def randomize_trade(trade):
        for year, categories in trade.items():
            for category, items in categories.items():
                for item in items:
                    items[item] = random.randint(1, 10000)

    # Insert documents into the destination collection with randomized "Trade" values
    for doc in documents:
        if 'Trade' in doc:
            randomize_trade(doc['Trade'])
        dst_collection.insert_one(doc)


def create_error_term_table():
    # Access the original and optimized collections
    Opt_cities = db["Cities_Opt_1"]  # Optimized cities table
    Org_cities = db["Cities"]  # Original cities table
    
    # Ensure the error terms table exists
    if "Cities_Error_Terms" not in db.list_collection_names():
        Cities_Error_Terms = db["Cities_Error_Terms"]
    else:
        Cities_Error_Terms = db["Cities_Error_Terms"]
    
    # Iterate through each city in the original table
    for city in Org_cities.find():
        # Get the city's name and trade data from the original table
        city_name = city.get("Name")
        original_trade_data = city.get("Trade", {})
        
        # Find the corresponding city in the optimized table
        optimized_city = Opt_cities.find_one({"Name": city_name})
        
        if optimized_city:
            optimized_trade_data = optimized_city.get("Trade", {})
            error_term_data = {"Imports": {}, "Exports": {}}
            
            # Calculate error terms for Imports
            for year, year_data in original_trade_data.items():
                for category, values in year_data.get("Imports", {}).items():
                    optimized_values = optimized_trade_data.get("Imports", {}).get(category, [])
                    if category not in error_term_data["Imports"]:
                        error_term_data["Imports"][category] = {}
                    error_term_data["Imports"][category][year] = calculate_error_terms(values, optimized_values)
            
            # Calculate error terms for Exports
            for year, year_data in original_trade_data.items():
                for category, values in year_data.get("Exports", {}).items():
                    optimized_values = optimized_trade_data.get("Exports", {}).get(category, [])
                    if category not in error_term_data["Exports"]:
                        error_term_data["Exports"][category] = {}
                    error_term_data["Exports"][category][year] = calculate_error_terms(values, optimized_values)
            
            # Insert the city's name and calculated error terms into the error terms table
            Cities_Error_Terms.insert_one({
                "Name": city_name,
                "Trade_Error_Terms": error_term_data
            })
            print(f"Processed city: {city_name}")
        else:
            print(f"No optimized data found for city: {city_name}")

# Method to each category to an array 
def category_to_array(category):
    #Find the difference between each value in array 
    



# Ensure the Constraints collection exists and add constraints if they don't already exist
if "Constraints" not in collist:
    Constraints = db["Constraints"]

    constraint1 = {"Name" : "Gradual Increase Constraint",
         "Expression" : """
         for i in 11:n
             @constraint(model, sum(adjusted_imports[i-9:i]) / 10 >= sum(adjusted_imports[i-10:i-1]) / 10)
         end
         """}

    constraint2 = {"Name" : "Trade Balance Constraint",
         "Expression" : "@constraint(sum(adjusted_imports) == sum(adjusted_exports))"}

    Constraints.insert_one(constraint1)
    Constraints.insert_one(constraint2)

    print("Success")

if "GPT_constraints" not in collist:
    GPT_constraints = db["GPT_constraints"]

create_error_term_table()






