import pymongo
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from utils.config import Config

scheduler = BackgroundScheduler(
    jobstores={
        'default': MongoDBJobStore(
            database=Config.MONGODB_DB,
            collection='scheduler_jobs',
            client=pymongo.MongoClient(Config.MONGODB_URI)
        )
    },
    timezone='UTC'
)