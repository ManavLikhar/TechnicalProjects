from fastapi import APIRouter, Response
from visitor_model import VisitorEntry, ExitUpdate
from controller.visitor_controller import check_in_visitor, check_out_visitor, get_inside_visitors, visitor_history

router = APIRouter(prefix="/visitors")

@router.post("/checkin")
async def check_in(visitor: VisitorEntry, response: Response):
    return await check_in_visitor(visitor, response)

@router.put("/checkout/{visitor_id}")
async def check_out(visitor_id: str, exit_update: ExitUpdate, response: Response):
    return await check_out_visitor(visitor_id, exit_update, response)

@router.get("/inside")
async def get_inside(response: Response):
    return await get_inside_visitors(response)

@router.get("/history")
async def get_history(response: Response):
    return await visitor_history(response)