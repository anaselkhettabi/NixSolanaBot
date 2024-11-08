from telegram.ext import CommandHandler
from commands.subscription import subscribe
from commands.tracking import track_wallet

def register_command_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("subscribe", subscribe))
    dispatcher.add_handler(CommandHandler("track", track_wallet))
    # Register other commands as needed