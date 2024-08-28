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

# Duplicate the Cities collection into Randomised_Cities with random values
# Only needs to be run once
# duplicate_and_randomize_collection('Cities', 'Randomised_Cities')

if "Cities_Opt_1" not in collist:
    #Create collection if not already existing
    Cities_Opt_1 = db["Cities_Opt_1"]

if "Cities_Opt_2" not in collist:
    #Create collection if not already existing
    Cities_Opt_2 = db["Cities_Opt_2"]

if "Cities_Opt_3" not in collist:
    #Create collection if not already existing
    Cities_Opt_3 = db["Cities_Opt_3"]

if "Cities_Opt_4" not in collist:
    #Create collection if not already existing
    Cities_Opt_4 = db["Cities_Opt_4"]

if "Cities_Opt_5" not in collist:
    #Create collection if not already existing
    Cities_Opt_5 = db["Cities_Opt_5"]

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






