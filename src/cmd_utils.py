import requests
from bitcoinlib.wallets import Wallet
DEBUG = True
# List to store loaded wallets
loaded_wallets = []

# Command Handlers
def show_help(_):
    print("\nList of commands:\n"
          "help: Lists commands\n"
          "create <name>: Creates a wallet and assigns a name to it\n"
          "load <name>: Loads a wallet with a specific name\n"
          "list: Lists all loaded wallets\n"
          "details <name>: Lists details of a specific wallet\n"
          "send <name> <address> <amount>: Sends BTC from a wallet to a specified address\n"
          "receive <name>: Displays the receiving address for a wallet\n"
          "balance <name>: Retrieves the balance of a wallet\n"
          "debug: Versatile function with multiple purposes, only can be called when in debug mode"
          "exit: Ends application\n")

def create_wallet(args):
    if args:
        wallet_name = args
        wallet = Wallet.create(wallet_name, network='testnet')
        print(f"Wallet '{wallet_name}' created successfully!")
    else:
        print("Error: Please specify a wallet name. Usage: create <wallet_name>")

def restore_wallet(args):
    if args:
        parts = args.split()
        if len(parts) == 2:
            wallet_name, private_key = parts
            try:
                wallet = Wallet.create(wallet_name, private_key, network="testnet", witness_type="segwit", key_path="m/84'/1'/0'")
                print(f"Wallet '{wallet_name}' restored successfully!")
                print(f"Address: {wallet.get_key().address}")
            except Exception as e:
                print(f"Error: Could not restore wallet '{wallet_name}'. {e}")
        else:
            print("Error: Usage: restore <wallet_name> <private_key>")
    else:
        print("Error: Please provide a wallet name and private key. Usage: restore <wallet_name> <private_key>")

def load_wallet(args):
    if args:
        wallet_name = args
        try:
            wallet = Wallet(wallet_name)
            loaded_wallets.append(wallet)
            print(f"Wallet '{wallet_name}' loaded successfully and added to the list of loaded wallets!")
        except Exception as e:
            print(f"Error: Could not load wallet '{wallet_name}'. {e}")
    else:
        print("Error: Please specify a wallet name. Usage: load <wallet_name>")

def list_wallets(_):
    if loaded_wallets:
        print("\nLoaded Wallets:")
        for wallet in loaded_wallets:
            print(f"- {wallet.name}")
    else:
        print("No wallets are currently loaded.")

def wallet_details(args):
    if args:
        wallet_name = args
        try:
            wallet = Wallet(wallet_name)
            print(f"\nDetails for Wallet '{wallet_name}':")
            print(f"- Name: {wallet.name}")
            print(f"- Address: {wallet.get_key().address}")
            print(f"- Private Key (WIF): {wallet.get_key().wif}")
        except Exception as e:
            print(f"Error: Could not retrieve details for wallet '{wallet_name}'. {e}")
    else:
        print("Error: Please specify a wallet name. Usage: details <wallet_name>")

def send_btc(args):
    if args:
        parts = args.split()
        if len(parts) == 3:
            wallet_name, address, amount = parts
            try:
                wallet = Wallet(wallet_name)
                tx = wallet.send_to(address, amount)
                print(f"Transaction sent! TXID: {tx.txid}")
            except Exception as e:
                print(f"Error: Could not send BTC. {e}")
        else:
            print("Error: Usage: send <name> <address> <amount>")
    else:
        print("Error: Please provide wallet name, address, and amount. Usage: send <name> <address> <amount>")

def receive_btc(args):
    if args:
        wallet_name = args
        try:
            wallet = Wallet(wallet_name)
            print(f"Receiving Address for Wallet '{wallet_name}': {wallet.get_key().address}")
        except Exception as e:
            print(f"Error: Could not retrieve receiving address for wallet '{wallet_name}'. {e}")
    else:
        print("Error: Please specify a wallet name. Usage: receive <name>")

# Get Balance  function (get_incoming_balance is a helper function for the balance function)
def get_incoming_balance(wallet_name):
    print("Work in progress")
    return
    try:
        wallet = Wallet(wallet_name)
        address = wallet.get_key().address
        url = f"https://blockstream.info/testnet/api/address/{address}/txs"
        response =  requests.get(url)
        transactions = response.json()
        for tx in transactions:
            if tx['status']['confirmed'] == False:
                print(f"Unconfirmed Transaction: {tx['txid']}")
    except Exception as e:
        print(f"Error: Could not retrieve balance for wallet '{wallet_name}'. {e}")
def get_balance(args):
    if args:
        parts = args.split()
        # -i modifer for incoming balance
        if len(parts) == 2:
            wallet_name, modifer = parts
            try:
                if modifer == "-i":
                    get_incoming_balance(wallet_name)
            except Exception as e:
                print(f"Error: '{modifer}' is not a valid modifer. {e}")
        # no modifer for confirmed balance
        elif len(parts) == 1:
            wallet_name = parts
            try:
                wallet = Wallet(wallet_name)
                wallet.scan()
                balance = wallet.balance()
                print(f"Balance for Wallet '{wallet_name}': {balance} BTC")
            except Exception as e:
                print(f"Error: Could not retrieve balance for wallet '{wallet_name}'. {e}")
    else:
        print("Error: Please specify a wallet name. Usage: balance <name>")

def exit_app(_):
    print("Exiting KeyStone Wallet...")
    exit()

def debug(_):
    if DEBUG == True:
        print("ENTERING DEBUG MODE...")
        try:
            from bitcoinlib.keys import Key, HDKey
            from bip_utils import Bip32Utils
            pk = "vprv9QLAqrfm5tDgJKT6UzBMx1xAmBSeCW7mV6FtpHhisB6aiQ42tNH29DkT1r4cYKc72GDXTWtZN9rrMPQN3j4y7LPt4CJkj1Uhcn1EeUbmJrf"
            bip32_obj = Bip32.FromExtendedKey(pk)
            tprv_key = bip32_obj.ConvertToNetwork(Bip32Utils.TestNet())
            print(f"Converted tprv Key: {tprv_key}")
        except Exception as e:
            print(f"{e}")
        print("DEBUG MODE ENDED")
    else:
        print("Only avaliable in debug mode")

# Command Mapping
commands = {
    "help": show_help,
    "create": create_wallet,
    "restore": restore_wallet,
    "load": load_wallet,
    "list": list_wallets,
    "details": wallet_details,
    "send": send_btc,
    "receive": receive_btc,
    "balance": get_balance,
    "exit": exit_app,
    "debug": debug
}