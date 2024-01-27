from fastapi import FastAPI
from app.api.main import router
from app.schemas.error import ValidationError
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="TRADEWITHCHUN BACKEND",
    responses={
        422: {
            "description": "Validation Error",
            "model": ValidationError,
        }
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
