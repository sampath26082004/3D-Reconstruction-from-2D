import os
from pymongo import MongoClient


def get_mongo_client() -> MongoClient:
    mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
    return MongoClient(mongo_uri)


def mongo_log_signup(doc: dict) -> None:
    try:
        client = get_mongo_client()
        db = client.get_database(os.getenv('MONGODB_DB', 'reconstruction'))
        db.user_events.insert_one(doc)
    except Exception:
        # Fail silently so auth flow continues even if Mongo is unavailable
        pass


def mongo_log_login(doc: dict) -> None:
    try:
        client = get_mongo_client()
        db = client.get_database(os.getenv('MONGODB_DB', 'reconstruction'))
        db.user_events.insert_one(doc)
    except Exception:
        pass





