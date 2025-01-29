import customtkinter as ctk
import network_bitcoin as n_btc
import qrcode
from PIL import Image, ImageTk

def open_send_window(crypto_type, wallet_name):
    match crypto_type:
        case "btc":
            # Create the BTC wallet import window
            btc_send_window = ctk.CTkToplevel()
            btc_send_window.title("Send BTC")
            btc_send_window.geometry("400x600")

            # Make the window stay on top and disable interactions with the main window
            btc_send_window.attributes("-topmost", True)
            btc_send_window.grab_set()

            # Header text
            header_label = ctk.CTkLabel(
                btc_send_window,
                text="Send BTC",
                font=("Roboto", 20, "bold"),
                anchor="w"
            )
            header_label.pack(pady=(10, 20), padx=10, anchor="w")

            # Description text
            description_label = ctk.CTkLabel(
                btc_send_window,
                text="Input the address you would like to send to and the amount of btc you would like to send",
                font=("Roboto", 14),
                justify="left",
                wraplength=380
            )
            description_label.pack(pady=(0, 20), padx=10, anchor="w")

            # Input for Wallet Name
            address_label = ctk.CTkLabel(
                btc_send_window,
                text="Address",
                font=("Roboto", 14)
            )
            address_label.pack(pady=(10, 5), padx=10, anchor="w")
            address_entry = ctk.CTkEntry(btc_send_window, width=300)
            address_entry.pack(pady=(0, 10), padx=10)

            # Input for Password
            amount_label = ctk.CTkLabel(
                btc_send_window,
                text="Amount (BTC)",
                font=("Roboto", 14)
            )
            amount_label.pack(pady=(10, 5), padx=10, anchor="w")
            amount_entry = ctk.CTkEntry(btc_send_window, width=300)
            amount_entry.pack(pady=(0, 10), padx=10)

            # Button frame at the bottom
            button_frame = ctk.CTkFrame(btc_send_window)
            button_frame.pack(side="bottom", fill="x", pady=20, padx=10)

            # Import button (functionality to be added later)
            import_button = ctk.CTkButton(
                button_frame,
                text="Send",
                fg_color="green",
                command=lambda: send(wallet_name, address_entry.get(), amount_entry.get())
            )
            import_button.pack(side="left", expand=True, fill="x", padx=5)

            # Cancel button
            cancel_button = ctk.CTkButton(
                button_frame,
                text="Cancel",
                fg_color="red",
                command=btc_send_window.destroy
            )
            cancel_button.pack(side="right", expand=True, fill="x", padx=5)
    return

def send(wallet_name, to_address, amount):
    amount = float(amount)
    tx = n_btc.send(wallet_name, to_address, amount)

    # QR Window
    qr_window = ctk.CTkToplevel()
    qr_window.title("Transaction Details")
    qr_window.geometry("400x600")

    # Make the window stay on top and disable interactions with the main window
    qr_window.attributes("-topmost", True)
    qr_window.grab_set()

    # Header text
    header_label = ctk.CTkLabel(
        qr_window,
        text="Transaction Details",
        font=("Roboto", 20, "bold")
    )
    header_label.pack(pady=(10, 10))

    # Transaction ID label
    txid_label = ctk.CTkLabel(
        qr_window,
        text=f"Transaction ID:\n{tx.txid}",
        font=("Roboto", 14),
        wraplength=380,
        justify="center"
    )
    txid_label.pack(pady=(0, 20))

    # Generate QR code for the TXID
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(f"https://blockstream.info/testnet/tx/{tx.txid}")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Convert the QR code image for display in CustomTkinter
    qr_img = qr_img.resize((200, 200), Image.Resampling.LANCZOS)  # Resize the image
    qr_img_tk = ImageTk.PhotoImage(qr_img)

    # Display the QR code
    qr_label = ctk.CTkLabel(qr_window, image=qr_img_tk)
    qr_label.image = qr_img_tk  # Keep a reference to prevent garbage collection
    qr_label.pack(pady=(10, 20))

    # Close button
    close_button = ctk.CTkButton(
        qr_window,
        text="Close",
        fg_color="red",
        command=qr_window.destroy
    )
    close_button.pack(pady=(20, 10))

def open_receive_window(crypto_type, address):
    match crypto_type:
        case "btc":
            print(address)
            # QR Window
            qr_window = ctk.CTkToplevel()
            qr_window.title("Address Details")
            qr_window.geometry("400x600")

            # Make the window stay on top and disable interactions with the main window
            qr_window.attributes("-topmost", True)
            qr_window.grab_set()

            # Header text
            header_label = ctk.CTkLabel(
                qr_window,
                text="Wallet Address",
                font=("Roboto", 20, "bold")
            )
            header_label.pack(pady=(10, 10))

            # Transaction ID label
            txid_label = ctk.CTkLabel(
                qr_window,
                text=f"Transaction ID:\n{address}",
                font=("Roboto", 14),
                wraplength=380,
                justify="center"
            )
            txid_label.pack(pady=(0, 20))

            # Generate QR code for the TXID
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4
            )
            qr.add_data(address)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Convert the QR code image for display in CustomTkinter
            qr_img = qr_img.resize((200, 200), Image.Resampling.LANCZOS)  # Resize the image
            qr_img_tk = ImageTk.PhotoImage(qr_img)

            # Display the QR code
            qr_label = ctk.CTkLabel(qr_window, image=qr_img_tk)
            qr_label.image = qr_img_tk  # Keep a reference to prevent garbage collection
            qr_label.pack(pady=(10, 20))

            # Close button
            close_button = ctk.CTkButton(
                qr_window,
                text="Close",
                fg_color="red",
                command=qr_window.destroy
            )
            close_button.pack(pady=(20, 10))
