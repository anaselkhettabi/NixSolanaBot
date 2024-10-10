from solana.rpc.api import Client
from solders.pubkey import Pubkey
from spl.token.instructions import get_associated_token_address
from spl.token.constants import TOKEN_PROGRAM_ID

# Function to get SPL token balance
def get_spl_token_balance(wallet_pubkey: Pubkey, token_mint: Pubkey):
    # Get the associated token account for the SPL token
    token_account = get_associated_token_address(wallet_pubkey, token_mint)

    # Query the token account balance
    response = solana_client.get_token_account_balance(token_account)
    if 'value' in response:
        amount = response['value']['amount']
        print(f"Token Balance for {token_mint}: {amount}")
    else:
        print("Unable to fetch the token balance.")

# Replace with your actual wallet public key and token mint address
wallet_pubkey = keypair.pubkey()  # Your wallet public key
token_mint = Pubkey.from_string("4LDT8u5BcVf2acdWJsqz45yaFsXBCsjY79ERLXX6pump")  # Replace with actual token mint

get_spl_token_balance(wallet_pubkey, token_mint)
