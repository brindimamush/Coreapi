import logging
import httpx
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from app.core.config import settings

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Check registration status
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"{settings.INTERNAL_API_URL}/merchants/check/{user.id}",
                headers={"X-Internal-API-Key": settings.INTERNAL_API_KEY},
            )
            if resp.status_code == 200:
                # Flow: Already Registered -> Open Merchant Menu
                await update.message.reply_text(
                    "Welcome back to the Core Verification Platform!\n\n"
                    "Use the menu below to manage your account.",
                    reply_markup=ReplyKeyboardMarkup([["Subscription Plans", "My Profile"]], resize_keyboard=True)
                )
                return
        except Exception as e:
            logger.error(f"Failed to check merchant status: {e}")
            await update.message.reply_text("⚠️ Service temporarily unavailable. Please try again later.")
            return

    # Flow: Not Registered -> Prompt /register
    await update.message.reply_text(
        "Welcome to the Core Verification Platform bot.\n\n"
        "You are not registered yet. Please tap or type /register to create your permanent identity."
    )
