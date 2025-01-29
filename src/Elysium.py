# Packages
import customtkinter as ctk
import tkinter as tk
from tkinter import *
from frames import *
from auth import authenticate as auth
from core.bitcoin import *
import time
import random
from PIL import Image, ImageTk
from tkinter import messagebox

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

    def show_frame(self, frame, *args):
        for widget in self.winfo_children():
            widget.destroy()
        frame(*args)

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

    def create_account_frame(self, index, seed=None):
        match index:
            # INTRO
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
                create_button.place(relx=0.35, rely=0.7, anchor='center')

                cancel_button = ctk.CTkButton(
                    master=self,
                    text="Cancel",
                    command=lambda: self.show_frame(self.login_frame)
                )
                cancel_button.place(relx=0.65, rely=0.7, anchor='center')
            # SEED GENERATION
            case 1:
                # Seed generation
                if seed == None:
                    seed = gen_seed()
                    split_seed = seed.split()
                print(seed)
                key_frame = ctk.CTkFrame(master=self, width=400, height=300)  # Adjust size as needed
                key_frame.place(relx=0.5, rely=0.4, anchor="center")  # Center the frame in the parent

                # Add a title to the frame
                title_label = ctk.CTkLabel(
                    master=key_frame,
                    text="Your 12 Recovery Words",
                    font=("Helvetica", 16)
                )
                title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

                # Add the recovery words in 2 columns
                for index, word in enumerate(split_seed):
                    row = (index % 6) + 1  # Divide into 6 rows
                    col = index // 6       # Column is 0 for first 6 words, 1 for next 6
                    word_label = ctk.CTkLabel(
                        master=key_frame,
                        text=f"{index + 1}. {word}",  # Add index for numbering
                        font=("Arial", 12),
                    )
                    word_label.grid(row=row, column=col, padx=20, pady=5, sticky="w")
                
                # Text
                styled_label = ctk.CTkLabel(
                    master=app,
                    text="Before continuing, store these word somewhere secure,\n"
                        "on the following page you will be asked to input the words in order.",
                    font=("Helvetica", 14)
                )
                styled_label.place(relx=0.5, rely=0.75, anchor='center')
                
                # Continue and cancel button
                create_button = ctk.CTkButton(
                    master=self, 
                    text="Continue",
                    command=lambda: self.show_frame(self.create_account_frame, 2, seed)
                )
                create_button.place(relx=0.35, rely=0.85, anchor='center')

                cancel_button = ctk.CTkButton(
                    master=self,
                    text="Back",
                    command=lambda: self.show_frame(self.create_account_frame, 0)
                )
                cancel_button.place(relx=0.65, rely=0.85, anchor='center')
            # SEED VALIDATION
            case 2:
                input_frame = ctk.CTkFrame(master=self, width=400, height=300)
                input_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

                # Add a title
                title_label = ctk.CTkLabel(
                    master=input_frame,
                    text="Enter Your 12 Recovery Words",
                    font=("Helvetica", 16),
                )
                title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

                # Create entry fields for the 12 recovery words
                entry_fields = []  # Store entry widgets for later use
                for index in range(12):
                    row = (index % 6) + 1  # 6 rows
                    col = index // 6       # 2 columns
                    word_entry = ctk.CTkEntry(
                        master=input_frame,
                        placeholder_text=f"Word {index + 1}",  # Placeholder for the word
                        width=120
                    )
                    word_entry.grid(row=row, column=col, padx=10, pady=5, sticky="w")
                    entry_fields.append(word_entry)

                # Logic to combine the entered words into a single string
                def combine_words():
                    combined_words = " ".join(entry.get().strip() for entry in entry_fields)
                    if seed == combined_words or True:
                        messagebox.showinfo("Success", "Seed was validated")
                        messagebox.showinfo("Development Build", "No systems have been put in place to put this key on a blockchain, "
                                            "for that reason the key is stored on your computer. "
                                            "Accounts cannot be transfered between devices currently.")
                        self.show_frame(self.create_account_frame, 3, seed)
                    else:
                        messagebox.showwarning("Validation Error", "Seed did not match")
                # Add a submit button
                submit_button = ctk.CTkButton(
                    master=input_frame,
                    text="Validate",
                    command=combine_words
                )
                submit_button.grid(row=7, column=0, columnspan=2, pady=20)
            # Account creation
            case 3:
                # Title
                title = Label(
                    master=self,
                    text="Create an Account",
                    bg='#333538',
                    fg='#ffffff',
                    font=("Helvetica", 18),
                )
                title.place(relx=0.5, rely=0.2, anchor='center')

                # Username Entry
                self.username_entry = ctk.CTkEntry(master=self, placeholder_text="Username", width=200)
                self.username_entry.place(relx=0.5, rely=0.4, anchor='center')
                # Password Entry
                self.password_entry = ctk.CTkEntry(master=self, placeholder_text="New Password", width=200, show="*")
                self.password_entry.place(relx=0.5, rely=0.5, anchor='center')

                # Confirm Password Entry
                self.confirm_password_entry = ctk.CTkEntry(master=self, placeholder_text="Confirm Password", width=200, show="*")
                self.confirm_password_entry.place(relx=0.5, rely=0.6, anchor='center')
                
                def create_account(username, password, confirm_password):
                    """Validate inputs and create a new account using `auth.create_account`."""
                    if not username or not password or not confirm_password:
                        messagebox.ERROR("Failed to create account", "Missing username or password")
                        return
                    if password != confirm_password:
                        messagebox.ERROR("Failed to create account", "Passwords do not match")
                        return
                    try:
                        # Call `auth.create_account` to handle the account creation
                        auth.create_account(username, password, seed)
                        print("reached")
                        #messagebox.INFO("Succes", "Account created successfully!")
                        self.show_frame(self.create_account_frame, 4)  # Redirect to login frame
                    except Exception as e:
                        print(f"Account creation error: {e}")
                # Create Account Button
                create_button = ctk.CTkButton(
                    master=self,
                    text="Create Account",
                    command=lambda: create_account(self.username_entry.get().strip(), 
                                                   self.password_entry.get().strip(), 
                                                   self.confirm_password_entry.get().strip())
                )
                create_button.place(relx=0.5, rely=0.7, anchor='center')

                back_button = ctk.CTkButton(
                    master=self,
                    text="Cancel",
                    command=lambda: self.show_frame(self.login_frame),
                )
                back_button.place(relx=0.5, rely=0.8, anchor='center')
            case 4:
                # Title
                title = Label(
                    master=self,
                    text="Create an Account",
                    bg='#333538',
                    fg='#ffffff',
                    font=("Helvetica", 18),
                )
                title.place(relx=0.5, rely=0.2, anchor='center')
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