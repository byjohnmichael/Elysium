from preferences import load_pref
from cmd_utils import commands
# Main function
def main():
    # Entry point
    print("KeyStone Wallet. Version 0.1.0")
    print("Starting Keystone Wallet...")

    # Preferences
    print("Loading preferences...")
    load_pref()

    # Main loop, waits for commands on console
    print("\nWelcome to KeyStone Wallet's console.\nType help for more information on commands.")
    while True:
        cmd = input("(KEYSTONE)> ")
        parts = cmd.split(maxsplit=1)
        command = parts[0]
        args = parts[1] if len(parts) > 1 else None
        if command in commands:
            # Call the appropriate function
            commands[command](args)
        else:
            print(f"Unknown command: {command}. Type 'help' for a list of commands.")
# Execution
main()