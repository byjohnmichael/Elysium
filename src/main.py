from bitcoinlib.wallets import Wallet
from cmd_utils import commands
# Main Loop
print("KeyStone Wallet. Version 0.1.0")
print("Starting Keystone Wallet...")
print("\nWelcome to KeyStone Wallet's console.\nType help for more information on commands.")

while True:
    cmd = input("(KEYSTONE)> ")
    parts = cmd.split(maxsplit=1)
    command = parts[0]
    args = parts[1] if len(parts) > 1 else None

    if command in commands:
        commands[command](args)  # Call the appropriate function
    else:
        print(f"Unknown command: {command}. Type 'help' for a list of commands.")
