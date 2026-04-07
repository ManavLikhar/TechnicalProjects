from booking_model import Booking, Room
from datetime import datetime
from dbconnect import booking_collection, room_collection

# Add Room
async def create_room(room: Room, response):
    try:
        res = await room_collection.insert_one(room.dict())
        response.status_code = 201
        return {"message": "Room created successfully", "id": str(res.inserted_id)}
    except Exception as e:
        response.status_code = 500
        return {"error": str(e)}

# Get Rooms
async def list_roooms(response):
    try:
        rooms = []
        async for room in room_collection.find():
            rooms.append({"id": str(room["_id"]), "name": room["name"], "capacity": room["capacity"]})
        return rooms
    except Exception as e:
        response.status_code = 500
        return {"error": str(e)}

# Book Room
async def book_room(booking: Booking, response):
    try:
        # Check time validity
        if booking.start_time >= booking.end_time:
            response.status_code = 400
            return {"error": "Start time must be before end time"}

        # Check Overlapping
        overlapping = await booking_collection.find_one(
            {
                "room_name": booking.room_name,
                "start_time": {"$lt": booking.end_time},
                "end_time": {"$gt": booking.start_time},
            }
        )

        if overlapping:
            response.status_code = 400
            return {"error": "Room is already booked for the selected time slot"}

        res = await booking_collection.insert_one(booking.dict())
        response.status_code = 201
        return {"message": "Room booked successfully", "id": str(res.inserted_id)}
    except Exception as e:
        response.status_code = 500
        return {"error": str(e)}

# Get Bookings
async def get_bookings(response):
    try:
        bookings = []
        async for booking in booking_collection.find():
            bookings.append(
                {
                    "id": str(booking["_id"]),
                    "room_name": booking["room_name"],
                    "user_name": booking["user_name"],
                    "start_time": booking["start_time"],
                    "end_time": booking["end_time"],
                }
            )
        return bookings
    except Exception as e:
        response.status_code = 500
        return {"error": str(e)}

# Cancel Booking
async def cancel_booking(room_name: str, start_time, response):
    try:
        if isinstance(start_time, str):
            iso_value = start_time.rstrip("Z")
            try:
                start_time = datetime.fromisoformat(iso_value)
            except ValueError:
                response.status_code = 400
                return {"error": "Invalid start_time format. Use ISO datetime."}

        res = await booking_collection.delete_one({"room_name": room_name, "start_time": start_time})
        if res.deleted_count == 0:
            response.status_code = 404
            return {"error": "Booking not found"}
        return {"message": "Booking cancelled successfully"}
    except Exception as e:
        response.status_code = 500
        return {"error": str(e)}