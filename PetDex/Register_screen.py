import customtkinter
import logging

logger = logging.getLogger(__name__)

class RegisterFrame(customtkinter.CTkFrame): # This should be the RegisterFrame class
    def __init__(self, master, user_manager, show_login_callback, show_main_menu_callback): # Added show_main_menu_callback
        super().__init__(master)
        self.user_manager = user_manager
        self.show_login_callback = show_login_callback
        self.show_main_menu_callback = show_main_menu_callback # Store the callback

        # --- Configure grid for the frame itself to expand ---
        self.grid_columnconfigure(0, weight=1) # Left spacer column
        self.grid_columnconfigure(1, weight=0) # Column for labels
        self.grid_columnconfigure(2, weight=0) # Column for entries
        self.grid_columnconfigure(3, weight=1) # Right spacer column
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1) # Make all rows expandable to push content to center vertically


        # Title Label
        # Use column 1 and 2 for content, with spacers on 0 and 3
        self.title_label = customtkinter.CTkLabel(self, text="Register New Account", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=1, columnspan=2, pady=(50, 20), sticky="s") # Use sticky

        # Username Input
        self.username_label = customtkinter.CTkLabel(self, text="Username:")
        self.username_label.grid(row=1, column=1, padx=(20, 5), pady=5, sticky="e")
        self.username_entry = customtkinter.CTkEntry(self, placeholder_text="Enter username", width=250)
        self.username_entry.grid(row=1, column=2, padx=(5, 20), pady=5, sticky="w")

        # Password Input
        self.password_label = customtkinter.CTkLabel(self, text="Password:")
        self.password_label.grid(row=2, column=1, padx=(20, 5), pady=5, sticky="e")
        self.password_entry = customtkinter.CTkEntry(self, placeholder_text="Enter password", show="*", width=250)
        self.password_entry.grid(row=2, column=2, padx=(5, 20), pady=5, sticky="w")

        # Confirm Password Input
        self.confirm_password_label = customtkinter.CTkLabel(self, text="Confirm Password:")
        self.confirm_password_label.grid(row=3, column=1, padx=(20, 5), pady=5, sticky="e")
        self.confirm_password_entry = customtkinter.CTkEntry(self, placeholder_text="Confirm password", show="*", width=250)
        self.confirm_password_entry.grid(row=3, column=2, padx=(5, 20), pady=5, sticky="w")

        # Contact Information (Optional)
        self.contact_info_label = customtkinter.CTkLabel(self, text="Contact Info (Optional):", font=customtkinter.CTkFont(weight="bold"))
        self.contact_info_label.grid(row=4, column=1, columnspan=2, pady=(20,5), sticky="s")

        self.email_label = customtkinter.CTkLabel(self, text="Email:")
        self.email_label.grid(row=5, column=1, padx=(20, 5), pady=5, sticky="e")
        self.email_entry = customtkinter.CTkEntry(self, placeholder_text="Enter email", width=250)
        self.email_entry.grid(row=5, column=2, padx=(5, 20), pady=5, sticky="w")

        self.phone_label = customtkinter.CTkLabel(self, text="Phone:")
        self.phone_label.grid(row=6, column=1, padx=(20, 5), pady=5, sticky="e")
        self.phone_entry = customtkinter.CTkEntry(self, placeholder_text="Enter phone number", width=250)
        self.phone_entry.grid(row=6, column=2, padx=(5, 20), pady=5, sticky="w")

        # Register Button
        self.register_button = customtkinter.CTkButton(self, text="Register", command=self._register_account)
        self.register_button.grid(row=7, column=1, columnspan=2, pady=20, sticky="n")

        # Go to Login Button - CORRECTED HERE
        self.login_button = customtkinter.CTkButton(self, text="Already have an account? Login", command=lambda: self.show_login_callback("login"), fg_color="transparent", text_color="gray")
        self.login_button.grid(row=8, column=1, columnspan=2, pady=5, sticky="n")

        # Back to Main Menu Button - CORRECTED HERE
        self.back_button = customtkinter.CTkButton(self, text="Back to Main Menu", command=lambda: self.show_main_menu_callback("main_menu"), fg_color="transparent", text_color="gray")
        self.back_button.grid(row=9, column=1, columnspan=2, pady=5, sticky="n")

        # Message Label for feedback
        self.message_label = customtkinter.CTkLabel(self, text="", text_color="red")
        self.message_label.grid(row=10, column=1, columnspan=2, pady=(5, 50), sticky="n")

    def _register_account(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()

        # Basic input validation
        if not username or not password or not confirm_password:
            self.message_label.configure(text="All fields must be filled.")
            return
        if password != confirm_password:
            self.message_label.configure(text="Passwords do not match.")
            return
        if len(password) < 6: # Example: Minimum password length
            self.message_label.configure(text="Password must be at least 6 characters long.")
            return

        contact_info = {}
        if email:
            contact_info['email'] = email
        if phone:
            contact_info['phone'] = phone

        # Attempt to register using UserManager
        user_id = self.user_manager.register_user(username, password, contact_info=contact_info)

        if user_id:
            self.message_label.configure(text=f"Registration successful! User ID: {user_id}", text_color="green")
            logger.info(f"GUI: User '{username}' registered.")
            self.reset_fields() # Clear fields after successful registration
            # Optionally, navigate to login screen or main menu
            # self.show_login_callback() # You might want to automatically go to login after successful registration
        else:
            # Error message will be set by UserManager if username exists
            self.message_label.configure(text=self.user_manager.users_status_message, text_color="red")
            logger.warning(f"GUI: Registration attempt for '{username}' failed. Message: {self.user_manager.users_status_message}")

    def reset_fields(self):
        """Clears all input fields and messages."""
        self.username_entry.delete(0, customtkinter.END)
        self.password_entry.delete(0, customtkinter.END)
        self.confirm_password_entry.delete(0, customtkinter.END)
        self.email_entry.delete(0, customtkinter.END)
        self.phone_entry.delete(0, customtkinter.END)
        self.message_label.configure(text="")