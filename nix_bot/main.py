import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from config import TELEGRAM_TOKEN
from subscriptions import renew, activate_subscription

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update, context):
    await update.message.reply_text("Welcome to Nix Tracker Bot! Use /renew to subscribe or renew your subscription.")

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("renew", renew))
    application.add_handler(CallbackQueryHandler(activate_subscription, pattern="^activate_subscription$"))
    logger.info("Bot started. Listening for commands...")
    application.run_polling()

if __name__ == '__main__':
    main()
