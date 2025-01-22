import os
import json
PREFERENCES_FILE = "preferences.json"
DEFAULT_PREFERENCES = {
    "network": "testnet",
    "gui": False
}
preferences = DEFAULT_PREFERENCES

# Helper function for load_pref
def set_pref():
    if preferences["network"] == "mainnet":
        print("Operating on the mainent")
        network = "mainnet"
    else:
        print("Operating on the testnet by default")
        network = "testnet"
    if preferences["gui"] == True:
        print("Loading into user interface...")
        # TODO
    else:
        print("Loaded into console by default")

# Loads or creates preferences 
def load_pref():
    if not os.path.exists(PREFERENCES_FILE):
        print("No preferences file found, creating preferences with default values")
        with open(PREFERENCES_FILE, "w") as file:
            json.dump(DEFAULT_PREFERENCES, file, indent=4)
            print(f"{PREFERENCES_FILE} created with default values")
    with open(PREFERENCES_FILE, "r") as file:
        preferences = json.load(file)
        set_pref()
        print(f"{PREFERENCES_FILE} loaded into memory, preferences set")

