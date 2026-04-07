from fastapi import APIRouter, Response
from models.auth_model import UserRegister, UserLogin
from controllers.auth_controller import register_user, login_user

auth_router = APIRouter()

@auth_router.post("/register")
async def register(user: UserRegister, response: Response):
    return await register_user(user, response)

@auth_router.post("/login")
async def login(user: UserLogin, response: Response):
    return await login_user(user, response)