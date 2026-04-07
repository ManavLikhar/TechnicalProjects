from fastapi import FastAPI
from router import visitor_router

app = FastAPI(title="Visitor Management API")

app.include_router(visitor_router.router)