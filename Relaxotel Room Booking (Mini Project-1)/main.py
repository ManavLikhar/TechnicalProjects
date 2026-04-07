from fastapi import FastAPI
from router import user_router
from utils import decode_access_token, SECRET_KEY
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development only)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Log requests
@app.middleware("http")
async def log_requests(request, call_next):
    print(request.url.path)
    if request.url.path in ["/user/register", "/user/login", "/docs", "/openapi.json"]:
        response = await call_next(request)
        return response
    else:
        # Get the token from the Authorization header
        token = request.headers["authorization"].split(" ")[1] if "authorization" in request.headers else None
        # Verify the token
        if token is None:
            return JSONResponse(status_code=401, content={"message": "Unauthorized"})
        else:
            # Decode the token
            decoded_token = decode_access_token(token, SECRET_KEY)
            print(decoded_token)
            if decoded_token is None:
                return JSONResponse(status_code=401, content={"message": "Invalid token"})
            else:
                response = await call_next(request)
                return response
            
app.include_router(user_router.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}