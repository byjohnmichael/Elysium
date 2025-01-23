import customtkinter as ctk
from gui_wallet_create import open_wallet_creation
from gui_wallet_login import open_wallet_login
from gui_wallet_import import open_wallet_import
from pubsub import pub
# Set appearance mode and theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def update_on_login(wallet_name):
    # Clear the main window
    for widget in app.winfo_children():
        widget.destroy()

    # Header with wallet name
    header_label = ctk.CTkLabel(
        app,
        text=wallet_name,
        font=("Roboto", 24, "bold")
    )
    header_label.pack(pady=(10, 5))

    # Horizontal line under the header
    header_separator = ctk.CTkFrame(app, height=2)
    header_separator.pack(fill="x", pady=(0, 10))

    # Left menu
    menu_frame = ctk.CTkFrame(app, width=100)
    menu_frame.pack(side="left", fill="y", padx=(10, 5))

    home_button = ctk.CTkButton(menu_frame, text="Home", command=lambda: print("Home clicked"))
    home_button.pack(pady=(10, 5))

    send_button = ctk.CTkButton(menu_frame, text="Send", command=lambda: print("Send clicked"))
    send_button.pack(pady=5)

    receive_button = ctk.CTkButton(menu_frame, text="Receive", command=lambda: print("Receive clicked"))
    receive_button.pack(pady=(5, 10))

    # Balances section
    balances_frame = ctk.CTkFrame(app)
    balances_frame.pack(side="left", fill="both", expand=True, padx=(5, 10))

    # General balance
    balance_label = ctk.CTkLabel(
        balances_frame,
        text="Balance: 0.00$",
        font=("Roboto", 18, "bold"),
        anchor="w"
    )
    balance_label.pack(anchor="w", pady=(10, 5), padx=10)

    # BTC balance with Import button
    btc_frame = ctk.CTkFrame(balances_frame)
    btc_frame.pack(fill="x", pady=5, padx=10)

    btc_label = ctk.CTkLabel(
        btc_frame,
        text="BTC: 0.0",
        font=("Roboto", 14),
        anchor="w"
    )
    btc_label.pack(side="left")

    btc_import_button = ctk.CTkButton(
        btc_frame,
        text="Import a Wallet",
        fg_color="blue",
        command=lambda: open_wallet_import("btc", wallet_name)
    )
    btc_import_button.pack(side="right", padx=5)

    # ETH balance with Import button
    eth_frame = ctk.CTkFrame(balances_frame)
    eth_frame.pack(fill="x", pady=5, padx=10)

    eth_label = ctk.CTkLabel(
        eth_frame,
        text="ETH: 0.0",
        font=("Roboto", 14),
        anchor="w"
    )
    eth_label.pack(side="left")

    eth_import_button = ctk.CTkButton(
        eth_frame,
        text="Import a Wallet",
        fg_color="blue",
        command=lambda: print("Import ETH wallet")
    )
    eth_import_button.pack(side="right", padx=5)

    # SOL balance with Import button
    sol_frame = ctk.CTkFrame(balances_frame)
    sol_frame.pack(fill="x", pady=5, padx=10)

    sol_label = ctk.CTkLabel(
        sol_frame,
        text="SOL: 0.0",
        font=("Roboto", 14),
        anchor="w"
    )
    sol_label.pack(side="left")

    sol_import_button = ctk.CTkButton(
        sol_frame,
        text="Import a Wallet",
        fg_color="blue",
        command=lambda: print("Import SOL wallet")
    )
    sol_import_button.pack(side="right", padx=5)

# Event handler
pub.subscribe(update_on_login, "login.success")



# Create the main application window
app = ctk.CTk()
app.title("KeyStone Wallet")
app.geometry("400x600")  # Taller window size

# Create header text
header_label = ctk.CTkLabel(
    app,
    text="Welcome to KeyStone Wallet",
    font=("Roboto", 24, "bold")
)
header_label.pack(pady=(100, 10))  # Position with padding

# Create description text
description_label = ctk.CTkLabel(
    app,
    text="KeyStone Wallet acts as a master wallet,\ncombining and simplifying your crypto assets in one wallet",
    font=("Roboto", 16),
    justify="center"
)
description_label.pack(pady=10)

# Create sub-description text
sub_description_label = ctk.CTkLabel(
    app,
    text="Create a master wallet to get started",
    font=("Roboto", 14),
    justify="center"
)
sub_description_label.pack(pady=20)

# Create button frame at the bottom
button_frame = ctk.CTkFrame(app)
button_frame.pack(side="bottom", fill="x", pady=20, padx=10)

# Green button for creating a master wallet
create_button = ctk.CTkButton(
    button_frame,
    text="Create a Master Wallet",
    fg_color="green",
    command=open_wallet_creation
)
create_button.pack(side="left", expand=True, fill="x", padx=5)

# Blue button for syncing a master wallet
sync_button = ctk.CTkButton(
    button_frame,
    text="Log into a Master Wallet",
    fg_color="blue",
    command=open_wallet_login
)
sync_button.pack(side="right", expand=True, fill="x", padx=5)
