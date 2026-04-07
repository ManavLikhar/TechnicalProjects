from visitor_model import VisitorEntry, ExitUpdate
from dbconnect import visitor_collection
from datetime import datetime
from fastapi import Response
from bson import ObjectId

# Check-in visitor
async def check_in_visitor(visitor: VisitorEntry, response: Response):
    try:
        visitor_entry = {
            "name": visitor.name,
            "phone": visitor.phone,
            "purpose": visitor.purpose,
            "host_employee": visitor.host_employee,
            "check_in_time": datetime.now(),
            "status": "checked_in"
        }
        result = await visitor_collection.insert_one(visitor_entry)
        response.status_code = 201
        return {"message": "Visitor checked in successfully", "visitor_id": str(result.inserted_id)}
    except Exception as e:
        response.status_code = 500
        return {"message": "Failed to check in visitor", "error": str(e)}
    
# Mark Exit
async def check_out_visitor(visitor_id: str, exit_update: ExitUpdate, response: Response): 
    try: 
        result = await visitor_collection.update_one(
            {"_id": ObjectId(visitor_id), "status": "checked_in"}, 
            {"$set": {"exit_time": exit_update.exit_time, "status": "checked_out"}}
        )
        if result.modified_count == 0:
            response.status_code = 404
            return {"message": "Visitor not found or already checked out"}
        else:
            response.status_code = 200
            return {"message": "Visitor checked out successfully"}
    except Exception as e:
        response.status_code = 500
        return {"message": "Failed to check out visitor", "error": str(e)}
    
# See all inside visitors
async def get_inside_visitors(response: Response): 
    try: 
        visitors = []
        async for visitor in visitor_collection.find({"status": "checked_in"}):
            visitor["_id"] = str(visitor["_id"])
            visitors.append(visitor)
        response.status_code = 200
        return {"visitors": visitors}
    except Exception as e:
        response.status_code = 500
        return {"message": "Failed to retrieve inside visitors", "error": str(e)}
    
# Full History
async def visitor_history(response: Response):
    try:
        visitors = await visitor_collection.find({"status": "checked_out"}, {"_id": 0}).to_list(length=None)
        return {"visitors": visitors}
    except Exception as e:
        response.status_code = 500
        return {"message": "Failed to retrieve visitor history", "error": str(e)}