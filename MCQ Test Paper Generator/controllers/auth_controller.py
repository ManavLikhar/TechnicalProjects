from models.auth_model import UserRegister, UserLogin
from dbconnect import users_collection
from bcrypt import hashpw, gensalt, checkpw
from utils import create_access_token, SECRET_KEY
from fastapi import Response

async def register_user(user: UserRegister, response: Response):
    try:
        existing_user = await users_collection.find_one({"email": user.email})

        if existing_user:
            response.status_code = 400
            return {"message": "User already exists"}

        hashed_password = hashpw(
            user.password.encode("utf-8"),
            gensalt()
        ).decode("utf-8")

        user_dict = user.dict()
        user_dict["password"] = hashed_password

        await users_collection.insert_one(user_dict)

        return {"message": "User registered successfully"}

    except Exception:
        response.status_code = 500
        return {"message": "Registration error"}

async def login_user(user: UserLogin, response: Response):
    try:
        existing_user = await users_collection.find_one({"email": user.email})

        if not existing_user:
            response.status_code = 400
            return {"message": "Invalid credentials"}

        if not checkpw(
            user.password.encode("utf-8"),
            existing_user["password"].encode("utf-8")
        ):
            response.status_code = 400
            return {"message": "Invalid credentials"}

        token = create_access_token({"email": user.email}, SECRET_KEY)

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except Exception:
        response.status_code = 500
        return {"message": "Login error"}