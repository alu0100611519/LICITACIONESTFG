from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import os
from dotenv import load_dotenv

## cargamos la  variables de entorno
load_dotenv()



class DatabaseConfig:
    def __init__(self, uri: str = None, db_name: str = None):
        self._uri = uri or os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        self._db_name = db_name or os.getenv("MONGO_DB_NAME", "miBasedeDatos")
        self._client: AsyncIOMotorClient = None
        self._db: AsyncIOMotorDatabase = None

    def connect(self):
        self._client = AsyncIOMotorClient(self._uri)
        self._db = self._client[self._db_name]

    def get_database(self) -> AsyncIOMotorDatabase:
        if not self._db:
            raise Exception("Database connection has not been established. Call connect() first.")
        return self._db

    def close(self):
        if self._client:
            self._client.close()


