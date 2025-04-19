from typing import Optional, Dict, Any
from bson import ObjectId
import pymongo
from utils.config import Config

def fetch_agent_config(agent_id: str) -> dict:
    try:
        with pymongo.MongoClient(Config.MONGODB_URI) as client:
            db = client[Config.MONGODB_DB]
            collection = db["agents"]
            print("DEBUG: Fetching agent configuration")
            print(f"DEBUG: Agent ID: {agent_id}")
            return collection.find_one({"agent_id": agent_id})
    except Exception as e:
        print(f"ERROR: MongoDB Error: {e}")
        return {}