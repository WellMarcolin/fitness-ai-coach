"""Script para iniciar o bot Telegram em polling mode (modo desenvolvimento)."""
import asyncio
import logging
import sys

from app.config import settings
from app.core.telegram_bot import get_application

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    token = settings.telegram_bot_token
    if not token or token == "your_telegram_bot_token":
        logger.error("Telegram bot token not configured in .env")
        sys.exit(1)

    logger.info("Starting Telegram bot in polling mode...")
    app = get_application()

    me = await app.bot.get_me()
    logger.info(f"Bot authenticated: @{me.username} (ID: {me.id})")

    await app.initialize()
    await app.start()
    logger.info("Bot is running. Press Ctrl+C to stop.")

    try:
        await app.updater.start_polling()
        # Keep running
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        logger.info("Stopping bot...")
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
