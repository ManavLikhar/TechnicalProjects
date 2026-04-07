import logging
from fastapi import FastAPI, Request
from routers.auth_router import router as auth_router
from routers.product_router import router as product_router
from routers.order_router import router as order_router
from utils import decode_access_token, SECRET_KEY
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="Inventory Management System")

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins
    allow_credentials=False, # Authorization header is used; wildcard origins with credentials is invalid in browsers
    allow_methods=["*"], # Allow all HTTP methods
    allow_headers=["*"], # Allow all headers
)

PUBLIC_PATHS = {
    "/auth/register",
    "/auth/login",
    "/auth/register/admin",
    "/auth/login/admin",
    "/openapi.json",
}

PUBLIC_PREFIXES = ("/docs", "/redoc")

# Global Middleware for Logging and Authentication
@app.middleware("http")
async def global_middleware(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")

    # Skip the middleware for OPTIONS requests
    if request.method == "OPTIONS":
        return await call_next(request)

    # Skip the middleware for public routes and documentation subpaths
    if request.url.path in PUBLIC_PATHS or request.url.path.startswith(PUBLIC_PREFIXES):
        return await call_next(request)

    # Get the token from the Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})

    _, _, token = auth_header.partition("Bearer ")
    token = token.strip()
    if not token:
        return JSONResponse(status_code=401, content={"message": "Invalid token format"})
    
    # Decode the token
    payload = decode_access_token(token, SECRET_KEY)
    if payload is None:
        return JSONResponse(status_code=401, content={"message": "Invalid token"})
    
    # Store user info in request state
    request.state.user = payload

    # Only Admin can Add, Get, Update, Delete
    role = str(payload.get("role", "Customer")).lower()
    if request.method in ["POST", "PUT", "DELETE"] and role != "admin":
        if request.url.path.rstrip("/") != "/orders/place":
            return JSONResponse(status_code=403, content={"message": "Admin access required"})
    
    # Only Admin can Get All Orders
    if request.method == "GET" and request.url.path == "/orders/all":
        if role != "admin":
            return JSONResponse(status_code=403, content={"message": "Admin access required"})

    return await call_next(request)

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(order_router)
