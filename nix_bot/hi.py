from telegram import Update
from telegram.ext import Application, CommandHandler

# Replace 'YOUR_BOT_TOKEN' with the token you got from BotFather
bot_token = "7734338247:AAE4Gq-Xem5WZyEdzKiOUscGt_PvE4j8FPU"

# Function to handle /start command
async def start(update: Update, context):
    """Send a welcome message with instructions."""
    welcome_message = """
Welcome to Nix, get started using the commands below:

Send /ping to check if the bot is online

Send /guide to get the comprehensive guide of Nix

Send /feedback [message] to provide feedback or any idea requests to @0xBl0ckus

Send /check_dex or /dex [contract-address] to check if the dex has been updated for a token.

Send /top_holders or /top [contract-address] to analyze top holders of a token.

Send /site_check or /site [site-url] to check if a site is reused.

Send /twitter_reuse or /x [twitter-handle] to check twitter account reuse history.

Send /wallet_analyzer or /wallet [wallet-address] to check PnLs of recently traded tokens for a wallet.

Send /graduated_stats or /stats to get the stats for recently graduated pumpfuns.

Send /reverse_image_search or /image [contract-address] to reverse image search for a token (SOL/TRON).

Send /common_top_traders or /common [contract-address] to filter common top traders from given contract addresses.

Send /bundle_check or /bundle [contract-address] to analyze if a token is bundled or not.

Send /hmap to get the price heatmap of the overall crypto market!

Send /holderscan or /holders [contract-address] to check holder information of a token.

Send /fresh [contract-address] to analyze top holder fresh wallets of a token.

Send /renew to purchase/renew your subscription - 1 SOL/month for individual subscriptions, contact @lunarfang_416 for group subscriptions.

Send /referral to view your referral earnings tab (partners only).

Send /my_id to retrieve your ID.

Want to contact the developer? @0xBl0ckus
    """
    await update.message.reply_text(welcome_message)

# Function to handle /ping command
async def ping(update: Update, context):
    """Ping the bot."""
    await update.message.reply_text('Pong! The bot is online.')

def main():
    """Start the bot and register handlers."""
    # Create an Application object using your bot token
    application = Application.builder().token(bot_token).build()

    # Register command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('ping', ping))

    # Add more handlers for other commands like /guide, /feedback, etc.

    # Start polling for updates (messages)
    application.run_polling()

if __name__ == '__main__':
    main()
