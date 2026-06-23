from fastapi import APIRouter, HTTPException, Request
from app.core.telegram_bot import application

router = APIRouter()


@router.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = await application.update_queue.put(data)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/set-webhook")
async def set_telegram_webhook(url: str = ""):
    from app.config import settings

    webhook_url = url or settings.telegram_webhook_url
    if not webhook_url:
        raise HTTPException(status_code=400, detail="Webhook URL is required")

    try:
        await application.bot.set_webhook(url=webhook_url)
        return {"status": "webhook set", "url": webhook_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/delete-webhook")
async def delete_telegram_webhook():
    try:
        await application.bot.delete_webhook()
        return {"status": "webhook deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def bot_info():
    try:
        me = await application.bot.get_me()
        webhook = await application.bot.get_webhook_info()
        return {
            "username": me.username,
            "id": me.id,
            "webhook_url": webhook.url,
            "webhook_pending": webhook.pending_update_count,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
