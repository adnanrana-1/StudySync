import logging
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

logger = logging.getLogger(__name__)

class MongoDBDatabase:
    client: AsyncIOMotorClient = None
    db = None

    def connect_to_database(self):
        logger.info("Initializing Async Motor driver instance pool...")
        self.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            maxPoolSize=50,
            minPoolSize=10
        )
        self.db = self.client[settings.DATABASE_NAME]
        logger.info("MongoDB cluster engine channel established.")

    def close_database_connection(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB cluster pooling successfully terminated.")

db_manager = MongoDBDatabase()

async def get_database():
    return db_manager.db
