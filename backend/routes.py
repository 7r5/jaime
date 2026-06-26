from fastapi import APIRouter
from .webhook import router as webhook_router
from .auth import router as auth_router
from .admin import router as admin_router

api_router = APIRouter()
api_router.include_router(webhook_router, prefix="/webhook")
api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(admin_router, prefix="/admin")
