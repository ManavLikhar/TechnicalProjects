from fastapi import APIRouter, Response, Request
from models.order_model import Order
from controllers.order_controller import place_order, get_all_orders

router = APIRouter(prefix="/orders")

@router.post("/place")
async def place_order_route(request: Request, order: Order, response: Response):
    username = request.state.user.get("sub")
    return await place_order(order, username, response)

@router.get("/all")
async def get_all_orders_route(response: Response):
    return await get_all_orders(response)