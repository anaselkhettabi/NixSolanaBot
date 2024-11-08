from utils.db import get_user, update_user_subscription, add_user_wallet
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils.wallet_utils import create_wallet, check_wallet_balance
import asyncio

SUBSCRIPTION_COST_SOL = 0.01  # Set your subscription cost here

async def subscribe(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user = get_user(user_id)
    
    # Check if the user already has a subscription
    if user and user.subscription_status:
        update.message.reply_text("You are already subscribed.")
        return

    # Generate a new wallet for the user
    wallet_public_key, wallet_private_key_encrypted = create_wallet()
    
    # Save the wallet info to the database
    add_user_wallet(user_id, wallet_public_key, wallet_private_key_encrypted)
    
    # Inform the user to pay
    message_text = f"""
    Thanks for deciding to subscribe! 
    Monthly subscriptions are {SUBSCRIPTION_COST_SOL} SOL.
    Please deposit {SUBSCRIPTION_COST_SOL} SOL to the following address:
    `{wallet_public_key}`
    
    After you have sent the funds, please click the Check button below.
    """
    
    # Add a "Check" button to let the user trigger balance check
    keyboard = [[InlineKeyboardButton("Check", callback_data="check_payment")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(message_text, reply_markup=reply_markup)

async def check_payment(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    user = get_user(user_id)
    
    if not user or not user.wallet_public_key:
        await query.answer("No wallet found for your account. Please start the subscription process again.")
        return
    
    # Check if the user has sent the payment
    balance = await check_wallet_balance(user.wallet_public_key)
    if balance >= SUBSCRIPTION_COST_SOL:
        # Activate the subscription
        update_user_subscription(user_id, active=True)
        await query.edit_message_text("Payment received! Your subscription is now active.")
    else:
        await query.answer("Payment not received yet. Please wait or send the required amount.")