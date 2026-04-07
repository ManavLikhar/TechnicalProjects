from datetime import datetime
from bcrypt import checkpw, gensalt, hashpw
from bson import ObjectId
from dbconnect import collection_leave, collection_users
from models import user_model
from utils import create_token


def _serialize_leave(leave_doc: dict):
    return {
        "id": str(leave_doc.get("_id")),
        "employee_id": str(leave_doc.get("employee_id")),
        "start_date": leave_doc.get("start_date").isoformat() if isinstance(leave_doc.get("start_date"), datetime) else leave_doc.get("start_date"),
        "end_date": leave_doc.get("end_date").isoformat() if isinstance(leave_doc.get("end_date"), datetime) else leave_doc.get("end_date"),
        "reason": leave_doc.get("reason"),
        "status": leave_doc.get("status", "pending"),
        "rejection_reason": leave_doc.get("rejection_reason"),
    }


async def register_user(user: user_model.UserRegister, response):
    try:
        existing_user = await collection_users.find_one({"username": user.username})
        if existing_user:
            response.status_code = 400
            return {"message": "User already exists"}

        new_user = user.model_dump() if hasattr(user, "model_dump") else user.dict()
        new_user["password"] = hashpw(user.password.encode("utf-8"), gensalt())
        new_user["role"] = "employee"
        result = await collection_users.insert_one(new_user)

        response.status_code = 201
        return {
            "message": "User registered successfully",
            "user_id": str(result.inserted_id),
        }
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}


async def login_user(user: user_model.UserLogin, response):
    try:
        db_user = await collection_users.find_one({"username": user.username})
        if db_user and checkpw(user.password.encode("utf-8"), db_user["password"]):
            token_data = {"user_id": str(db_user["_id"]), "role": "employee"}
            token = create_token(token_data)
            return {"message": "Login successful", "token": token}

        response.status_code = 401
        return {"message": "Invalid username or password"}
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}


async def get_leave_status(employee_id: str, response):
    try:
        leave_data = await collection_leave.find(
            {"employee_id": ObjectId(employee_id)}
        ).to_list(length=None)

        if leave_data:
            response.status_code = 200
            return {"leave": [_serialize_leave(item) for item in leave_data]}

        response.status_code = 404
        return {"message": "Leave not found for this employee"}
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}
