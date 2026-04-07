from typing import Optional
from pydantic import BaseModel


class HRRegister(BaseModel):
    hr_name: str
    hr_password: str


class HRLogin(BaseModel):
    hr_name: str
    hr_password: str


class ApproveRejectStatus(BaseModel):
    employee_id: str
    leave_id: str
    status: str
    rejection_reason: Optional[str] = None