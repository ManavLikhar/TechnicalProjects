from motor.motor_asyncio import AsyncIOMotorClient

url = "mongodb+srv://admin:admin@cluster0.dlwa67t.mongodb.net/?appName=Cluster0"

client = AsyncIOMotorClient(url, tlsAllowInvalidCertificates=True)
database = client["inventory_db"]
users_collection = database["users"]
products_collection = database["products"]
orders_collection = database["orders"]