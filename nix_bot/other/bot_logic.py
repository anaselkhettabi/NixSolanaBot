import asyncio
from telegram import Bot

# Replace with your bot's token
BOT_TOKEN = "7734338247:AAE4Gq-Xem5WZyEdzKiOUscGt_PvE4j8FPU"

async def get_chat_id():
    bot = Bot(token=BOT_TOKEN)
    updates = await bot.get_updates()
    for update in updates:
        print(f"Chat ID: {update.message.chat.id}")

# Run the asynchronous function
asyncio.run(get_chat_id())
