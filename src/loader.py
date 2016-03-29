from pymongo import mongo_client


def load_instructions(filename):
    client = mongo_client.MongoClient()
    db = client.udaan
    with open(filename, "r") as file:
        content = file.read()
    db.instrunctions.remove()
    db.instrunctions.insert({"instruction": content})
