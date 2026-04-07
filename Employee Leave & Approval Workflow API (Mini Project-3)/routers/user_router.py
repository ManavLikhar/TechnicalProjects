from fastapi import APIRouter, Response
from controllers.user_controller import get_leave_status, login_user, register_user
from models import user_model

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register(user: user_model.UserRegister, response: Response):
    return await register_user(user, response)


@router.post("/login")
async def login(user: user_model.UserLogin, response: Response):
    return await login_user(user, response)


@router.get("/leave/{employee_id}")
async def get_leave(employee_id: str, response: Response):
    return await get_leave_status(employee_id, response)
