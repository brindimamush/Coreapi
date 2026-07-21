import logging
from app.core.config import settings
from app.bot import create_bot
from app.core.logging import setup_logging

setup_logging()

if __name__ == "__main__":
    bot = create_bot()
    if settings.WEBHOOK_URL:
        bot.run_webhook(
            listen="0.0.0.0",
            port=8443,
            webhook_url=settings.WEBHOOK_URL,
        )
    else:
        bot.run_polling()