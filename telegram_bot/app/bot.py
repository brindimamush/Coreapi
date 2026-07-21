from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from app.core.config import settings
from app.handlers.start import start_command
from app.handlers.error import error_handler
from app.handlers.registration import create_registration_handler

def create_bot() -> Application:
    builder = Application.builder().token(settings.BOT_TOKEN)
    app = builder.build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(create_registration_handler())
    # Placeholder for future conversation handlers
    # conv_handler = ConversationHandler(...)
    # app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.COMMAND, error_handler))  # unknown command
    app.add_error_handler(error_handler)
    return app