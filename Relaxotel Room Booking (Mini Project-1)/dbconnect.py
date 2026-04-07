from motor.motor_asyncio import AsyncIOMotorClient

url = "mongodb+srv://admin:admin@cluster0.dlwa67t.mongodb.net/?appName=Cluster0"

client = AsyncIOMotorClient(url, tlsAllowInvalidCertificates=True)
db = client["relaxotel_db"]
booking_collection = db["bookings"]
room_collection = db["rooms"]
user_collection = db["users"]