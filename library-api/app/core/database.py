from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings 

class Database:
    client : AsyncIOMotorClient | None = None 
    db : AsyncIOMotorDatabase | None = None


database=Database()

async def connect_to_mongo() -> None:
    database.client = AsyncIOMotorClient(settings.MONGODB_URL)
    database.db = database.client[settings.DATABASE_NAME]

    await database.client.admin.command("ping")
    print(f"Connected to MongoDB - database: {settings.DATABASE_NAME}")

async def close_mongo_connection() -> None:
    if database.client is not None:
        database.client.close()
        print("MongoDB connection closed")

def get_database() -> AsyncIOMotorDatabase:
    if database.db is None:
        raise RuntimeError("Database not initialized. Call connect_to_mongo() first.")
    return database.db
