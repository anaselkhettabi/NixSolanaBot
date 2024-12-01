from solders.keypair import Keypair
import base64
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import asyncio

# Load the encryption secret
load_dotenv()
ENCRYPTION_SECRET = os.getenv("ENCRYPTION_SECRET")
cipher = Fernet(ENCRYPTION_SECRET)

def create_wallet():
    wallet = Keypair()
    wallet_public_key = str(wallet.pubkey())  # Use pubkey() to get the public key
    private_key_raw = base64.b64encode(bytes(wallet)).decode('utf-8')  # Encode the private key in base64
    
    # Encrypt the private key
    wallet_private_key = cipher.encrypt(private_key_raw.encode('utf-8')).decode('utf-8')
    
    return wallet_public_key, wallet_private_key

# def decrypt_private_key(encrypted_private_key):
#    decrypted_private_key = cipher.decrypt(encrypted_private_key.encode('utf-8')).decode('utf-8')
#    return decrypted_private_key
# Chat ID: 6867362512

async def check_wallet_balance(public_key):
    # Dummy implementation
    # Replace with actual Solana RPC API integration
    return 0.01
