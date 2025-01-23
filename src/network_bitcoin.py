from bitcoinlib.wallets import Wallet
from bitcoinlib.mnemonic import Mnemonic


def get_balance(wallet_name):
    try:
        wallet = Wallet(wallet_name)
        wallet.scan()
        balance_satoshis = wallet.balance()
        balance_btc = balance_satoshis / 1e8
        return balance_btc
    except Exception as e:
        print(f"Error: Could not retrieve balance for wallet '{wallet_name}'. {e}")

def create_wallet_from_words(wallet_name, words):
    words = "crisp blouse setup december appear duty wool few renew what husband service"
    raw_seed = Mnemonic().to_seed(words)
    wallet = Wallet.create(name=wallet_name,
                keys=raw_seed,
                network="testnet",
                witness_type="segwit")
    
    print(f"\nDetails for Wallet '{wallet_name}':")
    print(f"- Balance: {get_balance(wallet_name)} BTC")
    print(f"- Address: {wallet.get_key().address}")
    print(f"- Private Key (WIF): {wallet.get_key().wif}")
    


def wallet_details(args, seed=None):
    if args:
        wallet_name = args
        try:
            wallet = Wallet(wallet_name)
            print(f"\nDetails for Wallet '{wallet_name}':")
            print(f"- Name: {wallet.name}")
            print(f"- Address: {wallet.get_key().address}")
            if seed != None:
                print(f"- 12 Word Seed: {seed}")
            print(f"- Private Key (WIF): {wallet.get_key().wif}")
        except Exception as e:
            print(f"Error: Could not retrieve details for wallet '{wallet_name}'. {e}")
    else:
        print("Error: Please specify a wallet name. Usage: details <wallet_name>")