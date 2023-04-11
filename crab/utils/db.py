import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


mongo_uri = f"mongodb+srv://{os.environ.get('MONGODB_USERNAME')}:\
    {os.environ.get('MONGODB_PASSWORD')}@cluster0.s8odi72.mongodb.net/?\
        retryWrites=true&w=majority"

client = MongoClient(mongo_uri)

db = client['crab']  # database name
sites = db['sites']  # collection name


def get_allowed_domains() -> list[str]:
    return []


def insert_data() -> None:
    data = {
        
    }