import customtkinter as ctk
import tkinter.messagebox as messagebox
import fileman as fm
from pubsub import pub

def open_wallet_login():
    wallet_login_window = ctk.CTkToplevel()
    wallet_login_window.title("Wallet Login")
    wallet_login_window.geometry("400x400")

    # Make the window stay on top and disable interactions with the main window
    wallet_login_window.attributes("-topmost", True)
    wallet_login_window.grab_set()

    # Header text
    header_label = ctk.CTkLabel(
        wallet_login_window,
        text="Wallet Login",
        font=("Roboto", 20, "bold"),
        anchor="w"
    )
    header_label.pack(pady=(10, 20), padx=10, anchor="w")

    # Input for Wallet Name
    name_label = ctk.CTkLabel(
        wallet_login_window,
        text="Wallet Name",
        font=("Roboto", 14)
    )
    name_label.pack(pady=(10, 5), padx=10, anchor="w")
    name_entry = ctk.CTkEntry(wallet_login_window, width=300)
    name_entry.pack(pady=(0, 10), padx=10)

    # Input for Password
    password_label = ctk.CTkLabel(
        wallet_login_window,
        text="Password",
        font=("Roboto", 14)
    )
    password_label.pack(pady=(10, 5), padx=10, anchor="w")
    password_entry = ctk.CTkEntry(wallet_login_window, width=300, show="*")
    password_entry.pack(pady=(0, 10), padx=10)

    def load_and_validate():
        name = name_entry.get()
        password = password_entry.get()
        if not name or not password:
            messagebox.showerror("Error", "Name and Password cannot be empty!")
            return
        try:
            data = fm.load(f"wallet_{name}.json")
            if data["name"] == name and data["password"] == password:
                messagebox.showinfo("Success", f"Wallet {name} logged in successfully!")
                pub.sendMessage("login.success", wallet_name=name)
                wallet_login_window.destroy()  # Close the window on success
            else:
                messagebox.showinfo("Failure", f"Wallet name or password was incorrect")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save wallet: {e}")

    # Button frame at the bottom
    button_frame = ctk.CTkFrame(wallet_login_window)
    button_frame.pack(side="bottom", fill="x", pady=20, padx=10)

    # Login button
    login_button = ctk.CTkButton(
        button_frame,
        text="Login",
        fg_color="green",
        command=load_and_validate    
    )
    login_button.pack(side="left", expand=True, fill="x", padx=5)

    # Cancel button
    cancel_button = ctk.CTkButton(
        button_frame,
        text="Cancel",
        fg_color="red",
        command=wallet_login_window.destroy
    )
    cancel_button.pack(side="right", expand=True, fill="x", padx=5)
