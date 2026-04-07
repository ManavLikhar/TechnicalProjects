from fastapi import APIRouter, Response
from models import leave_model
from controllers.leave_controller import apply_leave
from bson import ObjectId

router = APIRouter(prefix="/leave")

@router.post("/apply")
async def apply(leave: leave_model.LeaveApply, response: Response):
    return await apply_leave(leave, response)