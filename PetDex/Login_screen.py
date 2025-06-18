import customtkinter
import logging
import tkinter.messagebox as messagebox

logger = logging.getLogger(__name__)

class LoginFrame(customtkinter.CTkFrame):
    def __init__(self, master, user_manager, show_dashboard_screen_callback, show_main_menu_callback):
        super().__init__(master)
        self.user_manager = user_manager
        self.show_dashboard_screen_callback = show_dashboard_screen_callback
        self.show_main_menu_callback = show_main_menu_callback # Store the callback for main menu navigation

        # Configure grid for the frame itself to expand
        self.grid_columnconfigure(0, weight=1) # Left spacer column
        self.grid_columnconfigure(1, weight=0) # Column for labels/content
        self.grid_columnconfigure(2, weight=0) # Column for entries/content
        self.grid_columnconfigure(3, weight=1) # Right spacer column
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1) # Make all rows expandable to push content to center vertically

        # Title Label
        self.title_label = customtkinter.CTkLabel(self, text="Login to PetDex", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=1, columnspan=2, pady=(50, 20), sticky="s") # Use sticky="s" to align to south of expanded row

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

        # Login Button
        self.login_button = customtkinter.CTkButton(self, text="Login", command=self._login_account)
        self.login_button.grid(row=3, column=1, columnspan=2, pady=20, sticky="n")

        # Go to Register Button
        self.register_button = customtkinter.CTkButton(self, text="Don't have an account? Register", command=lambda: self.show_main_menu_callback("register"), fg_color="transparent", text_color="gray")
        self.register_button.grid(row=4, column=1, columnspan=2, pady=5, sticky="n")

        # Back to Main Menu Button (if desired, or use the register button to implicitly go back)
        self.back_button = customtkinter.CTkButton(self, text="Back to Main Menu", command=lambda: self.show_main_menu_callback("main_menu"), fg_color="transparent", text_color="gray")
        self.back_button.grid(row=5, column=1, columnspan=2, pady=5, sticky="n")

        # Message Label for feedback
        self.message_label = customtkinter.CTkLabel(self, text="", text_color="red")
        self.message_label.grid(row=6, column=1, columnspan=2, pady=(5, 50), sticky="n")

    def _login_account(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.message_label.configure(text="Please enter both username and password.")
            return

        user_id = self.user_manager.login_user(username, password)

        if user_id:
            self.message_label.configure(text=f"Login successful! Welcome, {username}!", text_color="green")
            logger.info(f"GUI: User '{username}' logged in successfully.")
            self.reset_fields()
            self.show_dashboard_screen_callback(user_id) # Call the dashboard screen with the user ID
        else:
            self.message_label.configure(text=self.user_manager.users_status_message, text_color="red")
            logger.warning(f"GUI: Login attempt for '{username}' failed. Message: {self.user_manager.users_status_message}")

    def reset_fields(self):
        """Clears all input fields and messages."""
        self.username_entry.delete(0, customtkinter.END)
        self.password_entry.delete(0, customtkinter.END)
        self.message_label.configure(text="")