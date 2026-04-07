from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routers.auth_router import auth_router
from routers.mcq_router import mcq_router
from utils import decode_access_token

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PUBLIC_PATHS = [
    "/auth/login",
    "/auth/register",
    "/mcq/generate-mcqs",
    "/docs",
    "/openapi.json",
    "/redoc"
]

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    path = request.url.path

    if path in PUBLIC_PATHS:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    
    parts = auth_header.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        return JSONResponse(status_code=401, content={"message": "Invalid token"})
    
    token = parts[1]
    decoded_token = decode_access_token(token)

    if decoded_token is None:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})

    return await call_next(request)

app.include_router(auth_router, prefix="/auth")
app.include_router(mcq_router, prefix="/mcq")