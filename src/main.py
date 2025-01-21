from preferences import load_pref, set_pref
from cmd_utils import commands
pk = "vprv9QLAqrfm5tDgJKT6UzBMx1xAmBSeCW7mV6FtpHhisB6aiQ42tNH29DkT1r4cYKc72GDXTWtZN9rrMPQN3j4y7LPt4CJkj1Uhcn1EeUbmJrf"
# Main function
def main():
    # Entry point
    print("KeyStone Wallet. Version 0.1.0")
    print("Starting Keystone Wallet...")

    # Preferences
    print("Loading preferences file...")
    load_pref()
    print("Setting preferences...")
    set_pref()

    print("\nWelcome to KeyStone Wallet's console.\nType help for more information on commands.")
    # Waits for commands on console
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
main()