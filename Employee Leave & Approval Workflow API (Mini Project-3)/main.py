from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers import hr_router, leave_router, user_router
from utils import decode_token

app = FastAPI(title="HR Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PUBLIC_PATHS = {
    "/auth/register",
    "/auth/login",
    "/hr/register",
    "/hr/login",
    "/leave/apply",
    "/docs",
    "/openapi.json",
    "/redoc",
}

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    path = request.url.path
    if path in PUBLIC_PATHS:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})

    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return JSONResponse(status_code=401, content={"message": "Invalid authorization header"})

    token = parts[1]
    decoded_token = decode_token(token)
    if decoded_token is None:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})

    return await call_next(request)


app.include_router(user_router.router)
app.include_router(hr_router.router)
app.include_router(leave_router.router)
