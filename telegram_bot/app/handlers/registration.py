import logging
import re
import httpx
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
)
from app.core.config import settings

logger = logging.getLogger(__name__)

(
    BUSINESS_NAME,
    BUSINESS_EMAIL,
    PHONE_NUMBER,
    TELEBIRR_NAME,
    TELEBIRR_PHONE,
    CONFIRMATION,
) = range(6)

# Universal Navigation Keyboard
nav_keyboard = ReplyKeyboardMarkup([["Back", "Restart", "Cancel"]], resize_keyboard=True)

# Custom keyboard for phone number step with Telegram Contact Sharing button
phone_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📱 Share Phone Number", request_contact=True)],
        ["Back", "Restart", "Cancel"],
    ],
    resize_keyboard=True,
)

async def handle_navigation(text: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str | None:
    """Helper to catch universal navigation commands."""
    text_lower = text.lower()
    if text_lower == "cancel":
        await update.message.reply_text("Registration cancelled.", reply_markup=ReplyKeyboardRemove())
        context.user_data.clear()
        return "CANCEL"
    if text_lower == "restart":
        context.user_data.clear()
        await update.message.reply_text(
            "Let's start over.\n\nPlease enter your **Business Name** (2-100 characters):",
            reply_markup=nav_keyboard,
            parse_mode="Markdown"
        )
        return "RESTART"
    return None

async def start_register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        "Let's register your business.\n\n"
        "Please enter your **Business Name** (2-100 characters):",
        reply_markup=nav_keyboard,
        parse_mode="Markdown"
    )
    return BUSINESS_NAME

async def business_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    nav_action = await handle_navigation(text, update, context)
    if nav_action == "CANCEL": return ConversationHandler.END
    if nav_action == "RESTART": return BUSINESS_NAME
    if text.lower() == "back":
        await update.message.reply_text("This is the first step. Enter your **Business Name**:")
        return BUSINESS_NAME

    if len(text) < 2 or len(text) > 100:
        await update.message.reply_text("Invalid name. Must be 2-100 characters. Try again:")
        return BUSINESS_NAME

    context.user_data["business_name"] = text
    await update.message.reply_text("Great! Now enter your **Business Email**:", reply_markup=nav_keyboard, parse_mode="Markdown")
    return BUSINESS_EMAIL

async def business_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    nav_action = await handle_navigation(text, update, context)
    if nav_action == "CANCEL": return ConversationHandler.END
    if nav_action == "RESTART": return BUSINESS_NAME
    if text.lower() == "back":
        await update.message.reply_text("Going back. Please enter your **Business Name**:", reply_markup=nav_keyboard)
        return BUSINESS_NAME

    email = text.lower()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        await update.message.reply_text("Invalid email format. Please enter a valid email:")
        return BUSINESS_EMAIL

    context.user_data["business_email"] = email
    await update.message.reply_text(
        "Now share your **Phone Number** using the button below or enter it manually (e.g. 0911223344):",
        reply_markup=phone_keyboard,
        parse_mode="Markdown"
    )
    return PHONE_NUMBER

async def phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # 1. Handle Contact object if shared via Telegram button
    if update.message.contact:
        raw = update.message.contact.phone_number
    # 2. Handle text input if typed manually or navigation option pressed
    elif update.message.text:
        text = update.message.text.strip()
        nav_action = await handle_navigation(text, update, context)
        if nav_action == "CANCEL": return ConversationHandler.END
        if nav_action == "RESTART": return BUSINESS_NAME
        if text.lower() == "back":
            await update.message.reply_text("Going back. Please enter your **Business Email**:", reply_markup=nav_keyboard)
            return BUSINESS_EMAIL
        raw = text
    else:
        await update.message.reply_text(
            "Please tap '📱 Share Phone Number' or type a valid phone number:",
            reply_markup=phone_keyboard
        )
        return PHONE_NUMBER

    # Normalize phone number
    num = re.sub(r"[^\d+]", "", raw)
    if num.startswith("+251"): num = "0" + num[4:]
    elif num.startswith("251"): num = "0" + num[3:]
    
    if not re.match(r"^09\d{8}$", num):
        await update.message.reply_text(
            "Invalid Ethiopian phone number. Must be like 0911223344. Try again or tap '📱 Share Phone Number':",
            reply_markup=phone_keyboard
        )
        return PHONE_NUMBER

    context.user_data["phone_number"] = num
    await update.message.reply_text("Enter your **Telebirr Name** (account holder name, 2-100 chars):", reply_markup=nav_keyboard, parse_mode="Markdown")
    return TELEBIRR_NAME

async def telebirr_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    nav_action = await handle_navigation(text, update, context)
    if nav_action == "CANCEL": return ConversationHandler.END
    if nav_action == "RESTART": return BUSINESS_NAME
    if text.lower() == "back":
        await update.message.reply_text("Going back. Please enter your **Phone Number**:", reply_markup=nav_keyboard)
        return PHONE_NUMBER

    if len(text) < 2 or len(text) > 100:
        await update.message.reply_text("Name must be 2-100 characters. Please re-enter:")
        return TELEBIRR_NAME

    context.user_data["telebirr_name"] = text
    await update.message.reply_text("Finally, enter your **Telebirr Phone Number** (e.g. 0911223344):", reply_markup=nav_keyboard, parse_mode="Markdown")
    return TELEBIRR_PHONE

async def telebirr_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    nav_action = await handle_navigation(text, update, context)
    if nav_action == "CANCEL": return ConversationHandler.END
    if nav_action == "RESTART": return BUSINESS_NAME
    if text.lower() == "back":
        await update.message.reply_text("Going back. Please enter your **Telebirr Name**:", reply_markup=nav_keyboard)
        return TELEBIRR_NAME

    num = re.sub(r"[^\d+]", "", text)
    if num.startswith("+251"): num = "0" + num[4:]
    elif num.startswith("251"): num = "0" + num[3:]
    
    if not re.match(r"^09\d{8}$", num):
        await update.message.reply_text("Invalid Telebirr number. Must be like 0911223344:")
        return TELEBIRR_PHONE

    context.user_data["telebirr_phone"] = num

    summary = (
        "📋 **Registration Summary**\n\n"
        f"Business Name: {context.user_data['business_name']}\n"
        f"Email: {context.user_data['business_email']}\n"
        f"Phone: {context.user_data['phone_number']}\n"
        f"Telebirr Name: {context.user_data['telebirr_name']}\n"
        f"Telebirr Phone: {context.user_data['telebirr_phone']}\n\n"
        "Is this correct? Reply **Yes** or **No**."
    )
    confirm_kb = ReplyKeyboardMarkup([["Yes", "No"], ["Back", "Restart", "Cancel"]], resize_keyboard=True)
    await update.message.reply_text(summary, reply_markup=confirm_kb, parse_mode="Markdown")
    return CONFIRMATION

async def confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answer = update.message.text.strip().lower()
    nav_action = await handle_navigation(answer, update, context)
    if nav_action == "CANCEL": return ConversationHandler.END
    if nav_action == "RESTART": return BUSINESS_NAME
    if answer == "back":
        await update.message.reply_text("Going back. Please enter your **Telebirr Phone Number**:", reply_markup=nav_keyboard)
        return TELEBIRR_PHONE

    if answer == "yes":
        payload = {
            "telegram_id": update.effective_user.id,
            "telegram_username": update.effective_user.username,
            "telegram_first_name": update.effective_user.first_name,
            "telegram_last_name": update.effective_user.last_name,
            "business_name": context.user_data["business_name"],
            "business_email": context.user_data["business_email"],
            "phone_number": context.user_data["phone_number"],
            "telebirr_name": context.user_data["telebirr_name"],
            "telebirr_phone": context.user_data["telebirr_phone"],
        }
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    f"{settings.INTERNAL_API_URL}/merchants/register",
                    json=payload,
                    headers={"X-Internal-API-Key": settings.INTERNAL_API_KEY},
                )
                if resp.status_code == 201:
                    await update.message.reply_text(
                        "✅ Registration successful!\n\n"
                        "You are now a registered merchant.\n"
                        "Available subscription plans will be shown soon.",
                        reply_markup=ReplyKeyboardMarkup([["View Subscription Plans"]], resize_keyboard=True),
                    )
                else:
                    detail = resp.json().get("detail", "Registration failed.")
                    await update.message.reply_text(f"❌ Error: {detail}", reply_markup=nav_keyboard)
                    return CONFIRMATION
            except Exception as e:
                logger.error(f"Registration API call failed: {e}")
                await update.message.reply_text("⚠️ Service temporarily unavailable. Please try again later.", reply_markup=nav_keyboard)
                return CONFIRMATION
        return ConversationHandler.END

    elif answer == "no":
        await update.message.reply_text("Registration cancelled. You can start again with /register.", reply_markup=ReplyKeyboardRemove())
        context.user_data.clear()
        return ConversationHandler.END
    else:
        await update.message.reply_text("Please reply with **Yes**, **No**, **Back**, **Restart**, or **Cancel**.")
        return CONFIRMATION

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Registration cancelled.", reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END

def create_registration_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("register", start_register)],
        states={
            BUSINESS_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, business_name)],
            BUSINESS_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, business_email)],
            # Updated filter to accept both TEXT and CONTACT updates
            PHONE_NUMBER: [MessageHandler((filters.TEXT | filters.CONTACT) & ~filters.COMMAND, phone_number)],
            TELEBIRR_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, telebirr_name)],
            TELEBIRR_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, telebirr_phone)],
            CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirmation)],
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )