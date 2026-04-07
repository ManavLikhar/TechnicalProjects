from datetime import datetime
from bcrypt import checkpw, gensalt, hashpw
from bson import ObjectId
from dbconnect import collection_HR, collection_leave
from models.hr_model import ApproveRejectStatus, HRLogin, HRRegister
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


async def register_hr(hr: HRRegister, response):
    try:
        existing_hr = await collection_HR.find_one({"hr_name": hr.hr_name})
        if existing_hr:
            response.status_code = 400
            return {"message": "HR already exists"}

        new_hr = hr.model_dump() if hasattr(hr, "model_dump") else hr.dict()
        new_hr["hr_password"] = hashpw(hr.hr_password.encode("utf-8"), gensalt())
        result = await collection_HR.insert_one(new_hr)

        response.status_code = 201
        return {"message": "HR registered successfully", "hr_id": str(result.inserted_id)}
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}


async def login_hr(hr: HRLogin, response):
    try:
        db_hr = await collection_HR.find_one({"hr_name": hr.hr_name})
        if db_hr and checkpw(hr.hr_password.encode("utf-8"), db_hr["hr_password"]):
            token_data = {"hr_id": str(db_hr["_id"]), "role": "hr"}
            token = create_token(token_data)
            return {"message": "Login successful", "token": token}

        response.status_code = 401
        return {"message": "Invalid username or password"}
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}


async def ar_status(leave: ApproveRejectStatus, response):
    try:
        update_fields = {"status": leave.status}
        if leave.rejection_reason:
            update_fields["rejection_reason"] = leave.rejection_reason

        result = await collection_leave.update_one(
            {"_id": ObjectId(leave.leave_id), "employee_id": ObjectId(leave.employee_id)},
            {"$set": update_fields},
        )

        if result.matched_count:
            response.status_code = 200
            return {"message": "Leave status updated successfully"}

        response.status_code = 404
        return {"message": "Leave request not found"}
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}


async def get_leave_history(employee_id: str, leave_id: str, response):
    try:
        leave_data = await collection_leave.find_one(
            {"_id": ObjectId(leave_id), "employee_id": ObjectId(employee_id)}
        )

        if leave_data:
            response.status_code = 200
            return {"leave": _serialize_leave(leave_data)}

        response.status_code = 404
        return {"message": "Leave not found"}
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}
