# filename: nix_monitor.py

import re
import subprocess
from telethon import TelegramClient, events

# Replace with your actual API credentials
api_id = '25329515'
api_hash = 'fdb29fbe41dd3e020b8334a85f73ee6c'
group_id = -4563832468  # Replace with your group chat ID

# Initialize Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Function to extract Solana contract address from Telegram messages
def extract_solana_address(text):
    match = re.search(r'[A-Za-z0-9]{32,44}', text)  # Solana addresses are 32 to 44 alphanumeric characters
    return match.group(0) if match else None

# Function to call JS/TS script to snipe the token
def trigger_js_script(contract_address):
    # Call the JS/TS script via command line and pass the contract address as an argument
    subprocess.run(['node', '/home/misterdoco/test/nix_bot/sniping/nix_sniper.js', contract_address])

# Event handler for new messages in the group
@client.on(events.NewMessage(chats=group_id))
async def handler(event):
    message = event.message
    if message.text:
        contract_address = extract_solana_address(message.text)
        if contract_address:
            print(f"Found valid token contract address: {contract_address}")
            trigger_js_script(contract_address)  # Trigger the token snipe script
        else:
            print("No valid contract address found in the message.")

# Start the Telegram client, display launch message, and run it continuously
async def main():
    print("Bot started. Listening for messages...")
    await client.start()
    await client.run_until_disconnected()

# Run the main function
client.loop.run_until_complete(main())
