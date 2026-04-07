from models.user_model import UserRegister, UserLogin, AdminRegister, AdminLogin
from dbconnect import users_collection
from bcrypt import hashpw, gensalt, checkpw
from utils import create_access_token, SECRET_KEY

# Register user
async def register_user(user: UserRegister, response):
    try:
        # Check if user already exists
        existing_user = await users_collection.find_one({"username": user.username})
        if existing_user:
            response.status_code = 400
            return {"message": "User already exists"}
        else:
            # Insert user (role Customer)
            user_data = {
                "username": user.username,
                "password": hashpw(user.password.encode('utf-8'), gensalt()),
                "role": "Customer"
            }
            # Insert user
            await users_collection.insert_one(user_data)
            response.status_code = 201
            return {"message": "User registered successfully"}
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}

# Register admin
async def register_admin(admin: AdminRegister, response):
    try:
        # Check if user already exists
        existing_user = await users_collection.find_one({"username": admin.username})
        if existing_user:
            response.status_code = 400
            return {"message": "User already exists"}
        else:
            # Insert user (role Admin)
            user_data = {
                "username": admin.username,
                "password": hashpw(admin.password.encode('utf-8'), gensalt()),
                "role": "admin"
            }
            # Insert user
            await users_collection.insert_one(user_data)
            response.status_code = 201
            return {"message": "Admin registered successfully"}
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}

# Login user
async def login_user(user: UserLogin, response):
    try:
        # Check if user exists
        existing_user = await users_collection.find_one({"username": user.username})
        if not existing_user:
            response.status_code = 404
            return {"message": "User not found"}
        # Check password
        elif not checkpw(user.password.encode('utf-8'), existing_user["password"]):
            response.status_code = 401
            return {"message": "Incorrect password"}
        # Generate access token
        else:
            access_token = create_access_token({"sub": existing_user["username"], "role": existing_user.get("role", "Customer")}, SECRET_KEY)
            response.status_code = 200
            return {"message": "Login successful", "access_token": access_token}
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}
    
async def login_admin(admin: AdminLogin, response):
    try:
        # Check if admin exists
        existing_admin = await users_collection.find_one({"username": admin.username, "role": "admin"})
        if not existing_admin:
            response.status_code = 404
            return {"message": "Admin not found"}
        # Check password
        elif not checkpw(admin.password.encode('utf-8'), existing_admin["password"]):
            response.status_code = 401
            return {"message": "Incorrect password"}
        # Generate access token
        else:
            access_token = create_access_token({"sub": existing_admin["username"], "role": existing_admin.get("role", "admin")}, SECRET_KEY)
            response.status_code = 200
            return {"message": "Login successful", "access_token": access_token}
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}