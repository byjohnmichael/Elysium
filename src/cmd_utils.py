import time
from getpass import getpass
from preferences import preferences
from bitcoinlib.wallets import Wallet
from bitcoinlib.mnemonic import Mnemonic
# Global Variables
loaded_wallets = []
pref_network = preferences["network"]

# Helper Methods
def printt(message="", seconds=0):
    print(message)
    time.sleep(seconds)

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

# Command Handler Methods
def show_help(_):
    print("\nList of commands:\n"
          "help: Lists commands\n"
          "walkthrough: A guided way to create or restore a wallet "
          "walkthrough -tx <wallet_name>: A guided way to send, receive, or check your btc balance"
          "create <wallet_name>: Creates a wallet without revealing the 12 word seed\n"
          "restore <wallet_name> <seed>: Restores a wallet when provided with word seed"
          # "load <wallet_name>: Loads a wallet with a specific name\n"
          # "list <modifer>: Lists all loaded wallets\n"
          "send <wallet_name> <address> <amount>: Sends BTC from a wallet to a specified address\n"
          "receive <wallet_name>: Displays the receiving address for a wallet\n"
          "details <wallet_name>: Lists details of a specific wallet\n"
          "exit: Ends application\n")

def walkthrough(args):
    if args:
        parts = args.split()
        if parts[0] == "-tx":
            walkthrough_tx(parts[1])
        else:
            print("Error:\nIf you would like to walkthrough creating a wallet the usage is: walkthrough\n"
                  "If you would like to walkthrough a transaction the usage is: walkthrough -tx <wallet_name>")
        return
    printt("\nWELCOME TO A WALLET WALKTHROUGH", 1)
    answer = input("Did you want to restore a wallet?(y/n): ").strip().lower()
    while answer[0] != "y" or answer[0] != "n":
        if answer[0] == "y":
            wallet_name = input("Type a name to identify this restored wallet: ")
            restore_wallet(wallet_name)
            return
        elif answer[0] == "n":
            printt("Proceeding to wallet creation.", 1)
            time.sleep(1)
            wallet_name = input("Type a name to identify this wallet: ")
            # 12 word seed
            seed = Mnemonic().generate()
            # Raw binary seed
            raw_seed = Mnemonic().to_seed(seed)
            printt("This is your seed:\n"
                "\n***************************\n"
                f"{seed}\n"
                "***************************\n", 5)
            printt("Your seed is incredibly important as it's the human readable way to restore your wallet.", 3)
            printt("Write these 12 words down and keep them in a secure place that you can remember.", 3)
            repeated_seed = input("Once you are done backing up your 12 words, input your 12 words here to confirm, as they are displayed above: \n>")
            if repeated_seed == seed or repeated_seed == "skip":
                printt("Correct... creating wallet", 1)
            else:
                printt("Incorrect", 1)
                return
            create_wallet(wallet_name, seed=raw_seed)
            wallet_details(wallet_name, seed)
            printt("\nHere are the details of your newly created wallet.", 1)
            printt("This will be the last time the 12 word seed will be displayed.", 1)
            printt("You can also recover your wallet by using the private key which is displayed above, consider backing up the private key as well.", 3)
            getpass("\nPress enter to continue, after pressing enter the 12 word seed will be deleted from memory.")
            return

def walkthrough_tx(wallet_name):
    printt(f"\nWELCOME TO A TRANSACTION WALKTHROUGH ({wallet_name})", 1)
    wallet = Wallet(wallet_name)
    print("Requesting balance")
    balance = get_balance(wallet_name)
    printt(f"Balance for Wallet '{wallet_name}': {balance:.8f} BTC", 1)
    answer = input("What would you like to send, or receive? (s/r): ")
    while answer[0] != "s" or answer[0] != "r":
        if answer[0] == "s":
            address = input("Specify an address you would like to send btc to: ")
            amount = input("Specify the amount of btc you would like to send: ")
            send_btc(f"{wallet_name}, {address}, {amount}")
            return
        elif answer[0] == "r":
            printt(f"Here is your wallet address: {wallet.get_key().address}", 2)
            printt("Give this to the person who is sending you btc", 1)
            return

def create_wallet(args, seed=None):
    if args:
        try:
            wallet_name = args
            Wallet.create(
                name=wallet_name,
                keys=seed,
                network=pref_network,
                witness_type="segwit")
            print(f"Wallet '{wallet_name}' created successfully!")
        except Exception as e:
            print(f"Error: Could not create wallet. {e}")
    else:
        print("Error: Please specify a wallet name. Usage: create <wallet_name>")

def restore_wallet(args):
    if args:
        seed_phrase = input("Input 12 word seed: ")
        seed = Mnemonic().to_seed(seed_phrase)
        try:
            wallet = Wallet.create(
                name=args.strip(),
                keys=seed,
                network="testnet",
                witness_type="segwit"
            )
            print(f"Wallet '{wallet.name}' restored successfully!")
            print(f"First Receiving Address: {wallet.get_key().address}")
        except Exception as e:
            print(f"Error: Could not restore wallet. {e}")
    else:
        print("Error: Please provide a wallet name and the 12 word seed. Usage: restore <wallet_name> <seed>")

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

def exit_app(_):
    print("Exiting KeyStone Wallet...")
    exit()

# Command Mapping
commands = {
    "help": show_help,
    "walkthrough": walkthrough,
    "create": create_wallet,
    "restore": restore_wallet,
    # "load": load_wallet,
    # "list": list_wallets,
    "details": wallet_details,
    "send": send_btc,
    "receive": receive_btc,
    "balance": get_balance,
    "exit": exit_app
}
# Archived Functions
#def load_wallet(args):
#    if args:
#        wallet_name = args
#        try:
#            wallet = Wallet(wallet_name)
#            loaded_wallets.append(wallet)
#            print(f"Wallet '{wallet_name}' loaded successfully and added to the list of loaded wallets!")
#        except Exception as e:
#            print(f"Error: Could not load wallet '{wallet_name}'. {e}")
#    else:
#        print("Error: Please specify a wallet name. Usage: load <wallet_name>")
#
#def list_wallets(_):
#    if loaded_wallets:
#        print("\nLoaded Wallets:")
#        for wallet in loaded_wallets:
#            print(f"- {wallet.name}")
#    else:
#        print("No wallets are currently loaded.")
"""
TEST WALLET
JohnM

crisp blouse setup december appear duty wool few renew what husband service

tb1qqgre4zsy7x46svk9crqr427r0h6ruyjfremmdv

vprv9PEjKEnZDC2u3Do3TwpiRBeuuzKSC5hAuRUoVDrMUSuFsTGzrwaUx1H2iAgEcVWMbtwbKJcyn82CXgGNrZD9JtgSzuPZSf5VwGmJeq5T68M
"""