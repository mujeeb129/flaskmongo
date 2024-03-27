from pymongo import MongoClient
import os

class MongoDB(MongoClient):
    def __init__(self, db_name):
        super().__init__(
            host=os.getenv("MONGO_HOST", "localhost"),
            port=int(os.getenv("MONGO_PORT", 27017)),
            username=os.getenv("MONGO_USER", "mujeeb"),
            password=os.getenv("MONGO_PASSWORD", "qburst"),
        )
        self.db = self[db_name]

