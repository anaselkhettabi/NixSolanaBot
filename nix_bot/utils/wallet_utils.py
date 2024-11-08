from solana.keypair import Keypair
from cryptography.fernet import Fernet
import base64

encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

def create_wallet():
    wallet = Keypair()
    public_key = str(wallet.public_key)
    encrypted_private_key = cipher_suite.encrypt(base64.b64encode(wallet.secret_key))
    return public_key, encrypted_private_key.decode('utf-8')
