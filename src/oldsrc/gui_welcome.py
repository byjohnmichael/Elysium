import customtkinter as ctk
from gui_wallet_create import open_wallet_creation
from gui_wallet_login import open_wallet_login
from gui_wallet_home import open_home_page
from pubsub import pub

def welcome_page():
    # Set appearance mode and theme
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    def login_update(wallet_name):
        open_home_page(wallet_name, app)
    # Event handler
    pub.subscribe(login_update, "login.success")

    # Create the main application window
    app = ctk.CTk()
    app.title("KeyStone Wallet")
    app.geometry("600x600")  # Taller window size

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
    app.mainloop()