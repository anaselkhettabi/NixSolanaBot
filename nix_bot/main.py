import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from config import TELEGRAM_TOKEN
from handlers.command_handler import register_command_handlers
from commands.subscription import subscribe, check_payment

# Set up logging to monitor bot activity and errors
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update, context):
    """Start command handler to welcome users."""
    await update.message.reply_text("Welcome to Nix Tracker Bot! Use /subscribe to begin.")

def main():
    # Initialize the Application (replaces Updater)
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("subscribe", subscribe))
    
    # Add a CallbackQueryHandler for button interactions (like "Check")
    application.add_handler(CallbackQueryHandler(check_payment, pattern="^check_payment$"))

    # Start the bot
    logger.info("Bot started. Listening for commands...")
    application.run_polling()

if __name__ == '__main__':
    main()
