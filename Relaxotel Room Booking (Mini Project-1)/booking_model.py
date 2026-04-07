from pydantic import BaseModel
from datetime import datetime

class Room(BaseModel):
    name: str
    capacity: int

class Booking(BaseModel):
    room_name: str
    user_name: str
    start_time: datetime
    end_time: datetime