from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VisitorEntry(BaseModel):

    name: str
    phone: int
    purpose: str
    host_employee: str

class ExitUpdate(BaseModel):

    exit_time: datetime