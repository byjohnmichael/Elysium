# BLOCKCHAIN PACKAGES
from bitcoinlib.wallets import Wallet   # BITCOIN
from web3 import Web3                   # ETHERUEM
from eth_account import Account         # ETHERUEM
from stellar_sdk import Keypair         # STELLAR
from stellar_sdk import Server          # STELLAR

# OTHER PACKAGES
from cryptography.fernet import Fernet  # FOR CIPHER
from mnemonic import Mnemonic           # FOR GENERATING 12 WORD SEEDS
import requests                         # FOR INTERNET REQUESTS
import sqlite3                          # FOR DATABASE HANDLING
import hashlib                          # FOR STELLAR SUPPORT
import hmac                             # FOR STELLAR SUPPORT
import json
import sys
import os

###
# INIT METHOD
###
def init():
    # CONNECT TO ETHERUEM
    print("Connecting to the Etheruem network(Sepolia Testnet)")
    sepolia_url = "https://sepolia.infura.io/v3/23475d24beea4c9485db4586f06cfa7e"
    w3 = Web3(Web3.HTTPProvider(sepolia_url))
    print(f"Connected to Sepolia: {w3.is_connected()}")

    # GENERATING THE CIPHER
    if not os.path.exists(".key"):
        print("Generating cipher")
        try:
            cipher = Fernet.generate_key()
            with open(".key", "wb") as file:
                file.write(cipher)
        except Exception as e:
            print(f"Could not retrieve the cipher. {e}")

    # GENERATING WALLET DATABASE
    if not os.path.exists("wallets.db"):
        print("Generating wallet database")
        try:
            conn = sqlite3.connect("wallets.db")
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS wallets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    encrypted_private_key TEXT NOT NULL,
                    network TEXT NOT NULL
                )
            """)
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

###
# DATA MANAGER METHODS
### 
def save(wallet_name, private_key, network):
    # LOADING CIPHER
    try:
        with open(".key", "rb") as file:
            cipher = Fernet(file.read())
        epk = cipher.encrypt(private_key.encode()).decode()
    except Exception as e:
        print(f"Could not retrieve the cipher. {e}")

    # SAVING TO DATABASEcc
    try:
        conn = sqlite3.connect("wallets.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO wallets (name, encrypted_private_key, network) VALUES (?, ?, ?)", 
                    (wallet_name, epk, network))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

def load(wallet_name, network):
    # LOADING CIPHER
    try:
        with open(".key", "rb") as file:
            cipher = Fernet(file.read())
    except Exception as e:
        print(f"Error: Could not retrieve the cipher. {e}")

    # LOADING PRIVATE KEY FROM DATABASE
    try:
        conn = sqlite3.connect("wallets.db")
        cursor = conn.cursor()
        cursor.execute("SELECT encrypted_private_key FROM wallets WHERE name = ? AND network = ?", (wallet_name, network))
        result = cursor.fetchone()
        if result is not None:
            encrypted_private_key = result[0]
            conn.close()
            private_key = cipher.decrypt(encrypted_private_key.encode()).decode()
            return private_key
        else:
            return None
    except Exception as e:
        print(f"Error: Could not retrieve the private key: {e}")

###
# COMMAND HANDLER METHODS
###
def help(*_):
    print("\nList of commands:\n"
        "help: Show all commands\n"
        "mode <network>: Switch blockchain (bitcoin, ethereum, solana)\n"
        "create <wallet_name>: Create a new wallet\n"
        "restore <wallet_name>: Restore a wallet using a seed or private key\n"
        "send <wallet_name> <address> <amount>: Send assets to an address\n"
        "receive <wallet_name>: Show the wallet’s receiving address\n"
        "balance <wallet_name>: Show the balance of the wallet\n"
        "fund <wallet_name>: Fund the wallets account. Exclusive to the Stellar testnet"
        "exit: Close the application\n")

def mode(args, mode=None):
    if args in {"bitcoin", "etheruem", "solana", "stellar"}:
        return args
    else:
        return None

def create(args, mode=None):
    if args and mode != None:
        try:
            wallet_name = args
            mnemo = Mnemonic('english')
            seed = mnemo.generate(strength=128)
            raw_seed = mnemo.to_seed(seed)
            initialize(wallet_name, raw_seed, mode)
            print(f"Wallet '{wallet_name}' created successfully!")
            print(f"Your seed phrase: {seed}")
        except Exception as e:
            print(f"Error: Could not create wallet. {e}")
    else:
        if mode == None:
            print("Error: Network was not specified, run the 'mode' command. Usage: mode <network>")
            return
        print("Error: Wallet name was not specified. Usage: create <wallet_name>")

def restore(args, mode=None):
    if args and mode != None:
            try:
                wallet_name = args
                seed = input("Input seed or private key")
                mnemo = Mnemonic('english')
                raw_seed = mnemo.to_seed(seed)
                initialize(wallet_name, raw_seed, mode)
                print(f"Wallet '{wallet_name}' restored successfully!")
            except Exception as e:
                print(f"Error: Could not restore wallet. {e}")
    else:
        if mode == None:
            print("Error: Network was not specified, run the 'mode' command. Usage: mode <network>")
            return
        print("Error: Wallet name was not specified. Usage: restore <wallet_name>")

def initialize(wallet_name, raw_seed, mode):
    try:
        match mode:
            case "bitcoin":
                wallet = Wallet.create(name=wallet_name, keys=raw_seed, network="testnet", witness_type="segwit")
                private_key = wallet.get_key().wif
                save(wallet_name, private_key, mode)
            case "etheruem":
                sepolia_url = "https://sepolia.infura.io/v3/23475d24beea4c9485db4586f06cfa7e"
                w3 = Web3(Web3.HTTPProvider(sepolia_url))
                eth_acc = w3.eth.account.from_key(raw_seed[:32].hex())
                private_key = eth_acc.key.hex()
                save(wallet_name, private_key, mode)
            case "solana":
                return
            case "stellar":
                public_key = hmac.new(b"ed25519 seed", raw_seed[:32], hashlib.sha512).digest()
                keypair = Keypair.from_raw_ed25519_seed(public_key[:32])
                private_key = keypair.secret
                save(wallet_name, private_key, mode)
    except Exception as e:
        print(f"Error: could not initialize wallet. {e}") 

def send(args, mode=None):
    if args and mode != None:







        # TODO SEPERATE NETWOKRS
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
        if mode == None:
            print("Error: Network was not specified, run the 'mode' command. Usage: mode <network>")
            return
        print("Error: Please provide wallet name, address, and amount. Usage: send <name> <address> <amount>")

def receive(args, mode=None):
    if args and mode != None:
        try:
            wallet_name = args
            match mode:
                case "bitcoin":
                    return
                case "etheruem":
                    return
                case "solana":
                    return
                case "stellar":
                    private_key = load(wallet_name, mode)
                    keypair = Keypair.from_secret(private_key)
                    print(f"Address: {keypair.public_key}")
        except Exception as e:
            print(f"Error: Could not retrieve address for wallet '{wallet_name}'. {e}")
    else:
        if mode == None:
            print("Error: Network was not specified, run the 'mode' command. Usage: mode <network>")
            return
        print("Error: Wallet name was not specified. Usage: receive <wallet_name>")

def balance(args, mode=None):
    if args:
        try:
            wallet_name = args
            match mode:
                case "bitcoin":
                    wallet = Wallet(wallet_name)
                    wallet.scan()
                    wallet.utxos_update()
                    balance_satoshis = wallet.balance()
                    balance_btc = balance_satoshis / 1e8
                    print(f"Balance: BTC: {balance_btc}")
                case "etheruem":
                    private_key = load(wallet_name, mode)
                    sepolia_url = "https://sepolia.infura.io/v3/23475d24beea4c9485db4586f06cfa7e"
                    w3 = Web3(Web3.HTTPProvider(sepolia_url))
                    eth_acc = w3.eth.account.from_key(private_key)
                    balance_wei = w3.eth.get_balance(eth_acc.address)
                    balance_eth = w3.from_wei(balance_wei, 'ether')
                    print(f"Balance ETH: {balance_eth}")
                case "solana":
                    return
                case "stellar":
                    server = Server("https://horizon-testnet.stellar.org")
                    private_key = load(wallet_name, mode)
                    keypair = Keypair.from_secret(private_key)
                    account = server.accounts().account_id(keypair.public_key).call()
                    for balance in account['balances']:
                        print(f"Balance {balance['asset_type']}: {balance['balance']}")
                case _:
                    return
        except Exception as e:
            print(f"Error: Could not retrieve balance for wallet '{wallet_name}'. {e}")
    else:
        if mode == None:
            print("Error: Network was not specified, run the 'mode' command. Usage: mode <network>")
            return
        print("Error: Wallet name was not specified. Usage: balance <wallet_name>")

def fund(args, mode=None):
    if args and mode == "stellar":
        try:
            wallet_name = args
            private_key = load(wallet_name, mode)
            keypair = Keypair.from_secret(private_key)
            response = requests.get(f"https://friendbot.stellar.org?addr={keypair.public_key}")
            if response.status_code == 200:
                print("Account funded")
            else:
                print("Failed to fund account")
        except Exception as e:
            print(f"Error: Could not fund for wallet '{wallet_name}'. {e}")
    else:
        if mode == None:
            print("Error: The 'fund' method is exclusive to the Stellar testnet, switch networks using the 'mode' method. Usage: mode <network>")
            return
        print("Error: Wallet name was not specified. Usage: fund <wallet_name>")

def exit(*_):
    print("Exiting KeyStone Wallet...")
    sys.exit(0)

# Command Mapping
commands = {
    "help": help,
    "mode": mode,
    "create": create,
    "restore": restore,
    "send": send,
    "receive": receive,
    "balance": balance,
    "fund": fund,
    "exit": exit
}

###
# MAIN METHOD
###
def main():
    if True:
        init()
    print("ELYSIUM COMMAND. Version 0.1.0")
    # Main loop, waits for commands on console
    print("Type 'help' for more information on commands. Use the mode command to choose which blockchain to operate on.")
    print("Defaulting to the stellar network")
    mode = "stellar"
    while True:
        cmd = None
        if mode != None:
            cmd = input(f"(ELY-{mode})> ")
        else:
            cmd = input("(ELYSIUM)> ")
        parts = cmd.split(maxsplit=1)
        command = parts[0]
        args = parts[1] if len(parts) > 1 else None
        if command in commands:
            if parts[0] == "mode":
                mode = commands[command](args, mode)
            elif parts[0] == "balance":
                print(commands[command](args, mode))
            else:
                commands[command](args, mode)
        else:
            print(f"Unknown command: {command}. Type 'help' for a list of commands.")
main()