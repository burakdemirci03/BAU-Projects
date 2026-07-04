from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGODB_URL") or os.getenv("MONGO_URL", "mongodb://localhost:27072")
DB_NAME = "crfms_db"

class Database:
    client: AsyncIOMotorClient = None
    
    def connect(self):
        self.client = AsyncIOMotorClient(MONGO_URL)

    def get_db(self):
        return self.client[DB_NAME]

    def close(self):
        if self.client:
            self.client.close()

db = Database()

async def get_database():
    return db.get_db()