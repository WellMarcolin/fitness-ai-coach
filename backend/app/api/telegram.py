from fastapi import APIRouter, HTTPException, Request
from app.core.telegram_bot import get_application

router = APIRouter()


@router.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        app = get_application()
        data = await request.json()
        await app.update_queue.put(data)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/set-webhook")
async def set_telegram_webhook(url: str = ""):
    from app.config import settings

    webhook_url = url or settings.telegram_webhook_url
    if not webhook_url:
        raise HTTPException(status_code=400, detail="Webhook URL is required")

    try:
        app = get_application()
        await app.bot.set_webhook(url=webhook_url)
        return {"status": "webhook set", "url": webhook_url}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/delete-webhook")
async def delete_telegram_webhook():
    try:
        app = get_application()
        await app.bot.delete_webhook()
        return {"status": "webhook deleted"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def bot_info():
    try:
        app = get_application()
        me = await app.bot.get_me()
        webhook = await app.bot.get_webhook_info()
        return {
            "username": me.username,
            "id": me.id,
            "webhook_url": webhook.url,
            "webhook_pending": webhook.pending_update_count,
        }
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
