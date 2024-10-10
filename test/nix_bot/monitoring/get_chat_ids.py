from telethon.sync import TelegramClient

api_id = '25329515'  # Your API ID
api_hash = 'fdb29fbe41dd3e020b8334a85f73ee6c'  # Your API Hash

# Initialize the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Define the asynchronous main function
async def main():
    # Iterate through all dialogs (chats, groups, channels)
    async for dialog in client.iter_dialogs():
        print(f"Chat Name: {dialog.name}, Chat ID: {dialog.id}")

# Start the client and run the main function
client.start()
client.loop.run_until_complete(main())
