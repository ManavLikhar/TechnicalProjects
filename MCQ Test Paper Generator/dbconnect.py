from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGO_URL"), tlsAllowInvalidCertificates=True)
db = client["GenAI_Internship"]
collection = db["Interns"]
users_collection = db["Users"]

__all__ = ["client", "db", "collection", "users_collection"]