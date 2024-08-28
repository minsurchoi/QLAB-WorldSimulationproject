import re 
from openai import OpenAI
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

YOUR_API_KEY = "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"

chatGPT_client = OpenAI(
    api_key = "sk-proj-ZZjiW4jlVRQkMPai26ZLT3BlbkFJzxIRVIaR5g96gz57Xk3y"
)

client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

def get_response(message):
    response = client.chat.completions.create(
        model='llama-3-sonar-large-32k-online',
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an artificial intelligence assistant and you offer help on a database of cities holding the population history, co-ordinates of the settlement, and trade data."
                ),
            },
            {"role": "user", "content": message}
        ]
    )
    # Access the content directly from the response object
    return response.choices[0].message.content

#Implement an algorithm to maybe detect existing constraint descriptions and add into db if seemingly new

def add_constraint_desc(text):
    
    target_collection = db["GPT_constraints"]

    # If number and dot detected, add text if not * character up to the next instances of * characters as title
    # Strip whitespace then add from : until next instance of a number.

     # Split the text into lines
    lines = text.split('\n')
    
    title = ""
    description = ""
    constraint_number = 0

    for line in lines:
        # Check if the line starts with a number followed by a dot
        if re.match(r'^\d+\.', line):
            # If we have a previous constraint, add it to the database
            if title and description:
                document = {
                    "title": title.strip(),
                    "description": description.strip()
                }
                target_collection.insert_one(document)

            # Reset for the new constraint
            constraint_number += 1
            title = ""
            description = ""

            # Extract the title (text between the number and the first ':')
            title_match = re.search(r'^\d+\.\s*\*\*(.*?)\*\*:', line)
            if title_match:
                title = title_match.group(1)

            # Add the rest of the line to the description
            description += re.sub(r'^\d+\.\s*\*\*.*?\*\*:\s*', '', line) + " "
        else:
            # Add non-numbered lines to the description
            description += line.strip() + " "

    # Add the last constraint
    if title and description:
        document = {
            "title": title.strip(),
            "description": description.strip()
        }
        target_collection.insert_one(document)

query = "Create descriptions of logical constraints to verify realism on the dataset in an exhaustive manner. No other information is provided other than the amount and category of trade by year, population, and co-ordinates. Assume all data is normalised and values are non negative and in a consistent format, therefore ignore these as constraints. Make this list as extensive as possible - one example is a gradual increase in trade over time, implemented as each 10 year average must be greater than the last."
result = get_response(query)
print(result)

#Needs ran once until repeated check algorithm implemented 
#If accurate, create function for GPT to convert each constraint as part of a Julia objective
#add_constraint_desc(result)
