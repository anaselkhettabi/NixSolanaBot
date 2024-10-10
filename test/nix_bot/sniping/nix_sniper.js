"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
exports.__esModule = true;
var web3_js_1 = require("@solana/web3.js");
var core_1 = require("@jup-ag/core");
var jsbi_1 = require("jsbi"); // Import JSBI for large number handling
// Set up Solana connection and keypair
var connection = new web3_js_1.Connection('https://mainnet.helius-rpc.com/?api-key=b4e2d851-da90-46b8-96d9-7ca3c29ca8bd');
var walletKeypair = web3_js_1.Keypair.fromSecretKey(new Uint8Array([ /* Your Secret Key Array */]));
function snipeToken(tokenMintAddress) {
    return __awaiter(this, void 0, void 0, function () {
        var inputMint, outputMint, jupiter, amountInLamports, _a, routesInfos, cached, routes, bestRoute, execute, swapResult, error_1;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    console.log("Attempting to snipe token: ".concat(tokenMintAddress));
                    inputMint = new web3_js_1.PublicKey("So11111111111111111111111111111111111111112");
                    outputMint = new web3_js_1.PublicKey(tokenMintAddress);
                    _b.label = 1;
                case 1:
                    _b.trys.push([1, 8, , 9]);
                    return [4 /*yield*/, core_1.Jupiter.load({
                            connection: connection,
                            cluster: 'mainnet-beta',
                            user: walletKeypair
                        })];
                case 2:
                    jupiter = _b.sent();
                    amountInLamports = jsbi_1["default"].BigInt(0.001 * 1000000000);
                    return [4 /*yield*/, jupiter.computeRoutes({
                            inputMint: inputMint,
                            outputMint: outputMint,
                            amount: amountInLamports,
                            slippageBps: 50
                        })];
                case 3:
                    _a = _b.sent(), routesInfos = _a.routesInfos, cached = _a.cached;
                    routes = routesInfos;
                    if (!(routes.length > 0)) return [3 /*break*/, 6];
                    bestRoute = routes[0];
                    console.log('Best route found:', bestRoute);
                    return [4 /*yield*/, jupiter.exchange({ routeInfo: bestRoute })];
                case 4:
                    execute = (_b.sent()).execute;
                    return [4 /*yield*/, execute()];
                case 5:
                    swapResult = _b.sent();
                    // Log the full swap result for inspection
                    console.log('Full swap result:', swapResult);
                    // Check if there's any transaction information in the result
                    if (swapResult) {
                        console.log('Transaction result:', JSON.stringify(swapResult, null, 2));
                    }
                    else {
                        console.log('Transaction did not return expected result.');
                    }
                    return [3 /*break*/, 7];
                case 6:
                    console.log('No route found for the swap. The token may not be tradable yet.');
                    _b.label = 7;
                case 7: return [3 /*break*/, 9];
                case 8:
                    error_1 = _b.sent();
                    console.error('Error during the swap process:', error_1);
                    if (error_1.message.includes('Tick')) {
                        console.log('The token may not be supported by Raydium CLMM. Trying a different DEX...');
                        // You can implement fallback logic to try other DEXs here.
                    }
                    return [3 /*break*/, 9];
                case 9: return [2 /*return*/];
            }
        });
    });
}
// Get the contract address from the command-line argument
var tokenContractAddress = process.argv[2];
if (tokenContractAddress) {
    snipeToken(tokenContractAddress)["catch"](console.error);
}
else {
    console.error('No token contract address provided.');
}
