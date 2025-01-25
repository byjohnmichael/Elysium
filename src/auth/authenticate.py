import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Simulated "hardware storage" file
HARDWARE_STORAGE_FILE = "password_storage.enc"

# Derive a hardware-specific encryption key (in a real-world scenario, this could be from a TPM)
def get_hardware_key():
    # Example: Derive from hardware properties or securely generate once
    return os.urandom(32)  # Replace with actual hardware-bound key logic

# Encrypt and save the password to hardware
def store_password(password: str):
    # Hash the password
    ph = PasswordHasher()
    hashed_password = ph.hash(password)

    # Encrypt the hashed password using AES-GCM
    aes_key = get_hardware_key()
    aesgcm = AESGCM(aes_key)
    nonce = os.urandom(12)  # Unique nonce for AES-GCM
    ciphertext = aesgcm.encrypt(nonce, hashed_password.encode(), None)

    # Save the nonce and ciphertext to the "hardware"
    with open(HARDWARE_STORAGE_FILE, "wb") as f:
        f.write(nonce + ciphertext)

    print("Password stored securely on hardware.")

# Load and verify the password
def verify_password(input_password: str) -> bool:
    # Load the encrypted password from the "hardware"
    aes_key = get_hardware_key()
    with open(HARDWARE_STORAGE_FILE, "rb") as f:
        data = f.read()

    nonce = data[:12]  # Extract the nonce
    ciphertext = data[12:]  # Extract the ciphertext

    # Decrypt the stored password hash
    aesgcm = AESGCM(aes_key)
    try:
        hashed_password = aesgcm.decrypt(nonce, ciphertext, None).decode()
    except Exception as e:
        print("Decryption failed:", str(e))
        return False

    # Verify the input password
    ph = PasswordHasher()
    try:
        ph.verify(hashed_password, input_password)
        print("Password verified successfully!")
        return True
    except VerifyMismatchError:
        print("Incorrect password.")
        return False

# Example usage
if __name__ == "__main__":
    # Store a password securely
    if not os.path.exists(HARDWARE_STORAGE_FILE):
        store_password("my_secure_password")

    # Simulate a login
    user_input = input("Enter your password: ")
    if verify_password(user_input):
        print("Access granted!")
    else:
        print("Access denied!")
