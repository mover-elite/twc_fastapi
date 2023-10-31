from fastapi import FastAPI
from app.api.main import router
from app.schemas.error import ValidationError
from datetime import datetime


app = FastAPI(
    title="TRADEWITHCHUN BACKEND",
    responses={
        422: {
            "description": "Validation Error",
            "model": ValidationError,
        }
    },
)


@app.get("/")
def home():
    return datetime.now()


@app.get(
    "/ping",
)
def ping():
    """Ping the server"""
    return "pong"


app.include_router(router)
