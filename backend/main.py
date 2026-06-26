from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import api_router

app = FastAPI(title="WhatsApp Assistant Bot")

from backend.database import create_db_and_tables

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

app.include_router(api_router)
