from motor.motor_asyncio import AsyncIOMotorClient

url = "mongodb+srv://admin:admin@cluster0.dlwa67t.mongodb.net/?appName=Cluster0"

client = AsyncIOMotorClient(url, tlsAllowInvalidCertificates=True)
database = client['DB']
collection_HR = database['HR']
collection_users = database['users']
collection_leave = database['leave']