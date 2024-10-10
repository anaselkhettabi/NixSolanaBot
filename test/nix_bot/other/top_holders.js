const { Connection, PublicKey } = require('@solana/web3.js');
const readline = require('readline');

// Initialize Solana connection
const connection = new Connection('https://api.mainnet-beta.solana.com');

// Set up readline to take user input
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Mock memecoin price feed (replace with an actual API)
const MEMECOINS = {
  "MemeCoin1MintAddress": { name: "MemeCoin1", price: 100 }, // Replace with actual price
  "MemeCoin2MintAddress": { name: "MemeCoin2", price: 200 }  // Replace with actual price
};

// Minimum criteria for memecoins (total value > $10,000)
const MIN_MEMECOIN_VALUE = 10000;

// Check if the owner has a memecoin worth more than $10K
async function getMemecoinData(ownerAddress) {
  try {
    const tokenAccounts = await connection.getTokenAccountsByOwner(new PublicKey(ownerAddress), { programId: new PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA") });

    let qualifyingMemecoins = [];

    for (let { account } of tokenAccounts.value) {
      const tokenInfo = account.data.parsed.info;
      const mintAddress = tokenInfo.mint;
      const amount = tokenInfo.tokenAmount.uiAmount;

      if (MEMECOINS[mintAddress]) {
        const memecoinValue = amount * MEMECOINS[mintAddress].price;

        if (memecoinValue > MIN_MEMECOIN_VALUE) {
          qualifyingMemecoins.push({ name: MEMECOINS[mintAddress].name, value: memecoinValue });
        }
      }
    }

    return qualifyingMemecoins;
  } catch (error) {
    console.error('Error fetching token accounts:', error);
  }
}

// Function to get top token holders and apply filtering based on memecoin value
async function getTopHolders(mintAddress) {
  try {
    const mintPublicKey = new PublicKey(mintAddress);
    const tokenAccounts = await connection.getTokenLargestAccounts(mintPublicKey);

    const accounts = tokenAccounts.value;
    if (!accounts.length) {
      console.log('No holders found.');
      return;
    }

    console.log(`Noteworthy Holders for token mint: ${mintAddress}`);
    for (let i = 0; i < accounts.length; i++) {
      const { address } = accounts[i];

      // Fetch memecoin data
      const memecoins = await getMemecoinData(address);

      if (memecoins.length > 0) {
        console.log(`Rank ${i + 1}: Address: ${address}`);
        memecoins.forEach(memecoin => {
          console.log(`Memecoin: ${memecoin.name}, Value: $${memecoin.value.toFixed(2)}`);
        });
      }
    }
  } catch (error) {
    console.error('Error fetching top holders:', error);
  }
}

// Prompt user for the token mint address
rl.question('Please enter the Solana token mint address: ', (input) => {
  if (!input) {
    console.log('No address entered. Exiting...');
    rl.close();
  } else {
    console.log(`Fetching noteworthy holders for token mint: ${input}`);
    getTopHolders(input);
    rl.close();
  }
});