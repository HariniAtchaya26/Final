from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

client = AsyncIOMotorClient(MONGO_URL)

db = client["fastapi_app"]

# ✅ THESE NAMES MUST MATCH IMPORTS
users_collection = db["users"]
profiles_collection = db["profiles"]
