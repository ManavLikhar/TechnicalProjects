from datetime import datetime
from bson import ObjectId
from dbconnect import collection_leave
from models import leave_model


async def apply_leave(leave: leave_model.LeaveApply, response):
    try:
        leave_data = leave.model_dump() if hasattr(leave, "model_dump") else leave.dict()

        start_date = datetime.strptime(leave_data["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(leave_data["end_date"], "%Y-%m-%d")
        if end_date < start_date:
            response.status_code = 400
            return {"message": "end_date must be greater than or equal to start_date"}

        leave_data["start_date"] = start_date
        leave_data["end_date"] = end_date
        leave_data["employee_id"] = ObjectId(leave_data["employee_id"])
        leave_data["status"] = "pending"

        result = await collection_leave.insert_one(leave_data)
        response.status_code = 201
        return {
            "message": "Leave applied successfully",
            "leave_id": str(result.inserted_id),
        }
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}
