import customtkinter # Imports the CustomTkinter library for modern GUI elements
import logging # Imports the logging module for application logging
import tkinter.messagebox as messagebox # Imports messagebox for displaying pop-up messages

logger = logging.getLogger(__name__) # Initializes a logger for this module

class RegisterFrame(customtkinter.CTkFrame):
    def __init__(self, master, user_manager, switch_to_login_callback): # Adjusted parameters
        super().__init__(master) # Calls the constructor of the parent class (customtkinter.CTkFrame)
        self.user_manager = user_manager # Stores the UserManager instance to handle user registration
        self.switch_to_login_callback = switch_to_login_callback # Stores the callback function to switch to the login screen after successful registration

        # --- Configure grid for the frame itself to expand symmetrically ---
        self.grid_columnconfigure((0, 3), weight=1) # Makes columns 0 and 3 expandable, acting as spacers
        self.grid_columnconfigure((1, 2), weight=0) # Sets columns 1 and 2 (content columns) to a fixed size
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1) # Makes all rows expandable to push content to the center vertically

        # Title Label
        self.title_label = customtkinter.CTkLabel(self, text="Register New Account", font=customtkinter.CTkFont(size=24, weight="bold")) # Creates the registration title label
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

        # Confirm Password Entry
        self.confirm_password_label = customtkinter.CTkLabel(self, text="Confirm Password:") # Creates confirm password label
        self.confirm_password_label.grid(row=3, column=1, padx=10, pady=5, sticky="w") # Places confirm password label
        self.confirm_password_entry = customtkinter.CTkEntry(self, width=200, show="*") # Creates confirm password input field
        self.confirm_password_entry.grid(row=3, column=2, padx=10, pady=5, sticky="ew") # Places confirm password input field

        # Email Entry (Optional)
        self.email_label = customtkinter.CTkLabel(self, text="Email (Optional):") # Creates email label
        self.email_label.grid(row=4, column=1, padx=10, pady=5, sticky="w") # Places email label
        self.email_entry = customtkinter.CTkEntry(self, width=200) # Creates email input field
        self.email_entry.grid(row=4, column=2, padx=10, pady=5, sticky="ew") # Places email input field

        # Phone Entry (Optional)
        self.phone_label = customtkinter.CTkLabel(self, text="Phone (Optional):") # Creates phone label
        self.phone_label.grid(row=5, column=1, padx=10, pady=5, sticky="w") # Places phone label
        self.phone_entry = customtkinter.CTkEntry(self, width=200) # Creates phone input field
        self.phone_entry.grid(row=5, column=2, padx=10, pady=5, sticky="ew") # Places phone input field

        # Register Button
        self.register_button = customtkinter.CTkButton(self, text="Register", command=self._register_account) # Creates register button, linked to _register_account method
        self.register_button.grid(row=6, column=1, columnspan=2, pady=20) # Places register button, spanning two columns

        # Back to Login Link/Button
        self.login_link_label = customtkinter.CTkLabel(self, text="Already have an account?") # Creates prompt for existing account
        self.login_link_label.grid(row=7, column=1, padx=10, pady=5, sticky="e") # Places prompt
        self.login_link_button = customtkinter.CTkButton(self, text="Login", fg_color="transparent", text_color="deepskyblue", hover_color="gray70",
                                                         command=self.switch_to_login_callback) # Creates login button (looks like a link), linked to switch_to_login_callback
        self.login_link_button.grid(row=7, column=2, padx=10, pady=5, sticky="w") # Places login button

        # Message Label for feedback (e.g., registration success/failure)
        self.message_label = customtkinter.CTkLabel(self, text="", text_color="red") # Creates a label to display messages, defaulting to red text for errors
        self.message_label.grid(row=8, column=1, columnspan=2, pady=(5, 50), sticky="n") # Places message label, spanning two columns

    def _register_account(self):
        """
        Handles the user registration process.
        Retrieves user input, performs validation, and calls UserManager to create a new user.
        """
        username = self.username_entry.get().strip() # Gets username from entry field
        password = self.password_entry.get().strip() # Gets password from entry field
        confirm_password = self.confirm_password_entry.get().strip() # Gets confirm password from entry field
        email = self.email_entry.get().strip() # Gets email from entry field
        phone = self.phone_entry.get().strip() # Gets phone from entry field

        # Input Validation
        if not username or not password or not confirm_password: # Checks for mandatory fields
            self.message_label.configure(text="Username, Password, and Confirm Password cannot be empty.") # Displays error message
            return # Stops function execution

        if password != confirm_password: # Checks if passwords match
            self.message_label.configure(text="Passwords do not match.") # Displays error message
            return # Stops function execution

        contact_info = {} # Dictionary to store optional contact information
        if email:
            contact_info['email'] = email # Adds email if provided
        if phone:
            contact_info['phone'] = phone # Adds phone if provided

        # Attempt to register using UserManager
        user_id = self.user_manager.register_user(username, password, contact_info=contact_info) # Calls UserManager to register the user

        if user_id: # If registration is successful (user_id is returned)
            self.message_label.configure(text=f"Registration successful! Please log in.", text_color="green") # Displays success message in green
            logger.info(f"GUI: User '{username}' registered.") # Logs successful registration
            self.clear_inputs() # Clears input fields after successful registration
            self.switch_to_login_callback() # Calls the callback to automatically go to the login screen
        else:
            # Error message will be set by UserManager if username already exists
            self.message_label.configure(text=self.user_manager.users_status_message, text_color="red") # Displays error message from UserManager
            logger.warning(f"GUI: Registration attempt for '{username}' failed. Message: {self.user_manager.users_status_message}") # Logs failed registration attempt

    def clear_inputs(self): # Renamed for consistency
        """Clears all input fields and messages on the registration screen."""
        self.username_entry.delete(0, customtkinter.END) # Clears username entry
        self.password_entry.delete(0, customtkinter.END) # Clears password entry
        self.confirm_password_entry.delete(0, customtkinter.END) # Clears confirm password entry
        self.email_entry.delete(0, customtkinter.END) # Clears email entry
        self.phone_entry.delete(0, customtkinter.END) # Clears phone entry
        self.message_label.configure(text="") # Clears any displayed messages