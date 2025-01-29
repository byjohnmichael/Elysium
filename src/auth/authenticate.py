import json
import os
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Initialize password hasher
ph = PasswordHasher()

# AES encryption key (store securely in your application)
ENCRYPTION_KEY = AESGCM.generate_key(bit_length=256)

# Define the secure file path for account storage
APP_NAME = "ElysiumApp"
APP_DATA_FOLDER = os.path.join(os.getenv("APPDATA"), APP_NAME)  # For Windows
os.makedirs(APP_DATA_FOLDER, exist_ok=True)  # Create the folder if it doesn't exist
ACCOUNT_FILE_PATH = os.path.join(APP_DATA_FOLDER, "accounts.json")


def load_accounts(filename=ACCOUNT_FILE_PATH):
    """Load accounts from a JSON file."""
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # Return an empty dict if the file doesn't exist

def save_accounts(accounts, filename=ACCOUNT_FILE_PATH):
    """Save accounts to a JSON file."""
    with open(filename, "w") as file:
        json.dump(accounts, file, indent=4)


def create_account(username, main_password, secondary_password):
    """Create a new account."""
    accounts = load_accounts()

    if username in accounts:
        print("Error: Username already exists!")
        return

    # Hash the main password
    hashed_password = ph.hash(main_password)

    # Encrypt the secondary password
    aesgcm = AESGCM(ENCRYPTION_KEY)
    nonce = os.urandom(12)  # Generate a unique nonce for this encryption
    encrypted_secondary = aesgcm.encrypt(nonce, secondary_password.encode(), None)

    # Store account details
    accounts[username] = {
        "hashed_password": hashed_password,
        "secondary_password": encrypted_secondary.hex(),  # Store as hex
        "nonce": nonce.hex()  # Store nonce as hex
    }

    save_accounts(accounts)
    print(f"Account for '{username}' created successfully!")


def login_with_main_password(username, main_password):
    """Login using the main password."""
    accounts = load_accounts()

    if username not in accounts:
        print("Error: Username not found!")
        return False

    # Verify main password
    try:
        stored_hash = accounts[username]["hashed_password"]
        ph.verify(stored_hash, main_password)
    except VerifyMismatchError:
        print("Error: Incorrect main password!")
        return False

    print("Login successful with main password!")
    return True


def login_with_secondary_password(username, secondary_password):
    """Login using the secondary password."""
    accounts = load_accounts()

    if username not in accounts:
        print("Error: Username not found!")
        return False

    try:
        # Retrieve the encrypted secondary password and nonce
        encrypted_secondary = bytes.fromhex(accounts[username]["secondary_password"])
        nonce = bytes.fromhex(accounts[username]["nonce"])

        # Decrypt the secondary password
        aesgcm = AESGCM(ENCRYPTION_KEY)
        decrypted_secondary = aesgcm.decrypt(nonce, encrypted_secondary, None).decode()

        # Check if the input matches the decrypted secondary password
        if secondary_password == decrypted_secondary:
            print("Login successful with secondary password!")
            return True
        else:
            print("Error: Incorrect secondary password!")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False


# Example Usage
if __name__ == "__main__":
    # Create an account
    create_account("user1", "mainpassword123", "mysecondarypassword")

    # Login using the main password
    login_with_main_password("user1", "mainpassword123")

    # Login using the secondary password
    login_with_secondary_password("user1", "mysecondarypassword")
