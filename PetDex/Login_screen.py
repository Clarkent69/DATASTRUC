import customtkinter # Imports the CustomTkinter library for modern GUI elements
import logging # Imports the logging module for application logging
import tkinter.messagebox as messagebox # Imports messagebox for displaying pop-up messages (e.g., validation errors)

logger = logging.getLogger(__name__) # Initializes a logger for this module

class LoginFrame(customtkinter.CTkFrame):
    def __init__(self, master, user_manager, show_dashboard_screen_callback, switch_to_register_callback):
        super().__init__(master) # Calls the constructor of the parent class (customtkinter.CTkFrame)
        self.user_manager = user_manager # Stores the UserManager instance to handle user authentication
        self.show_dashboard_screen_callback = show_dashboard_screen_callback # Stores the callback function to show the dashboard on successful login
        self.switch_to_register_callback = switch_to_register_callback # Stores the callback function to switch to the registration screen

        # Configure grid for the frame itself to expand symmetrically
        self.grid_columnconfigure((0, 3), weight=1) # Makes columns 0 and 3 expandable, acting as spacers
        self.grid_columnconfigure((1, 2), weight=0) # Sets columns 1 and 2 (content columns) to a fixed size
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1) # Makes all rows expandable to push content to the center vertically

        # Title Label
        self.title_label = customtkinter.CTkLabel(self, text="Login to PetDex", font=customtkinter.CTkFont(size=24, weight="bold")) # Creates the login title label
        self.title_label.grid(row=0, column=1, columnspan=2, pady=(50, 20), sticky="s") # Places the title label, spanning two columns

        # Username Entry
        self.username_label = customtkinter.CTkLabel(self, text="Username:") # Creates username label
        self.username_label.grid(row=1, column=1, padx=10, pady=5, sticky="w") # Places username label
        self.username_entry = customtkinter.CTkEntry(self, width=200) # Creates username input field
        self.username_entry.grid(row=1, column=2, padx=10, pady=5, sticky="ew") # Places username input field

        # Password Entry
        self.password_label = customtkinter.CTkLabel(self, text="Password:") # Creates password label
        self.password_label.grid(row=2, column=1, padx=10, pady=5, sticky="w") # Places password label
        self.password_entry = customtkinter.CTkEntry(self, width=200, show="*") # Creates password input field, hiding input with asterisks
        self.password_entry.grid(row=2, column=2, padx=10, pady=5, sticky="ew") # Places password input field

        # Login Button
        self.login_button = customtkinter.CTkButton(self, text="Login", command=self._login_account) # Creates login button, linked to _login_account method
        self.login_button.grid(row=3, column=1, columnspan=2, pady=20) # Places login button, spanning two columns

        # Register Link/Button
        self.register_label = customtkinter.CTkLabel(self, text="Don't have an account?") # Creates prompt for registration
        self.register_label.grid(row=4, column=1, padx=10, pady=5, sticky="e") # Places registration prompt
        self.register_button = customtkinter.CTkButton(self, text="Register", fg_color="transparent", text_color="deepskyblue", hover_color="gray70",
                                                       command=self.switch_to_register_callback) # Creates register button (looks like a link), linked to switch_to_register_callback
        self.register_button.grid(row=4, column=2, padx=10, pady=5, sticky="w") # Places register button

        # Message Label for feedback (e.g., login success/failure)
        self.message_label = customtkinter.CTkLabel(self, text="", text_color="red") # Creates a label to display messages, defaulting to red text for errors
        self.message_label.grid(row=5, column=1, columnspan=2, pady=(5, 50), sticky="n") # Places message label, spanning two columns

    def _login_account(self):
        """
        Handles the login process.
        Retrieves username and password, validates input, and calls UserManager for authentication.
        """
        username = self.username_entry.get().strip() # Gets username from entry field and removes leading/trailing whitespace
        password = self.password_entry.get().strip() # Gets password from entry field and removes leading/trailing whitespace

        if not username or not password: # Basic validation: check if both fields are empty
            self.message_label.configure(text="Please enter both username and password.") # Displays error message
            return # Stops function execution

        user_id = self.user_manager.login_user(username, password) # Calls UserManager to attempt login and get user ID

        if user_id: # If login is successful (user_id is returned)
            self.message_label.configure(text=f"Login successful! Welcome, {username}!", text_color="green") # Displays success message in green
            logger.info(f"GUI: User '{username}' logged in successfully.") # Logs successful login
            self.clear_inputs() # Clears input fields after successful login
            self.show_dashboard_screen_callback(user_id) # Calls the callback to switch to the dashboard screen, passing the user ID
        else: # If login fails
            # Error message will be set by UserManager if login fails (e.g., invalid credentials)
            self.message_label.configure(text=self.user_manager.users_status_message, text_color="red") # Displays error message from UserManager
            logger.warning(f"GUI: Login attempt for '{username}' failed. Message: {self.user_manager.users_status_message}") # Logs failed login attempt

    def clear_inputs(self): # Renamed for consistency
        """Clears all input fields and messages on the login screen."""
        self.username_entry.delete(0, customtkinter.END) # Clears the username entry field
        self.password_entry.delete(0, customtkinter.END) # Clears the password entry field
        self.message_label.configure(text="") # Clears any displayed messages