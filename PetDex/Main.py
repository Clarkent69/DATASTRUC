import customtkinter # Imports the CustomTkinter library for GUI components
import logging # Imports the logging module for application-wide logging
import sys # Imports sys module for system-specific parameters and functions (e.g., for exiting the application)

# Basic logging configuration for the entire application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) # Initializes a logger for the main application file

# Import backend managers and GUI screens
from User_registration import UserManager # Imports the class for managing user registration and authentication
from Pet_data_manager import PetDataManager # Imports the class for managing pet data (registration, update, delete, lost/found)
from Report import ReportManager # Imports the class for generating various reports
from database_manager import InMemoryDBManager # Imports the class for handling all database interactions

# Import CustomTkinter GUI screen classes
from Login_screen import LoginFrame # Imports the login screen frame
from Register_screen import RegisterFrame # Imports the registration screen frame
from Dashboard_screen import DashboardFrame # Imports the dashboard screen frame

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__() # Calls the constructor of the parent class (customtkinter.CTk)

        self.title("PetDex: Digital Database for Pet Registration and Monitoring") # Sets the title of the main application window
        self.geometry("1000x700") # Sets the initial size of the application window
        self.grid_rowconfigure(0, weight=1) # Makes the single row in the main window grid expandable
        self.grid_columnconfigure(0, weight=1) # Makes the single column in the main window grid expandable

        customtkinter.set_appearance_mode("System") # Sets the GUI appearance mode to follow the system's theme
        customtkinter.set_default_color_theme("blue") # Sets the default color theme for CustomTkinter widgets

        # Store the currently logged-in user ID
        self.current_user_id = None # Initializes current_user_id to None; will store the ID of the successfully logged-in user

        # --- Backend Managers Initialization ---
        self.db_manager = InMemoryDBManager() # Initializes the DatabaseManager, establishing connection and creating tables
        self.user_manager = UserManager(self.db_manager) # Initializes UserManager, passing the DatabaseManager instance
        self.pet_data_manager = PetDataManager(self.db_manager) # Initializes PetDataManager, passing the DatabaseManager instance
        self.report_manager = ReportManager(self.pet_data_manager) # Initializes ReportManager, passing the PetDataManager instance

        # --- GUI Screen Frames Initialization ---
        # Each screen is initialized with necessary managers and callbacks for navigation
        self.login_frame = LoginFrame(self, self.user_manager, self.show_dashboard_screen, self.show_register_screen) # Login screen instance
        self.login_frame.grid(row=0, column=0, sticky="nsew") # Places login frame, initially hidden

        self.register_frame = RegisterFrame(self, self.user_manager, self.show_login_screen) # Register screen instance
        self.register_frame.grid(row=0, column=0, sticky="nsew") # Places register frame, initially hidden

        self.dashboard_frame = DashboardFrame(self, self.user_manager, self.pet_data_manager, self.report_manager, self.show_login_screen) # Dashboard screen instance
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew") # Places dashboard frame, initially hidden

        self.show_frame("login") # Sets the initial visible screen to the login screen

    def show_frame(self, page_name):
        """
        Manages which GUI frame is currently visible.
        It raises the requested frame to the top and handles specific data loading for some screens.
        """
        # Dictionary mapping page names to their corresponding frame objects
        frames = {
            "login": self.login_frame,
            "register": self.register_frame,
            "dashboard": self.dashboard_frame
        }
        frame = frames.get(page_name) # Gets the frame object based on the page name
        if frame: # If a valid frame is found
            frame.tkraise() # Raises the selected frame to the top of the stacking order, making it visible
            logger.info(f"Switched to {page_name.capitalize()} Screen.") # Logs the screen transition

            # Special handling for clearing inputs or loading data when switching screens
            if page_name == "login":
                self.login_frame.clear_inputs() # Clears login input fields
                logger.info("Switched to Login Screen.")
            elif page_name == "register":
                self.register_frame.clear_inputs() # Clears registration input fields
                logger.info("Switched to Register Screen.")
            elif page_name == "dashboard":
                # Dashboard needs user_id to load specific data
                # This method should only be called after successful login/registration
                if self.current_user_id: # Checks if a user is logged in
                    self.dashboard_frame.load_user_data(self.current_user_id) # Loads user profile data
                    self.dashboard_frame.load_pet_data(self.current_user_id) # Loads owned pet data
                    self.dashboard_frame.load_stray_data() # Loads all stray data (public view)
                    logger.info(f"Switched to Dashboard Screen for user: {self.current_user_id}") # Logs dashboard entry for the user
                else:
                    logger.warning("Attempted to show dashboard without a logged-in user.") # Warns if dashboard is accessed without login
                    self.show_frame("login") # Redirects to login if no user is set

    def show_login_screen(self):
        """Callback function to switch to the login screen."""
        self.show_frame("login")

    def show_register_screen(self):
        """Callback function to switch to the register screen."""
        self.show_frame("register")

    def show_dashboard_screen(self, user_id):
        """
        Callback function to switch to the dashboard screen,
        setting the current user ID upon successful login/registration.
        """
        self.current_user_id = user_id # Stores the ID of the newly logged-in/registered user
        self.show_frame("dashboard") # Switches to the dashboard frame

    def destroy(self):
        """
        Overrides the default destroy method to ensure the database connection is closed
        before the application exits.
        """
        logger.info("Closing application. Closing database connection.") # Logs application shutdown
        if self.db_manager: # Checks if the database manager exists
            self.db_manager.close() # Closes the database connection
        super().destroy() # Calls the parent class's destroy method

if __name__ == '__main__':
    app = App() # Creates an instance of the main application
    app.mainloop() # Starts the CustomTkinter event loop, which keeps the application running