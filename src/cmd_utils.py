from bitcoinlib.wallets import Wallet

# List to store loaded wallets
loaded_wallets = []

# Command Handlers
def show_help(_):
    print("\nList of commands:\n"
          "help: Lists commands\n"
          "create <name>: Creates a wallet and assigns a name to it\n"
          "load <name>: Loads a wallet with a specific name\n"
          "list: Lists all loaded wallets\n"
          "exit: Ends application\n")

def create_wallet(args):
    if args:
        wallet_name = args
        wallet = Wallet.create(wallet_name, network='testnet')
        print(f"Wallet '{wallet_name}' created successfully!")
    else:
        print("Error: Please specify a wallet name. Usage: create <wallet_name>")

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

def exit_app(_):
    print("Exiting KeyStone Wallet...")
    exit()

# Command Mapping
commands = {
    "help": show_help,
    "create": create_wallet,
    "load": load_wallet,
    "list": list_wallets,
    "exit": exit_app,
}