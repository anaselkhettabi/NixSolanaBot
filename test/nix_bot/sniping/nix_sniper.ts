import { Connection, PublicKey, Keypair } from '@solana/web3.js';
import { Jupiter, RouteInfo } from '@jup-ag/api';
import JSBI from 'jsbi';  // Import JSBI for handling large numbers

// Set up Solana connection and keypair
const connection = new Connection('https://mainnet.helius-rpc.com/?api-key=b4e2d851-da90-46b8-96d9-7ca3c29ca8bd');
const walletKeypair = Keypair.fromSecretKey(new Uint8Array([/* Your Secret Key Array */]));

async function snipeToken(tokenMintAddress: string): Promise<void> {
    console.log(`Attempting to snipe token: ${tokenMintAddress}`);
    
    const inputMint = new PublicKey("So11111111111111111111111111111111111111112");  // SOL Mint
    const outputMint = new PublicKey(tokenMintAddress);  // Detected token mint address

    try {
        // Load Jupiter instance
        const jupiter = await Jupiter.load({
            connection,
            cluster: 'mainnet-beta',
            user: walletKeypair,
        });

        // Convert amount to JSBI
        const amountInLamports = JSBI.BigInt(0.001 * 1_000_000_000);  // Amount in lamports

        // Get the best route to swap SOL for the token
        const { routesInfos } = await jupiter.computeRoutes({
            inputMint,
            outputMint,
            amount: amountInLamports,  // Use JSBI for the amount
            slippageBps: 50,  // 0.5% slippage (50 bps)
        });

        const routes: RouteInfo[] = routesInfos;

        if (routes.length > 0) {
            const bestRoute = routes[0];
            console.log('Best route found:', bestRoute);

            // Execute the swap
            const { execute } = await jupiter.exchange({ routeInfo: bestRoute });
            const swapResult = await execute();

            // Log the result of the swap
            console.log('Swap result:', swapResult);
        } else {
            console.log('No route found for the swap. The token may not be tradable yet.');
        }
    } catch (error: any) {  // Type 'any' used for generic error handling
        console.error('Error during the swap process:', error);
        if (error.message.includes('Tick')) {
            console.log('The token may not be supported by Raydium CLMM. Trying a different DEX...');
            // You can implement fallback logic to try other DEXs here.
        }
    }
}

// Get the contract address from the command-line argument
const tokenContractAddress: string = process.argv[2];
if (tokenContractAddress) {
    snipeToken(tokenContractAddress).catch(console.error);
} else {
    console.error('No token contract address provided.');
}
