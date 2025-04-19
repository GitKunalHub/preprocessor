import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Azure File Storage
    AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=chatsee;AccountKey=voz5uIMJNTaFrqvk38g7TUNrzwcYiVeLNfXa9ltPMUixZh3xEz0Wl8gYgopLMWlU4TgzIIB0S2OJ+ASt8xp9kQ==;EndpointSuffix=core.windows.net"
    AZURE_FILE_SHARE_NAME = "chatsee-fs"
    AZURE_FILE_DIRECTORY = ""
    AZURE_BLOB_CONTAINER_NAME = "chatsee-data"
    # MongoDB
    # MONGO_USER = quote_plus(os.getenv("MONGODB_USER"))
    # MONGO_PASS = quote_plus(os.getenv("MONGODB_PASS"))
    # MONGO_HOST = os.getenv("MONGODB_HOST")
    # MONGO_PORT = os.getenv("MONGODB_PORT")
    # MONGO_AUTH_SOURCE = quote_plus(os.getenv("MONGODB_AUTH_SOURCE"))
    MONGODB_URI = (
        f"mongodb+srv://dbQH:kunal2001@clusterqh.pvbet.mongodb.net/"
    )
    MONGODB_DB = "tenant_ice_energy"
    MONGODB_COLLECTION = "scheduler_jobs"

    # RabbitMQ
    RABBITMQ_HOST = "20.244.24.210"
    RABBITMQ_USER = "chatsee"
    RABBITMQ_PASS = "chatsee_pro"
    RABBITMQ_PORT = "5672"
    REDIS_HOST = "redis-test"
    REDIS_PORT = 6379