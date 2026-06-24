from fastapi import APIRouter

from app.api.intervals import router as intervals_router
from app.api.agents import router as agents_router
from app.api.telegram import router as telegram_router
from app.api.settings import router as settings_router

api_router = APIRouter()

api_router.include_router(intervals_router, prefix="/intervals", tags=["Intervals.icu"])
api_router.include_router(agents_router, prefix="/agents", tags=["AI Agents"])
api_router.include_router(telegram_router, prefix="/telegram", tags=["Telegram"])
api_router.include_router(settings_router, prefix="", tags=["Settings"])
