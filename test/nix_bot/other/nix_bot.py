import re
from telethon import TelegramClient, events
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solana.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solders.keypair import Keypair
from solana.rpc.commitment import Confirmed
from solana.rpc.core import RPCException
import json
import asyncio

# Replace with your actual API credentials
api_id = '25329515'
api_hash = 'fdb29fbe41dd3e020b8334a85f73ee6c'
group_id = -4563832468  # Replace with your group chat ID

# Initialize Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Initialize Solana RPC client (Helius RPC endpoint)
solana_client = Client("https://mainnet.helius-rpc.com/?api-key=b4e2d851-da90-46b8-96d9-7ca3c29ca8bd")

# Load your private key from a keypair file
def load_wallet_keypair(filepath):
    with open(filepath, "r") as file:
        secret_key = json.load(file)
        return Keypair.from_bytes(bytes(secret_key))  # Convert the list of integers to bytes

# Initialize your wallet's keypair
keypair = load_wallet_keypair("keypair.json")

# Function to extract Solana contract address from Telegram messages
def extract_solana_address(text):
    match = re.search(r'[A-Za-z0-9]{32,44}', text)  # Solana addresses are 32 to 44 alphanumeric characters
    return match.group(0) if match else None

# Function to validate if the contract address exists on Solana
def is_valid_solana_address(address):
    try:
        public_key = Pubkey.from_string(address)
        account_info = solana_client.get_account_info(public_key)
        
        # Access the 'value' field from the result of the account info response
        if account_info.value is None:
            return False
        return True
    except (ValueError, RPCException):  # Ensure you catch appropriate exceptions
        return False

# Function to interact with Raydium to perform the swap (real sniping)
async def snipe_token(contract_address):
    print(f"Sniping token with contract address: {contract_address}")
    
    # Set the amount of SOL to swap (example: 0.01 SOL)
    amount_in_sol = 0.001  # Modify this to adjust the amount you're swapping
    amount_in_lamports = int(amount_in_sol * 1_000_000_000)  # Convert SOL to lamports (1 SOL = 1e9 lamports)

    # Create the transfer instruction using the solders system program's transfer function
    transfer_instruction = transfer(
        TransferParams(
            from_pubkey=keypair.pubkey(),
            to_pubkey=Pubkey.from_string(contract_address),
            lamports=amount_in_lamports
        )
    )

    # Build and sign the transaction
    transaction = Transaction().add(transfer_instruction)

    # Send the transaction to the Solana blockchain
    response = solana_client.send_transaction(transaction, keypair)
    print(f"Transaction sent: {response.value}")  # Access response.value instead of subscripting

    # Wait for confirmation using the transaction signature from response.value
    confirmation = solana_client.confirm_transaction(response.value, commitment="confirmed")
    print(f"Transaction confirmed: {confirmation}")

# Event handler for new messages in the group
@client.on(events.NewMessage(chats=group_id))
async def handler(event):
    message = event.message
    if message.text:
        contract_address = extract_solana_address(message.text)
        if contract_address:
            if is_valid_solana_address(contract_address):
                print(f"Found valid token contract address: {contract_address}")
                await snipe_token(contract_address)  # Trigger the token snipe
            else:
                print(f"Invalid or non-existent contract address: {contract_address}")
        else:
            print("No valid contract address found in the message.")

# Function to print "Monitoring..." message periodically
async def show_monitoring_message():
    while True:
        print("Monitoring...")
        await asyncio.sleep(30)  # Wait 30 seconds before printing again

# Start the Telegram client and run it continuously
async def main():
    await client.start()
    print("Bot started. Monitoring for new messages...")
    asyncio.create_task(show_monitoring_message())
    await client.run_until_disconnected()

asyncio.run(main())
