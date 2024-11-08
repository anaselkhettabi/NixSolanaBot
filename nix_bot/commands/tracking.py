from utils.db import get_tracked_wallets
from telegram import Update
from telegram.ext import CallbackContext

def track_wallet(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    wallets = get_tracked_wallets(user_id)
    wallet_list = "\n".join([f"{w.kol_name}: {w.wallet_address}" for w in wallets])
    update.message.reply_text(f"Currently tracking:\n{wallet_list}")