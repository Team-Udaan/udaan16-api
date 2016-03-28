import sys
from pymongo import mongo_client


def load_instructions():
    client = mongo_client.MongoClient()
    db = client.udaan
    with open(sys.argv[1], "r") as file:
        content = file.read()
    db.instrunctions.remove()
    db.instrunctions.insert({"instruction": content})
