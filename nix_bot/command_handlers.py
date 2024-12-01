from telegram.ext import CommandHandler, CallbackQueryHandler
from subscriptions import renew, activate_subscription

def register_command_handlers(dispatcher):
    """Register all bot commands and their respective handlers."""
    # Command Handlers
    dispatcher.add_handler(CommandHandler("renew", renew))
    dispatcher.add_handler(CallbackQueryHandler(activate_subscription, pattern="^activate_subscription$"))
