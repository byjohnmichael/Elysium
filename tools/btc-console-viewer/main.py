from cmd import commands
# Main function
def main():
    print("BTC Console Viewer. Version 0.1.0")
    # Main loop, waits for commands on console
    print("Type help for more information on commands.")
    while True:
        cmd = input("(KEYSTONE)> ")
        parts = cmd.split(maxsplit=1)
        command = parts[0]
        args = parts[1] if len(parts) > 1 else None
        if command in commands:
            commands[command](args)
        else:
            print(f"Unknown command: {command}. Type 'help' for a list of commands.")
main()