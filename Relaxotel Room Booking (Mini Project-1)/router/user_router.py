from fastapi import APIRouter, Response
from user_model import User
from controller.user_controller import register_user, login_user

router = APIRouter(prefix="/user")

@router.post("/register")
async def register_user_route(user: User, response: Response):
    return await register_user(user, response)

@router.post("/login")
async def login_user_route(email: str, password: str, response: Response):
    return await login_user(email, password, response)