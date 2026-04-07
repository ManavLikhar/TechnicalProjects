from fastapi import APIRouter, Response
from models.user_model import UserRegister, UserLogin, AdminRegister, AdminLogin
from controllers.auth_controller import register_user, login_user, register_admin, login_admin

router = APIRouter(prefix="/auth")

@router.post("/register")
async def register(user: UserRegister, response: Response):
    return await register_user(user, response)

@router.post("/register/admin")
async def register_admin_route(admin: AdminRegister, response: Response):
    return await register_admin(admin, response)

@router.post("/login")
async def login(user: UserLogin, response: Response):
    return await login_user(user, response)

@router.post("/login/admin")
async def login_admin_route(admin: AdminLogin, response: Response):
    return await login_admin(admin, response)