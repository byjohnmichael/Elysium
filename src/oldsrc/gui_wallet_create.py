import customtkinter as ctk
import tkinter.messagebox as messagebox
import fileman as fm

def open_wallet_creation():
    master_wallet_window = ctk.CTkToplevel()
    master_wallet_window.title("Master Wallet Creation")
    master_wallet_window.geometry("400x400")

    # Make the window stay on top and disable interactions with the main window
    master_wallet_window.attributes("-topmost", True)
    master_wallet_window.grab_set()

    # Header text
    header_label = ctk.CTkLabel(
        master_wallet_window,
        text="Create a Master Wallet",
        font=("Roboto", 20, "bold"),
        anchor="w"
    )
    header_label.pack(pady=(10, 20), padx=10, anchor="w")

    # Input for Name
    name_label = ctk.CTkLabel(
        master_wallet_window,
        text="Name",
        font=("Roboto", 14)
    )
    name_label.pack(pady=(10, 5), padx=10, anchor="w")
    name_entry = ctk.CTkEntry(master_wallet_window, width=300)
    name_entry.pack(pady=(0, 10), padx=10)

    # Input for Password
    password_label = ctk.CTkLabel(
        master_wallet_window,
        text="Password",
        font=("Roboto", 14)
    )
    password_label.pack(pady=(10, 5), padx=10, anchor="w")
    password_entry = ctk.CTkEntry(master_wallet_window, width=300, show="*")
    password_entry.pack(pady=(0, 10), padx=10)
    
    # Development note
    dev_note_label = ctk.CTkLabel(
        master_wallet_window,
        text="*12 word seed not available as this is in development",
        font=("Roboto", 12, "italic"),
        fg_color=None,
        justify="center"
    )
    dev_note_label.pack(pady=(10, 0), padx=10)

    # Function to validate and save wallet
    def validate_and_save():
        name = name_entry.get()
        password = password_entry.get()
        if not name or not password:
            messagebox.showerror("Error", "Name and Password cannot be empty!")
            return
        try:
            fm.save({"name": name, "password": password}, f"wallet_{name}.json")
            messagebox.showinfo("Success", f"Wallet {name} saved successfully!")
            master_wallet_window.destroy()  # Close the window on success
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save wallet: {e}")

    # Button frame at the bottom
    button_frame = ctk.CTkFrame(master_wallet_window)
    button_frame.pack(side="bottom", fill="x", pady=20, padx=10)

    # Confirm creation button
    confirm_button = ctk.CTkButton(
        button_frame,
        text="Confirm Creation",
        fg_color="green",
        command=validate_and_save
    )
    confirm_button.pack(side="left", expand=True, fill="x", padx=5)

    # Cancel creation button
    cancel_button = ctk.CTkButton(
        button_frame,
        text="Cancel Creation",
        fg_color="red",
        command=master_wallet_window.destroy
    )
    cancel_button.pack(side="right", expand=True, fill="x", padx=5)