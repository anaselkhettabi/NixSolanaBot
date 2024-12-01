from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from db import get_user, add_user_wallet, update_user_subscription
from wallet_utils import create_wallet, check_wallet_balance

SUBSCRIPTION_COST_SOL = 0.01

async def renew(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    user = get_user(chat_id)

    if user and user.subscription_status:
        await update.message.reply_text("You are already subscribed.")
        return

    subscription_status=False
    # Generate a new wallet for the user
    wallet_public_key, wallet_private_key = create_wallet()
    # Save the wallet info to the database with the username
    add_user_wallet(username, chat_id, subscription_status, wallet_public_key, wallet_private_key)
    print(f"Wallet saved to DB for chat_id {chat_id}: {wallet_public_key}")

    message_text = f"Deposit {SUBSCRIPTION_COST_SOL} SOL to this address: {wallet_public_key}\nClick 'Activate' after payment."
    keyboard = [[InlineKeyboardButton("Activate", callback_data="activate_subscription")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(message_text, reply_markup=reply_markup)

async def activate_subscription(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.from_user.id
    user = get_user(chat_id)

    if not user:
        print(f"No user found for chat_id {chat_id}")
        await query.answer("This is what you are not supposed to see", show_alert=True)
        return

    print(f"User found: {user.chat_id}, Wallet: {user.wallet_public_key}")

    # Check wallet balance
    balance = await check_wallet_balance(user.wallet_public_key)
    if balance >= SUBSCRIPTION_COST_SOL:
        update_user_subscription(chat_id, active=True)  # Activate subscription
        await query.edit_message_text("Payment received! Your subscription is now active.")
    else:
        await query.answer("Payment not received yet. Please wait or send the required amount.", show_alert=True)
