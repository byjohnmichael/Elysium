from bitcoinlib.wallets import Wallet
from bitcoinlib.mnemonic import Mnemonic

# Command Handler Methods
def show_help(_):
    print("\nList of commands:\n"
          "help: Lists commands\n"
          "create <wallet_name>: Creates a wallet without revealing the 12 word seed\n"
          "send <wallet_name> <address> <amount>: Sends BTC from a wallet to a specified address\n"
          "details <wallet_name>: Lists details of a specific wallet\n"
          "exit: Ends application\n")

def create_wallet(args):
    if args:
        try:
            seed = input("Input seed, if none type 'no'")
            if seed == "no":
                raw_seed = None
            else:
                raw_seed = Mnemonic().to_seed(seed)
            wallet_name = args
            Wallet.create(
                name=wallet_name,
                keys=raw_seed,
                network="testnet",
                witness_type="segwit")
            print(f"Wallet '{wallet_name}' created successfully!")
        except Exception as e:
            print(f"Error: Could not create wallet. {e}")
    else:
        print("Error: Please specify a wallet name. Usage: create <wallet_name>")

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


def get_balance(args):
    if args:
        wallet_name = args
        try:
            wallet = Wallet(wallet_name)
            wallet.scan()
            balance_satoshis = wallet.balance()
            balance_btc = balance_satoshis / 1e8
            return balance_btc
        except Exception as e:
            print(f"Error: Could not retrieve balance for wallet '{wallet_name}'. {e}")
    else:
        print("Error: Wallet name was not specified.")



 
def wallet_details(args):
    if args:
        wallet_name = args
        try:
            wallet = Wallet(wallet_name)
            print(f"\nDetails for Wallet '{wallet_name}':")
            print(f"- Balance: {get_balance(wallet_name)} BTC")        
            print(f"- Address: {wallet.get_key().address}")
            print(f"- Private Key (WIF): {wallet.get_key().wif}")
        except Exception as e:
            print(f"Error: Could not retrieve details for wallet '{wallet_name}'. {e}")
    else:
        print("Error: Please specify a wallet name. Usage: details <wallet_name>")

def exit_app(_):
    print("Exiting KeyStone Wallet...")
    exit()

# Command Mapping
commands = {
    "help": show_help,
    "create": create_wallet,
    "details": wallet_details,
    "send": send_btc,
    "exit": exit_app
}

"""
TEST WALLET
JohnM

crisp blouse setup december appear duty wool few renew what husband service

tb1qqgre4zsy7x46svk9crqr427r0h6ruyjfremmdv

vprv9PEjKEnZDC2u3Do3TwpiRBeuuzKSC5hAuRUoVDrMUSuFsTGzrwaUx1H2iAgEcVWMbtwbKJcyn82CXgGNrZD9JtgSzuPZSf5VwGmJeq5T68M
"""