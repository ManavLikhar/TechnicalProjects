from fastapi import APIRouter, Response
from controllers.hr_controller import ar_status, get_leave_history, login_hr, register_hr
from models import hr_model

router = APIRouter(prefix="/hr")


@router.post("/register")
async def register(hr: hr_model.HRRegister, response: Response):
    return await register_hr(hr, response)


@router.post("/login")
async def login(hr: hr_model.HRLogin, response: Response):
    return await login_hr(hr, response)


@router.post("/status")
async def status_update(leave: hr_model.ApproveRejectStatus, response: Response):
    return await ar_status(leave, response)


@router.get("/history/{employee_id}")
async def get_history(employee_id: str, leave_id: str, response: Response):
    return await get_leave_history(employee_id, leave_id, response)
