from typing import Optional, Dict, Any
from bson import ObjectId
import pymongo
from utils.config import Config

def fetch_agent_config(agent_id: str) -> dict:
    try:
        with pymongo.MongoClient(Config.MONGODB_URI) as client:
            db = client[Config.MONGODB_DB]
            collection = db[Config.MONGODB_COLLECTION]
            return collection.find_one({"_id": ObjectId(agent_id)}) or {}
    except Exception as e:
        import logging
        logging.getLogger("AzureInteractionsProcessor").error(f"MongoDB Error: {e}")
        return {}