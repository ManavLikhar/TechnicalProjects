from fastapi import APIRouter, Response
from booking_model import Room, Booking
from controller.booking_controller import create_room, list_roooms, book_room, cancel_booking, get_bookings

router = APIRouter(prefix="/api")

@router.post("/add_rooms")
async def create_room_route(room: Room, response: Response):
    return await create_room(room, response)

@router.get("/get_rooms")
async def list_rooms_route(response: Response):
    return await list_roooms(response)

@router.post("/book_room")
async def book_room_route(booking: Booking, response: Response):
    return await book_room(booking, response)

@router.get("/get_bookings")
async def get_bookings_route(response: Response):
    return await get_bookings(response)

@router.delete("/cancel_booking")
async def cancel_booking_route(room_name: str, start_time: str, response: Response):
    return await cancel_booking(room_name, start_time, response)