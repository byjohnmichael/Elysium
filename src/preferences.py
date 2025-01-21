import os
import json
PREFERENCES_FILE = "preferences.json"
DEFAULT_PREFERENCES = {
    "network": "testnet",
    "gui": False
}
preferences = DEFAULT_PREFERENCES

def load_pref():
    if not os.path.exists(PREFERENCES_FILE):
        print("No preferences file found, creating preferences with default values")
        with open(PREFERENCES_FILE, "w") as file:
            json.dump(DEFAULT_PREFERENCES, file, indent=4)
            print(f"{PREFERENCES_FILE} created with default values")
    with open(PREFERENCES_FILE, "r") as file:
        preferences = json.load(file)
        print(f"{PREFERENCES_FILE} loaded into memory, preferences set")

def set_pref():
    if preferences["network"] == "mainnet":
        print("Loading into mainent...")
        network = "mainnet"
    else:
        print("Loading into testnet by default...")
        network = "testnet"
    if preferences["gui"] == True:
        print("Loading into user interface...")
    else:
        print("Loading into console by default...")