# Packages
import customtkinter as ctk
import tkinter as tk
from tkinter import *
from frames import *
from auth import authenticate as auth
import time
import random
from PIL import Image, ImageTk

# Set global variables
background_color = '#333538'
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    # Set const variables
    WIDTH = 700
    HEIGHT = 480

    # Init method
    def __init__(self):
        super().__init__()

        # Window configuration
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(False, False)
        self.configure(fg_color=background_color)
        self.login_frame()

    def show_frame(self, frame, args=None):
        for widget in self.winfo_children():
            widget.destroy()
        if args != None:
            frame(args)
        else:
            frame()

    def login_frame(self):
        self.title("Elysium: Login/Sign up")

        # Icon
        #ico = Image.open('icon.png')
        #photo = ImageTk.PhotoImage(ico)
        #self.wm_iconphoto(False, photo)

        # Login Image
        image = Image.open("login.png")
        img = ImageTk.PhotoImage(image)
        label1 = Label(image=img, bg='#333538')
        label1.image = img
        label1.place(relx = -0.003, rely = 0.5, anchor='w')

        # Load the game logo
        #image2 = Image.open("logo.png")
        #img2 = ImageTk.PhotoImage(image2)
        #label1 = Label(image=img2, bg='#333538')
        #label1.image2 = img2
        #label1.place(relx = 0.75, rely = 0.23, anchor='center')

        # Welcome text
        welcome = Label(text="Welcome to Elysium", bg='#333538', fg='#ffffff')
        welcome.place(relx = 0.75, rely = 0.36, anchor='center')

        # Define the username entry field
        username = ctk.CTkEntry(master=self, placeholder_text="Username", width=200)
        username.place(relx = 0.75, rely = 0.5, anchor = 'center')

        # Define the password entry field
        password = ctk.CTkEntry(master=self, placeholder_text="Password", width=200, show="*")
        password.place(relx = 0.75, rely = 0.6, anchor = 'center')

        # Define the login button
        button = ctk.CTkButton(
            master=self, 
            text="Login",
            command=lambda: self.show_frame(self.login_account_frame)
        )
        button.place(relx = 0.75, rely = 0.75, anchor = 'center')

        # Define the create account button
        create_account_button = ctk.CTkButton(
            master=self,
            text="Create Account",
            command=lambda: self.show_frame(self.create_account_frame, 0)
        )
        create_account_button.place(relx=0.75, rely=0.85, anchor='center')

        # Define the restore account button
        create_account_button = ctk.CTkButton(
            master=self,
            text="Restore Account",
            command=lambda: self.show_frame(self.restore_account_frame)
        )
        create_account_button.place(relx=0.75, rely=0.95, anchor='center')
    def login_account_frame(self, password):

        return

    def create_account_frame(self, index):
        match index:
            case 0:
                # Title
                title = Label(text="Welcome to Elysium", bg='#333538', fg='#ffffff', font=("Helvetica", 18))
                title.place(relx=0.5, rely=0.1, anchor='center')

                # Text
                styled_label = ctk.CTkLabel(
                    master=app,
                    text="Welcome to Elysium, your gateway to a streamlined, multi-asset wallet experience!\n"
                        "Elysium is designed to manage multiple types of assets securely and efficiently, all from one simple interface.\n"
                        "Whether you're storing cryptocurrency, NFTs, or other digital assets,\n"
                        "Elysium makes it easy to send, receive, and view your balance without unnecessary complexity.\n\n"
                        "Your wallet is secured with 12 recovery words and a local password.\n"
                        "The 12 words are your master key—keep them safe to recover your wallet anytime.\n"
                        "The password is stored on your device to protect local access\n"
                        "but doesn’t replace the recovery words for account recovery.\n\n"
                        "Click the generate key button to continue with acccount creation.",
                    font=("Helvetica", 14)
                )
                styled_label.place(relx=0.5, rely=0.4, anchor='center')

                # Generate key, and cancel button
                create_button = ctk.CTkButton(
                    master=self, 
                    text="Generate Key",
                    command=lambda: self.show_frame(self.create_account_frame, 1)
                )
                create_button.place(relx=0.25, rely=0.7, anchor='center')

                cancel_button = ctk.CTkButton(
                    master=self,
                    text="Cancel",
                    command=lambda: self.show_frame(self.login_frame)
                )
                cancel_button.place(relx=0.75, rely=0.7, anchor='center')
            case 1:
                # Title
                title = Label(text="Key Generation", bg='#333538', fg='#ffffff', font=("Helvetica", 18))
                title.place(relx=0.5, rely=0.1, anchor='center')
            case 2:
                # Title
                title = Label(text="Create an Account", bg='#333538', fg='#ffffff', font=("Helvetica", 18))
                title.place(relx=0.5, rely=0.2, anchor='center')

                # Username Entry
                username = ctk.CTkEntry(master=self, placeholder_text="Username", width=200)
                username.place(relx=0.5, rely=0.4, anchor='center')

                # Password Entry
                password = ctk.CTkEntry(master=self, placeholder_text="New Password", width=200, show="*")
                password.place(relx=0.5, rely=0.5, anchor='center')

                # Confirm Password Entry
                confirm_password = ctk.CTkEntry(master=self, placeholder_text="Confirm Password", width=200, show="*")
                confirm_password.place(relx=0.5, rely=0.6, anchor='center')

                # Create Button
                create_button = ctk.CTkButton(
                    master=self, 
                    text="Create Account",
                    command=lambda: self.show_frame(self.login_account_frame)
                )
                create_button.place(relx=0.5, rely=0.7, anchor='center')

                # Back Button
                back_button = ctk.CTkButton(
                    master=self,
                    text="Back to Login",
                    command=lambda: self.show_frame(self.login_frame),
                )
                back_button.place(relx=0.5, rely=0.8, anchor='center')

    def restore_account_frame(self):

        return

    # On close method
    def on_closing(self, event=0):
        self.destroy()

    # Start method
    def start(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()