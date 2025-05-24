from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI
from ANNIEMUSIC.logging import LOGGER

LOGGER(__name__).info("Connecting to your Mongo Database...")

try:
    _mongo_async_ = AsyncIOMotorClient(MONGO_DB_URI)
    mongodb = _mongo_async_.Annie  # Replace 'Annie' if your DB has a different name
    cardsdb = mongodb.cards        # Declare collection here if used frequently
    LOGGER(__name__).info("Connected to your Mongo Database.")
except Exception as e:
    LOGGER(__name__).error(f"Failed to connect to your Mongo Database: {e}")
    exit()
