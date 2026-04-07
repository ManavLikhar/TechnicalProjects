from user_model import User
from dbconnect import user_collection
from bson import ObjectId
from bcrypt import hashpw, gensalt, checkpw
from utils import create_access_token, decode_access_token

SECRET_KEY = "Lock"  # In a real app, this should be a secure secret key

# def hash_password(password: str) -> str:
#     return hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# def verify_password(password: str, hashed_password: str) -> bool:
#     return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Register User
async def register_user(user: User, response):
    try:
        # Hash the password before storing it in the database
        hashed_password = hashpw(user.password.encode("utf-8"), gensalt()).decode("utf-8")
        user_data = {"name": user.name, "email": user.email, "password": hashed_password}
        result = await user_collection.insert_one(user_data)
        return {"message": "User registered successfully", "user_id": str(result.inserted_id)}
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}
    
# Find the user by email
# Verify the password
# If Login  is successful, create a JWT token and return it to the client
async def login_user(email: str, password: str, response):
    try:
        user = await user_collection.find_one({"email": email})
        if user and checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
            token_data = {"user_id": str(user["_id"])}
            secret_key = "Lock"  # In a real app, this should be a secure secret key
            token = create_access_token(token_data, secret_key)
            return {"message": "Login successful", "token": token}
        else:
            response.status_code = 401
            return {"message": "Invalid email or password"}
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}