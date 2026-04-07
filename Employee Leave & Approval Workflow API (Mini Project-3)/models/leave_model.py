from pydantic import BaseModel

class LeaveApply(BaseModel):
    
    employee_id: str
    start_date: str
    end_date: str
    reason: str