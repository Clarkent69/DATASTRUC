import customtkinter
import os
import json
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import your backend managers and GUI screens
from User_registration import UserManager
from Pet_data_manager import PetDataManager
from Report import ReportManager
from Search import SearchManager
from Register_screen import RegisterFrame
from Login_screen import LoginFrame
from Search import SearchManager
from Dashboard_screen import DashboardFrame # Import the new Dashboard GUI screen

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("PetDex: Digital Database for Pet Registration and Monitoring")
        self.geometry("1000x700")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("dark-blue")

        # Store the currently logged-in user ID
        self.current_user_id = None

        # --- Backend Managers Initialization ---
        self.user_manager = UserManager()
        self.pet_data_manager = PetDataManager() # Initialize PetDataManager
        self.search_manager = SearchManager(self.pet_data_manager)
        # Initialize ReportManager, passing it the pet_data_manager
        self.report_manager = ReportManager(self.pet_data_manager) # Initialize ReportManager
        # Initialize SearchManager, passing it the pet_data_manager
        self.search_manager = SearchManager(self.pet_data_manager) # <--- ADD THIS LINE: Initialize SearchManager

        # Dictionary to hold frames
        self.frames = {}
        self._create_main_menu_frame()
        self._create_login_frame()
        self._create_register_frame()
        # Dashboard frame will be created when a user logs in successfully

        self.show_frame("main_menu")

    def show_frame(self, name):
        """Hides current frame and shows the requested one."""
        for frame in self.frames.values():
            frame.grid_forget() # Hide all frames

        if name == "login":
            self.frames["login"].reset_fields()
        elif name == "register":
            self.frames["register"].reset_fields()
        
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    def _create_login_frame(self):
        """Creates the login frame."""
        login_frame = LoginFrame(self, self.user_manager, self.show_dashboard_screen, self.show_frame)
        self.frames["login"] = login_frame

    def _create_register_frame(self):
        """Creates the register frame."""
        register_frame = RegisterFrame(self, self.user_manager, self.show_frame, self.show_frame)
        self.frames["register"] = register_frame

    def _create_main_menu_frame(self):
        """Creates the main menu frame."""
        main_menu_frame = customtkinter.CTkFrame(self)
        main_menu_frame.grid_columnconfigure(0, weight=1)
        main_menu_frame.grid_rowconfigure((0,1,2,3,4), weight=1)

        label = customtkinter.CTkLabel(main_menu_frame, text="Welcome to PetDex!", font=customtkinter.CTkFont(size=24, weight="bold"))
        label.grid(row=0, column=0, pady=50, sticky="nsew")

        btn_login = customtkinter.CTkButton(main_menu_frame, text="Login", command=lambda: self.show_frame("login"))
        btn_login.grid(row=1, column=0, pady=10)

        btn_register = customtkinter.CTkButton(main_menu_frame, text="Register", command=lambda: self.show_frame("register"))
        btn_register.grid(row=2, column=0, pady=10)

        btn_exit = customtkinter.CTkButton(main_menu_frame, text="Exit", command=self.destroy)
        btn_exit.grid(row=3, column=0, pady=10)

        self.frames["main_menu"] = main_menu_frame

    def show_dashboard_screen(self, user_id):
        self.current_user_id = user_id
        logger.info(f"User {user_id} logged in. Displaying dashboard.")

        if "dashboard" in self.frames:
            self.frames["dashboard"].destroy()

        self.frames["dashboard"] = DashboardFrame(
            master=self,
            user_manager=self.user_manager,
            pet_data_manager=self.pet_data_manager,
            show_main_menu_callback=lambda: self.show_frame("main_menu"),
            report_manager=self.report_manager,
            search_manager=self.search_manager, # Pass the search manager here
        )
        self.frames["dashboard"].set_current_user(user_id)
        self.show_frame("dashboard")


if __name__ == "__main__":
    app = App()
    app.mainloop()