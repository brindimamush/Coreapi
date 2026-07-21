import logging
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from app.core.config import settings

logger = logging.getLogger(__name__)

def format_plan_card(plan: dict) -> str:
    keys = "Unlimited" if plan.get("max_api_keys") is None else plan['max_api_keys']
    services = "Unlimited" if plan.get("max_services") is None else plan['max_services']
    invoices = "Unlimited" if plan.get("max_monthly_invoices") is None else f"{plan['max_monthly_invoices']}/mo"

    return (
        f"🌟 **{plan['name']}**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"⏱ **Duration**: {plan['duration_days']} Days\n"
        f"💰 **Price**: {plan['price']} {plan['currency']}\n"
        f"🔑 **Max API Keys**: {keys}\n"
        f"🛠 **Services Allowed**: {services}\n"
        f"🧾 **Invoice Limit**: {invoices}\n"
        f"📝 _{plan.get('description') or 'No description available.'}_\n"
    )

async def view_plans_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays available ACTIVE subscription plans."""
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{settings.CORE_API_URL}/subscription-plans")
            if resp.status_code == 200:
                plans = resp.json()
                if not plans:
                    text = "No active subscription plans available at the moment."
                    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Refresh", callback_data="refresh_plans")]])
                else:
                    text = "📦 **Available Subscription Plans**\n\n" + "\n".join([format_plan_card(p) for p in plans])
                    keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔄 Refresh Plans", callback_data="refresh_plans")]
                    ])

                if update.callback_query:
                    await update.callback_query.answer("Plans refreshed!")
                    await update.callback_query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")
                else:
                    await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")
            else:
                msg = "⚠️ Failed to fetch subscription plans."
                if update.callback_query:
                    await update.callback_query.answer(msg)
                else:
                    await update.message.reply_text(msg)
        except Exception as e:
            logger.error(f"Error fetching subscription plans: {e}")
            msg = "⚠️ Service unavailable. Please try again later."
            if update.callback_query:
                await update.callback_query.answer(msg)
            else:
                await update.message.reply_text(msg)

async def plans_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "refresh_plans":
        await view_plans_command(update, context)

def register_plan_handlers(app):
    app.add_handler(CommandHandler("plans", view_plans_command))
    app.add_handler(MessageHandler(filters.Regex("^Subscription Plans$|^View Subscription Plans$"), view_plans_command))
    app.add_handler(CallbackQueryHandler(plans_callback, pattern="^refresh_plans$"))