from bitcoinlib.wallets import Wallet
from bitcoinlib.mnemonic import Mnemonic

def create_wallet_from_words(wallet_name, words):
    raw_seed = Mnemonic().to_seed(words)
    print(raw_seed)
    wallet = Wallet.create(name=wallet_name,
                keys=raw_seed,
                network="testnet",
                witness_type="segwit")
    # Print details (optional)
    if False:
        try:
            print(f"Wallet Name: {wallet.name}")
            print(f"Wallet Network: tesnet")
            print(f"Wallet Balance: {get_balance(wallet_name)} BTC")
            print(f"Wallet Key: {wallet.get_key().wif}")
            print(f"Receiving Address: {wallet.get_key().address}")
            print("Addresses:")
            for address in wallet.addresslist():
                print(f"- {address}")
            print("Transactions:")
            for tx in wallet.transactions():
                print(f"- TXID: {tx.txid}, Amount: {tx.amount}, Confirmed: {tx.confirmed}")
        except Exception as e:
            print(f"Error: Could not retrieve details for wallet '{wallet_name}'. {e}")

def send(wallet_name, address, amnt):
    try:
        wallet = Wallet(wallet_name)
        amnt = int(amnt * 1e8)
        tx = wallet.send_to(to_address=address, amount=amnt, broadcast=True)
        print(f"SENT! {tx.txid}")
        return tx
    except Exception as e:
        print(f"Error: Could not send BTC. {e}")

# HELPER METHODS
def gen_seed():
    seed = Mnemonic().generate()
    return seed

def get_balance(wallet_name):
    try:
        wallet = Wallet(wallet_name)
        wallet.scan()
        #wallet.utxos_update()
        balance_satoshis = wallet.balance()
        balance_btc = balance_satoshis / 1e8
        return balance_btc
    except Exception as e:
        print(f"Error: Could not retrieve balance for wallet '{wallet_name}'. {e}")

def get_address(wallet_name):
    try:
        wallet = Wallet(wallet_name)
        return wallet.get_key().address
    except Exception as e:
        print(f"Error: Could not retrieve balance for wallet '{wallet_name}'. {e}")