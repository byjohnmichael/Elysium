import customtkinter as ctk
import tkinter.messagebox as messagebox
import network_bitcoin as n_btc
import fileman as fm
from pubsub import pub

"""
SECTIONS:
1. Refresh
- for refreshing wallet info

2. Import
- for importing wallets
"""

# REFRESH SECTION
def refresh(crypto_type, wallet_name):
    data = fm.load(f"wallet_{wallet_name}.json")
    match crypto_type:
        case "btc":
            btc_data = {
                "balance": None,
                "address": None
            }
            if "btc_active" in data:
                btc_data["balance"] = n_btc.get_balance(wallet_name)
                btc_data["address"] = n_btc.get_address(wallet_name)
                return btc_data
            else:
                return btc_data
        case "eth":
            eth_data = {
                "balance": None,
                "address": None
            }
            return eth_data
        case "sol":
            sol_data = {
                "balance": None,
                "address": None
            }
            return sol_data

# IMPORT SECTION
def open_wallet_import(crypto_type, wallet_name):
    """
    Opens the wallet import window based on the type of cryptocurrency.
    :param crypto_type: Type of cryptocurrency (e.g., "btc", "eth", "sol").
    """
    match crypto_type:
        case "btc":
            # Create the BTC wallet import window
            btc_import_window = ctk.CTkToplevel()
            btc_import_window.title("Import or Create a Bitcoin Wallet")
            btc_import_window.geometry("400x600")

            # Make the window stay on top and disable interactions with the main window
            btc_import_window.attributes("-topmost", True)
            btc_import_window.grab_set()

            # Header text
            header_label = ctk.CTkLabel(
                btc_import_window,
                text="Import or Create a Bitcoin Wallet",
                font=("Roboto", 20, "bold"),
                anchor="w"
            )
            header_label.pack(pady=(10, 20), padx=10, anchor="w")

            # Description text
            description_label = ctk.CTkLabel(
                btc_import_window,
                text="Input your twelve-word key to import your Bitcoin wallet, or create a new one below:",
                font=("Roboto", 14),
                justify="left",
                wraplength=380
            )
            description_label.pack(pady=(0, 20), padx=10, anchor="w")

            # Create New Wallet Button
            create_wallet_button = ctk.CTkButton(
                btc_import_window,
                text="Create New Wallet",
                fg_color="blue",
                command=lambda: btc_create(wallet_name, btc_import_window)
            )
            create_wallet_button.pack(pady=(10, 20), padx=10)

            # Input fields for 12-word seed (two columns)
            seed_frame = ctk.CTkFrame(btc_import_window)
            seed_frame.pack(fill="both", expand=True, padx=10, pady=10)

            left_column = ctk.CTkFrame(seed_frame)  # Left column for 1st-6th words
            left_column.pack(side="left", fill="y", expand=True, padx=5)

            right_column = ctk.CTkFrame(seed_frame)  # Right column for 7th-12th words
            right_column.pack(side="right", fill="y", expand=True, padx=5)

            # Add fields to the left column (1st-6th words)
            seed_entries = []
            for i in range(1, 7):
                placeholder = f"{i}{'st' if i == 1 else 'nd' if i == 2 else 'rd' if i == 3 else 'th'} Word"
                entry = ctk.CTkEntry(left_column, width=150, placeholder_text=placeholder)
                entry.pack(pady=(5, 10))
                seed_entries.append(entry)

            # Add fields to the right column (7th-12th words)
            for i in range(7, 13):
                placeholder = f"{i}{'st' if i == 1 else 'nd' if i == 2 else 'rd' if i == 3 else 'th'} Word"
                entry = ctk.CTkEntry(right_column, width=150, placeholder_text=placeholder)
                entry.pack(pady=(5, 10))
                seed_entries.append(entry)

            # Button frame at the bottom
            button_frame = ctk.CTkFrame(btc_import_window)
            button_frame.pack(side="bottom", fill="x", pady=20, padx=10)

            # Import button (functionality to be added later)
            import_button = ctk.CTkButton(
                button_frame,
                text="Import",
                fg_color="green",
                command=lambda: btc_import(wallet_name, seed_entries, btc_import_window)
            )
            import_button.pack(side="left", expand=True, fill="x", padx=5)

            # Cancel button
            cancel_button = ctk.CTkButton(
                button_frame,
                text="Cancel",
                fg_color="red",
                command=btc_import_window.destroy
            )
            cancel_button.pack(side="right", expand=True, fill="x", padx=5)

        case "eth":
            print("Opening ETH wallet import...")
            # Logic for importing an ETH wallet will go here

        case "sol":
            print("Opening SOL wallet import...")
            # Logic for importing a SOL wallet will go here

        case _:
            print(f"Unsupported cryptocurrency type: {crypto_type}")

def btc_create(wallet_name, window):
    seed = n_btc.gen_seed()
    n_btc.create_wallet_from_words(wallet_name, seed)
    data = fm.load(f"wallet_{wallet_name}.json")
    data["btc_active"] = True
    fm.save(data, f"wallet_{wallet_name}.json")
    messagebox.showinfo("Success", f"Wallet {wallet_name} created. Here are the 12 words:\n{seed}")
    pub.sendMessage("import.success")
    window.destroy()
    

def btc_import(wallet_name, words, window):
    seed = " ".join(entry.get() for entry in words)
    n_btc.create_wallet_from_words(wallet_name, seed)
    data = fm.load(f"wallet_{wallet_name}.json")
    data["btc_active"] = True
    fm.save(data, f"wallet_{wallet_name}.json")
    messagebox.showinfo("Success", f"Wallet {wallet_name} imported.")
    pub.sendMessage("import.success")
    window.destroy()
