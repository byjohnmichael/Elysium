import customtkinter as ctk
import gui_wallet_handler as wh
import gui_wallet_tx as wtx
from pubsub import pub


def open_home_page(wallet_name, app):
    # Clear the main window
    for widget in app.winfo_children():
        widget.destroy()

    # Header with wallet name
    header_frame = ctk.CTkFrame(app)
    header_frame.pack(fill="x", pady=(10, 10), padx=10)

    header_label = ctk.CTkLabel(
        header_frame,
        text=wallet_name,
        font=("Roboto", 24, "bold"),
    )
    header_label.pack(side="left", pady=(10, 5))

    # Refresh button
    refresh_button = ctk.CTkButton(
        header_frame,
        text="Refresh",
        fg_color="gray",
        width=100,
        command=lambda: build_balance_section()  # Call the refresh function
    )
    refresh_button.pack(side="right", padx=5)

    # Horizontal line under the header
    header_separator = ctk.CTkFrame(app, height=2)
    header_separator.pack(fill="x", pady=(0, 10))

    # Store balances_frame reference for clearing it
    balances_frame = ctk.CTkFrame(app)
    balances_frame.pack(side="left", fill="both", expand=True, padx=(5, 10))

    def build_balance_section():
        # Clear existing content in balances_frame
        for widget in balances_frame.winfo_children():
            widget.destroy()

        print("Refreshing balances...")

        # General balance
        balance_label = ctk.CTkLabel(
            balances_frame,
            text="Balance: 0.00$",
            font=("Roboto", 18, "bold"),
            anchor="w"
        )
        balance_label.pack(anchor="w", pady=(10, 5), padx=10)

        # BTC balance with Import or Send/Receive buttons
        btc_frame = ctk.CTkFrame(balances_frame)
        btc_frame.pack(fill="x", pady=5, padx=10)

        btc_data = wh.refresh("btc", wallet_name)
        btc_label = ctk.CTkLabel(
            btc_frame,
            text=f"BTC: {btc_data['balance']}",
            font=("Roboto", 14),
            anchor="w"
        )
        btc_label.pack(side="left")

        if btc_data["balance"] is None:
            btc_import_button = ctk.CTkButton(
                btc_frame,
                text="Import a Wallet",
                fg_color="blue",
                command=lambda: wh.open_wallet_import("btc", wallet_name)
            )
            btc_import_button.pack(side="right", padx=5)
        else:
            # Add Send and Receive buttons if balance exists
            btc_send_button = ctk.CTkButton(
                btc_frame,
                text="Send",
                fg_color="green",
                command=lambda: wtx.open_send_window("btc", wallet_name)
            )
            btc_send_button.pack(side="right", padx=5)

            btc_receive_button = ctk.CTkButton(
                btc_frame,
                text="Receive",
                fg_color="blue",
                command=lambda: wtx.open_receive_window("btc", btc_data["address"])
            )
            btc_receive_button.pack(side="right", padx=5)

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

    # Build the initial balance section
    build_balance_section()

    # Subscribe to refresh event
    pub.subscribe(build_balance_section, "import.success")
