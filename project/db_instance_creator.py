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

    for doc in documents:
        if 'Trade' in doc:
            randomize_trade(doc['Trade'])
        dst_collection.insert_one(doc)


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






