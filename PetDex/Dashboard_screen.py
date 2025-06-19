import customtkinter # Imports the CustomTkinter library for modern GUI elements
import logging # Imports the logging module for application logging
import datetime # Imports datetime for handling date and time objects
import tkinter.messagebox as messagebox # Imports messagebox for displaying pop-up messages
from PIL import Image, ImageTk # Imports Image and ImageTk for handling images (e.g., pet photos)
import os # Imports the os module for interacting with the operating system (e.g., file paths)

from Update_pet_dialog import UpdatePetDialog # Imports the custom dialog for updating pet details

logger = logging.getLogger(__name__) # Initializes a logger for this module

class DashboardFrame(customtkinter.CTkFrame):
    def __init__(self, master, user_manager, pet_data_manager, report_manager, switch_to_login_callback):
        super().__init__(master) # Calls the constructor of the parent class (customtkinter.CTkFrame)
        self.user_manager = user_manager # Stores the UserManager instance for user-related operations
        self.pet_data_manager = pet_data_manager # Stores the PetDataManager instance for pet data operations
        self.report_manager = report_manager # Stores the ReportManager instance for generating reports
        self.switch_to_login_callback = switch_to_login_callback # Stores the callback function to switch to the login screen
        self.current_user_id = None # Initializes current_user_id to None; will store the ID of the logged-in user

        # Current selected pet/stray in lists for update/delete
        self.selected_pet_id = None # Stores the ID of the currently selected owned pet in the list
        self.selected_stray_id = None # Stores the ID of the currently selected stray pet in the list

        # Configure grid for the Dashboard frame itself
        self.grid_columnconfigure(1, weight=1) # Makes the second column (content area) expandable
        self.grid_rowconfigure(0, weight=1) # Makes the first row (main content) expandable

        # ------------------------------------------------------------------------- Sidebar Navigation ---------------------------------------------------------------------
        self.sidebar_frame = customtkinter.CTkFrame(self, width=150, corner_radius=0) # Creates the sidebar frame
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew") # Places the sidebar on the left, spanning multiple rows
        self.sidebar_frame.grid_rowconfigure(7, weight=1) # Pushes the logout button to the bottom of the sidebar

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="PetDex", font=customtkinter.CTkFont(size=24, weight="bold")) # Creates the application logo label
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10)) # Places the logo at the top of the sidebar

        self.home_button = customtkinter.CTkButton(self.sidebar_frame, text="Dashboard", command=lambda: self.select_tab("dashboard_tab")) # Button to switch to Dashboard tab
        self.home_button.grid(row=1, column=0, padx=20, pady=10) # Places the Dashboard button

        self.add_pet_button = customtkinter.CTkButton(self.sidebar_frame, text="Manage My Pets", command=lambda: self.select_tab("manage_pets_tab")) # Button to switch to Manage My Pets tab
        self.add_pet_button.grid(row=2, column=0, padx=20, pady=10) # Places the Manage My Pets button

        self.stray_reporting_button = customtkinter.CTkButton(self.sidebar_frame, text="Stray Reporting", command=lambda: self.select_tab("stray_reporting_tab")) # Button to switch to Stray Reporting tab
        self.stray_reporting_button.grid(row=3, column=0, padx=20, pady=10) # Places the Stray Reporting button

        self.report_button = customtkinter.CTkButton(self.sidebar_frame, text="Reports", command=lambda: self.select_tab("reports_tab")) # Button to switch to Reports tab
        self.report_button.grid(row=4, column=0, padx=20, pady=10) # Places the Reports button

        self.settings_button = customtkinter.CTkButton(self.sidebar_frame, text="Settings", command=lambda: self.select_tab("settings_tab")) # Button to switch to Settings tab
        self.settings_button.grid(row=5, column=0, padx=20, pady=10) # Places the Settings button

        self.logout_button = customtkinter.CTkButton(self.sidebar_frame, text="Logout", command=self.switch_to_login_callback) # Button to log out and return to login screen
        self.logout_button.grid(row=8, column=0, padx=20, pady=(10, 20), sticky="s") # Places the Logout button at the bottom

        # ------------------------------------------------------------------------- Main Content Area (Tab View) ---------------------------------------------------------------------
        self.tab_view = customtkinter.CTkTabview(self, width=800, height=580) # Creates a tab view to organize different sections
        self.tab_view.grid(row=0, column=1, padx=20, pady=20, sticky="nsew") # Places the tab view in the main content area

        # Add tabs to the tab view
        self.tab_view.add("Dashboard")
        self.tab_view.add("Manage My Pets")
        self.tab_view.add("Stray Reporting")
        self.tab_view.add("Reports")
        self.tab_view.add("Settings")

        self.tab_view._segmented_button.grid_forget() # Hides the default segmented button for tab switching, as custom buttons are used

        # ------------------------------------------------------------------------- Dashboard Tab ---------------------------------------------------------------------
        self.dashboard_tab = self.tab_view.tab("Dashboard") # Gets the "Dashboard" tab frame
        self.dashboard_tab.grid_columnconfigure(0, weight=1) # Makes the column in dashboard tab expandable
        self.dashboard_tab.grid_rowconfigure(0, weight=1) # Makes the row in dashboard tab expandable

        self.dashboard_content_frame = customtkinter.CTkFrame(self.dashboard_tab) # Frame to hold dashboard specific content
        self.dashboard_content_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10) # Places the content frame within the tab
        self.dashboard_content_frame.grid_columnconfigure(0, weight=1) # Makes the column in content frame expandable
        self.dashboard_content_frame.grid_rowconfigure((0,1,2,3), weight=0) # Sets fixed size for info labels
        self.dashboard_content_frame.grid_rowconfigure(4, weight=1) # Makes the scrollable frame row expandable

        customtkinter.CTkLabel(self.dashboard_content_frame, text="Welcome to Your PetDex Dashboard!", font=customtkinter.CTkFont(size=20, weight="bold")).grid(row=0, column=0, pady=10) # Welcome message

        # User Info Section
        self.user_info_label = customtkinter.CTkLabel(self.dashboard_content_frame, text="", wraplength=700, justify="left") # Label to display user's profile information
        self.user_info_label.grid(row=1, column=0, padx=20, pady=5, sticky="ew") # Places the user info label

        # Pets Summary Section
        self.pet_summary_label = customtkinter.CTkLabel(self.dashboard_content_frame, text="", wraplength=700, justify="left") # Label to display summary of owned pets
        self.pet_summary_label.grid(row=2, column=0, padx=20, pady=5, sticky="ew") # Places the pet summary label

        # Lost/Stray Summary Section
        self.lost_stray_summary_label = customtkinter.CTkLabel(self.dashboard_content_frame, text="", wraplength=700, justify="left") # Label to display summary of lost/stray pets
        self.lost_stray_summary_label.grid(row=3, column=0, padx=20, pady=5, sticky="ew") # Places the lost/stray summary label

        # Display owned pets in dashboard
        customtkinter.CTkLabel(self.dashboard_content_frame, text="Your Registered Pets:", font=customtkinter.CTkFont(size=16, weight="bold")).grid(row=4, column=0, pady=(20,10), sticky="sw") # Label for registered pets list
        self.dashboard_pets_scroll_frame = customtkinter.CTkScrollableFrame(self.dashboard_content_frame) # Scrollable frame to display registered pets
        self.dashboard_pets_scroll_frame.grid(row=5, column=0, padx=10, pady=10, sticky="nsew") # Places the scrollable frame
        self.dashboard_pets_scroll_frame.grid_columnconfigure(0, weight=1) # Makes the column in the scrollable frame expandable

        # ------------------------------------------------------------------------- Manage My Pets Tab ---------------------------------------------------------------------
        self.manage_pets_tab = self.tab_view.tab("Manage My Pets") # Gets the "Manage My Pets" tab frame
        self.manage_pets_tab.grid_columnconfigure(0, weight=1) # Makes the column in the tab expandable
        self.manage_pets_tab.grid_rowconfigure(0, weight=1) # Makes the row in the tab expandable

        self.manage_pets_frame = customtkinter.CTkFrame(self.manage_pets_tab) # Frame to hold pet management content
        self.manage_pets_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10) # Places the frame within the tab
        self.manage_pets_frame.grid_columnconfigure(0, weight=1) # Makes the column in the frame expandable
        self.manage_pets_frame.grid_rowconfigure(1, weight=1) # Makes the scrollable frame row expandable

        customtkinter.CTkLabel(self.manage_pets_frame, text="Register New Pet", font=customtkinter.CTkFont(size=18, weight="bold")).grid(row=0, column=0, pady=10, sticky="w") # Label for new pet registration section

        # Pet Registration Form
        self.add_pet_form_frame = customtkinter.CTkFrame(self.manage_pets_frame) # Frame for the add pet form
        self.add_pet_form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew") # Places the form frame
        self.add_pet_form_frame.grid_columnconfigure(1, weight=1) # Makes the second column (entry fields) expandable

        labels_and_entries_pets = [
            ("Pet Name:", "pet_name_entry"),
            ("Species:", "species_optionmenu", ["Dog", "Cat"]), # Option menu for species
            ("Breed (Optional):", "breed_entry"),
            ("Age (Years):", "age_entry"),
            ("Color:", "color_entry"),
            ("Image Path (Optional):", "image_path_entry")
        ]

        self.pet_form_widgets = {} # Dictionary to store references to pet form widgets
        for i, (label_text, widget_name, *options) in enumerate(labels_and_entries_pets): # Loops through the list to create labels and entry/option widgets
            row = i # Current row index
            customtkinter.CTkLabel(self.add_pet_form_frame, text=label_text).grid(row=row, column=0, padx=5, pady=5, sticky="w") # Creates and places label
            if widget_name == "species_optionmenu": # Special handling for species dropdown
                widget = customtkinter.CTkOptionMenu(self.add_pet_form_frame, values=options[0]) # Creates option menu
                widget.set(options[0][0]) # Set default value for species
            else:
                widget = customtkinter.CTkEntry(self.add_pet_form_frame) # Creates a standard entry field
            widget.grid(row=row, column=1, padx=5, pady=5, sticky="ew") # Places the widget
            self.pet_form_widgets[widget_name] = widget # Stores widget in dictionary for easy access

        self.add_pet_button_form = customtkinter.CTkButton(self.add_pet_form_frame, text="Add Pet", command=self._add_pet) # Button to submit new pet registration
        self.add_pet_button_form.grid(row=len(labels_and_entries_pets), column=0, columnspan=2, pady=10) # Places the add pet button

        customtkinter.CTkLabel(self.manage_pets_frame, text="Your Registered Pets", font=customtkinter.CTkFont(size=18, weight="bold")).grid(row=1, column=0, pady=(20,10), sticky="w") # Label for displaying registered pets list
        self.my_pets_scroll_frame = customtkinter.CTkScrollableFrame(self.manage_pets_frame) # Scrollable frame to display owned pets
        self.my_pets_scroll_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew") # Places the scrollable frame
        self.my_pets_scroll_frame.grid_columnconfigure(0, weight=1) # Makes the column in the scrollable frame expandable

        # ------------------------------------------------------------------------- Stray Reporting Tab ---------------------------------------------------------------------
        self.stray_reporting_tab = self.tab_view.tab("Stray Reporting") # Gets the "Stray Reporting" tab frame
        self.stray_reporting_tab.grid_columnconfigure(0, weight=1) # Makes the column in the tab expandable
        self.stray_reporting_tab.grid_rowconfigure(1, weight=1) # Makes the row for stray list expandable

        customtkinter.CTkLabel(self.stray_reporting_tab, text="Report a Stray Pet", font=customtkinter.CTkFont(size=18, weight="bold")).grid(row=0, column=0, pady=10, sticky="w") # Label for stray reporting section

        # Stray Reporting Form
        self.report_stray_form_frame = customtkinter.CTkFrame(self.stray_reporting_tab) # Frame for the stray reporting form
        self.report_stray_form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew") # Places the form frame
        self.report_stray_form_frame.grid_columnconfigure(1, weight=1) # Makes the second column (entry fields) expandable

        labels_and_entries_strays = [
            ("Species:", "stray_species_optionmenu", ["Dog", "Cat"]), # Option menu for species
            ("Location (Last Seen):", "stray_location_entry"),
            ("Breed (Optional):", "stray_breed_entry"),
            ("Color:", "stray_color_entry"),
            ("Description (Optional):", "stray_description_entry"),
            ("Contact Email (Optional):", "stray_email_entry"),
            ("Contact Phone (Optional):", "stray_phone_entry")
        ]

        self.stray_form_widgets = {} # Dictionary to store references to stray form widgets
        for i, (label_text, widget_name, *options) in enumerate(labels_and_entries_strays): # Loops to create labels and widgets
            row = i # Current row index
            customtkinter.CTkLabel(self.report_stray_form_frame, text=label_text).grid(row=row, column=0, padx=5, pady=5, sticky="w") # Creates and places label
            if "optionmenu" in widget_name: # Special handling for option menus
                widget = customtkinter.CTkOptionMenu(self.report_stray_form_frame, values=options[0]) # Creates option menu
                widget.set(options[0][0]) # Set default value
            elif "description" in widget_name: # Special handling for description (multi-line)
                widget = customtkinter.CTkTextbox(self.report_stray_form_frame, height=70) # Creates a textbox for description
            else:
                widget = customtkinter.CTkEntry(self.report_stray_form_frame) # Creates a standard entry field
            widget.grid(row=row, column=1, padx=5, pady=5, sticky="ew") # Places the widget
            self.stray_form_widgets[widget_name] = widget # Stores widget in dictionary

        self.report_stray_button = customtkinter.CTkButton(self.report_stray_form_frame, text="Report Stray", command=self._report_stray_pet) # Button to submit stray report
        self.report_stray_button.grid(row=len(labels_and_entries_strays), column=0, columnspan=2, pady=10) # Places the report stray button

        customtkinter.CTkLabel(self.stray_reporting_tab, text="Reported Stray Pets (Public)", font=customtkinter.CTkFont(size=18, weight="bold")).grid(row=1, column=0, pady=(20,10), sticky="w") # Label for reported stray pets list
        self.stray_pets_scroll_frame = customtkinter.CTkScrollableFrame(self.stray_reporting_tab) # Scrollable frame to display stray pets
        self.stray_pets_scroll_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew") # Places the scrollable frame
        self.stray_pets_scroll_frame.grid_columnconfigure(0, weight=1) # Makes the column in the scrollable frame expandable

        # ------------------------------------------------------------------------- Reports Tab ---------------------------------------------------------------------
        self.reports_tab = self.tab_view.tab("Reports") # Gets the "Reports" tab frame
        self.reports_tab.grid_columnconfigure(0, weight=1) # Makes the column in the tab expandable
        self.reports_tab.grid_rowconfigure(1, weight=1) # Makes the row for reports content expandable

        self.reports_frame = customtkinter.CTkFrame(self.reports_tab) # Frame to hold reports content
        self.reports_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10) # Places the frame within the tab
        self.reports_frame.grid_columnconfigure(0, weight=1) # Makes the column in the frame expandable
        self.reports_frame.grid_rowconfigure((0,1,2,3), weight=0) # Sets fixed size for report labels
        self.reports_frame.grid_rowconfigure(4, weight=1) # Makes the scrollable frame row expandable

        customtkinter.CTkLabel(self.reports_frame, text="Application Reports", font=customtkinter.CTkFont(size=20, weight="bold")).grid(row=0, column=0, pady=10) # Title for reports section

        self.total_users_label = customtkinter.CTkLabel(self.reports_frame, text="", wraplength=700, justify="left") # Label for total users count
        self.total_users_label.grid(row=1, column=0, padx=20, pady=5, sticky="ew") # Places the label

        self.total_pets_label = customtkinter.CTkLabel(self.reports_frame, text="", wraplength=700, justify="left") # Label for total registered pets count
        self.total_pets_label.grid(row=2, column=0, padx=20, pady=5, sticky="ew") # Places the label

        self.lost_pets_label = customtkinter.CTkLabel(self.reports_frame, text="", wraplength=700, justify="left") # Label for lost pets count
        self.lost_pets_label.grid(row=3, column=0, padx=20, pady=5, sticky="ew") # Places the label

        self.stray_pets_report_label = customtkinter.CTkLabel(self.reports_frame, text="", wraplength=700, justify="left") # Label for stray pets count
        self.stray_pets_report_label.grid(row=4, column=0, padx=20, pady=5, sticky="ew") # Places the label

        # Display Lost Pets in Reports Tab
        customtkinter.CTkLabel(self.reports_frame, text="Lost Pets (Public Reports):", font=customtkinter.CTkFont(size=16, weight="bold")).grid(row=5, column=0, pady=(20,10), sticky="sw") # Label for lost pets list
        self.lost_pets_scroll_frame = customtkinter.CTkScrollableFrame(self.reports_frame) # Scrollable frame for lost pets
        self.lost_pets_scroll_frame.grid(row=6, column=0, padx=10, pady=10, sticky="nsew") # Places the scrollable frame
        self.lost_pets_scroll_frame.grid_columnconfigure(0, weight=1) # Makes the column in the scrollable frame expandable

        # ------------------------------------------------------------------------- Settings Tab ---------------------------------------------------------------------
        self.settings_tab = self.tab_view.tab("Settings") # Gets the "Settings" tab frame
        self.settings_tab.grid_columnconfigure(0, weight=1) # Makes the column in the tab expandable
        self.settings_tab.grid_rowconfigure(0, weight=1) # Makes the row in the tab expandable

        self.settings_frame = customtkinter.CTkFrame(self.settings_tab) # Frame to hold settings content
        self.settings_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10) # Places the frame within the tab
        self.settings_frame.grid_columnconfigure(1, weight=1) # Makes the second column (entry fields) expandable

        customtkinter.CTkLabel(self.settings_frame, text="Profile Settings", font=customtkinter.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=2, pady=10) # Title for profile settings

        # User Profile Fields
        self.settings_widgets = {} # Dictionary to store references to settings widgets
        settings_fields = [
            ("Username:", "username_entry"),
            ("Email:", "email_entry"),
            ("Phone:", "phone_entry"),
            ("New Password:", "new_password_entry", True), # True indicates it's a password field
            ("Confirm New Password:", "confirm_new_password_entry", True)
        ]

        for i, (label_text, widget_name, *is_password) in enumerate(settings_fields): # Loops to create labels and entry widgets for settings
            row = i + 1 # Start from row 1
            customtkinter.CTkLabel(self.settings_frame, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky="w") # Creates and places label
            widget = customtkinter.CTkEntry(self.settings_frame, show="*" if is_password else "") # Creates entry, hides text for password fields
            widget.grid(row=row, column=1, padx=10, pady=5, sticky="ew") # Places the widget
            self.settings_widgets[widget_name] = widget # Stores widget in dictionary

        self.update_profile_button = customtkinter.CTkButton(self.settings_frame, text="Update Profile", command=self._update_profile) # Button to update user profile
        self.update_profile_button.grid(row=len(settings_fields) + 1, column=0, columnspan=2, pady=10) # Places the update profile button

        self.delete_account_button = customtkinter.CTkButton(self.settings_frame, text="Delete Account", fg_color="red", hover_color="darkred", command=self._delete_account) # Button to delete user account
        self.delete_account_button.grid(row=len(settings_fields) + 2, column=0, columnspan=2, pady=10) # Places the delete account button


    def select_tab(self, tab_name):
        """
        Switches the visible tab in the CTkTabview.
        This is called by the sidebar navigation buttons.
        """
        # Mapping of button commands to tab names
        tab_map = {
            "dashboard_tab": "Dashboard",
            "manage_pets_tab": "Manage My Pets",
            "stray_reporting_tab": "Stray Reporting",
            "reports_tab": "Reports",
            "settings_tab": "Settings"
        }
        self.tab_view.set(tab_map.get(tab_name, "Dashboard")) # Sets the active tab in the CTkTabview

        # Reload data specific to certain tabs when they are selected
        if tab_name == "dashboard_tab":
            self.load_user_data(self.current_user_id) # Reloads user and pet data for the dashboard
            self.load_pet_data(self.current_user_id)
            self.load_stray_data() # Reloads stray data
        elif tab_name == "manage_pets_tab":
            self.load_pet_data(self.current_user_id) # Reloads pet data for the manage pets tab
        elif tab_name == "stray_reporting_tab":
            self.load_stray_data() # Reloads stray data for the stray reporting tab
        elif tab_name == "reports_tab":
            self.load_reports_data() # Reloads report data for the reports tab


    def load_user_data(self, user_id):
        """
        Loads and displays the current user's profile data on the dashboard and settings tabs.
        """
        if user_id:
            self.current_user_id = user_id # Sets the current user ID
            user_data = self.user_manager.get_user(user_id) # Fetches user data from the user manager
            if user_data:
                # Update Dashboard Info
                self.user_info_label.configure(text=
                    f"User ID: {user_data.get('user_id', 'N/A')}\n" # Displays user ID
                    f"Username: {user_data.get('username', 'N/A')}\n" # Displays username
                    f"Email: {user_data.get('contact_info', {}).get('email', 'N/A')}\n" # Displays email from contact info
                    f"Phone: {user_data.get('contact_info', {}).get('phone', 'N/A')}\n" # Displays phone from contact info
                    f"Registration Date: {user_data.get('registration_date', 'N/A')}" # Displays registration date
                )

                # Populate Settings fields
                self.settings_widgets["username_entry"].delete(0, customtkinter.END) # Clears existing username entry
                self.settings_widgets["username_entry"].insert(0, user_data.get('username', '')) # Inserts current username

                self.settings_widgets["email_entry"].delete(0, customtkinter.END) # Clears existing email entry
                self.settings_widgets["email_entry"].insert(0, user_data.get('contact_info', {}).get('email', '')) # Inserts current email

                self.settings_widgets["phone_entry"].delete(0, customtkinter.END) # Clears existing phone entry
                self.settings_widgets["phone_entry"].insert(0, user_data.get('contact_info', {}).get('phone', '')) # Inserts current phone

                # Clear password fields
                self.settings_widgets["new_password_entry"].delete(0, customtkinter.END) # Clears new password field
                self.settings_widgets["confirm_new_password_entry"].delete(0, customtkinter.END) # Clears confirm password field
            else:
                messagebox.showerror("Error", "Could not load user data.") # Shows error if user data cannot be loaded
                logger.error(f"Failed to load user data for user ID: {user_id}") # Logs the error


    def load_pet_data(self, owner_id):
        """
        Loads and displays the current user's registered pets in the Dashboard and Manage My Pets tabs.
        """
        if owner_id:
            pets = self.pet_data_manager.get_pets_by_owner(owner_id) # Fetches pets owned by the current user
            
            # Clear existing pet displays
            for widget in self.dashboard_pets_scroll_frame.winfo_children(): # Removes all widgets from dashboard scroll frame
                widget.destroy()
            for widget in self.my_pets_scroll_frame.winfo_children(): # Removes all widgets from manage pets scroll frame
                widget.destroy()

            if pets:
                self.pet_summary_label.configure(text=f"You have {len(pets)} pets registered.") # Updates pet summary label on dashboard
                
                dashboard_row = 0
                manage_pets_row = 0
                for pet_id, pet_data in pets.items(): # Iterates through each pet
                    # Display in Dashboard
                    pet_frame_dashboard = self._create_pet_display_frame(self.dashboard_pets_scroll_frame, pet_data, is_dashboard=True) # Creates pet display frame for dashboard
                    pet_frame_dashboard.grid(row=dashboard_row, column=0, padx=5, pady=5, sticky="ew") # Places pet frame in dashboard
                    dashboard_row += 1

                    # Display in Manage My Pets
                    pet_frame_manage = self._create_pet_display_frame(self.my_pets_scroll_frame, pet_data, is_dashboard=False) # Creates pet display frame for manage pets
                    pet_frame_manage.grid(row=manage_pets_row, column=0, padx=5, pady=5, sticky="ew") # Places pet frame in manage pets
                    manage_pets_row += 1
            else:
                self.pet_summary_label.configure(text="You have no pets registered yet.") # Updates pet summary if no pets are registered
                customtkinter.CTkLabel(self.dashboard_pets_scroll_frame, text="No registered pets to display.").grid(row=0, column=0, padx=10, pady=10) # Message for no pets
                customtkinter.CTkLabel(self.my_pets_scroll_frame, text="No registered pets to display. Add one above!").grid(row=0, column=0, padx=10, pady=10) # Message for no pets

    def _create_pet_display_frame(self, parent_frame, pet_data, is_dashboard=False):
        """
        Helper function to create a frame displaying pet details.
        Reused for both Dashboard and Manage My Pets tabs.
        """
        pet_frame = customtkinter.CTkFrame(parent_frame, fg_color="transparent") # Creates a transparent frame for pet details
        pet_frame.grid_columnconfigure(1, weight=1) # Makes the second column expandable for text details

        # Load and display pet image if available
        if pet_data.get('image_path') and os.path.exists(pet_data['image_path']): # Checks if image path exists
            try:
                # Open image
                img = Image.open(pet_data['image_path'])
                # Resize image while maintaining aspect ratio
                img.thumbnail((70, 70)) # Resizes image to fit
                pet_image = ImageTk.PhotoImage(img) # Converts image to PhotoImage for CustomTkinter
                
                # Store reference to prevent garbage collection
                pet_frame.image = pet_image # Stores image reference
                
                image_label = customtkinter.CTkLabel(pet_frame, image=pet_image, text="") # Creates label for image
                image_label.grid(row=0, column=0, rowspan=5, padx=10, pady=5, sticky="n") # Places image label
            except Exception as e:
                logger.error(f"Error loading image {pet_data['image_path']}: {e}") # Logs error if image fails to load
                # Fallback if image loading fails
                image_label = customtkinter.CTkLabel(pet_frame, text="No Image", width=70, height=70, fg_color="gray") # Placeholder if image fails
                image_label.grid(row=0, column=0, rowspan=5, padx=10, pady=5, sticky="n")
        else:
            image_label = customtkinter.CTkLabel(pet_frame, text="No Image", width=70, height=70, fg_color="gray") # Placeholder if no image path
            image_label.grid(row=0, column=0, rowspan=5, padx=10, pady=5, sticky="n")

        # Display pet details
        customtkinter.CTkLabel(pet_frame, text=f"Name: {pet_data.get('pet_name', 'N/A')}", font=customtkinter.CTkFont(weight="bold")).grid(row=0, column=1, sticky="w") # Pet name
        customtkinter.CTkLabel(pet_frame, text=f"Species: {pet_data.get('species', 'N/A')}").grid(row=1, column=1, sticky="w") # Species
        customtkinter.CTkLabel(pet_frame, text=f"Breed: {pet_data.get('breed', 'N/A')}").grid(row=2, column=1, sticky="w") # Breed
        customtkinter.CTkLabel(pet_frame, text=f"Age: {pet_data.get('age', 'N/A')}").grid(row=3, column=1, sticky="w") # Age
        customtkinter.CTkLabel(pet_frame, text=f"Color: {pet_data.get('color', 'N/A')}").grid(row=4, column=1, sticky="w") # Color
        customtkinter.CTkLabel(pet_frame, text=f"Status: {pet_data.get('status', 'N/A').replace('_', ' ').title()}").grid(row=5, column=1, sticky="w") # Status, formatted for display

        # Add buttons only if not in dashboard view
        if not is_dashboard:
            button_frame = customtkinter.CTkFrame(pet_frame, fg_color="transparent") # Frame to hold action buttons
            button_frame.grid(row=0, column=2, rowspan=6, padx=10, sticky="e") # Places button frame
            button_frame.grid_rowconfigure((0,1,2,3), weight=1) # Makes rows expandable for buttons

            # Update Button
            update_button = customtkinter.CTkButton(button_frame, text="Update", command=lambda: self._open_update_pet_dialog(pet_data['pet_id'])) # Update button
            update_button.grid(row=0, column=0, pady=5, sticky="ew") # Places update button
            
            # Report Lost Button (visible only if pet is 'registered')
            if pet_data.get('status') == 'registered': # Only show if pet is not already lost
                lost_button = customtkinter.CTkButton(button_frame, text="Report Lost", command=lambda: self._report_lost_pet(pet_data['pet_id'])) # Report lost button
                lost_button.grid(row=1, column=0, pady=5, sticky="ew") # Places report lost button
            
            # Mark Found Button (visible only if pet is 'lost')
            if pet_data.get('status') == 'lost': # Only show if pet is lost
                found_button = customtkinter.CTkButton(button_frame, text="Mark Found", command=lambda: self._mark_pet_found(pet_data['pet_id'])) # Mark found button
                found_button.grid(row=2, column=0, pady=5, sticky="ew") # Places mark found button

            # Delete Button
            delete_button = customtkinter.CTkButton(button_frame, text="Delete", fg_color="red", hover_color="darkred", command=lambda: self._delete_pet(pet_data['pet_id'])) # Delete button
            delete_button.grid(row=3, column=0, pady=5, sticky="ew") # Places delete button

        return pet_frame # Returns the created pet display frame


    def load_stray_data(self):
        """
        Loads and displays all reported stray pets in the Stray Reporting tab.
        """
        strays = self.pet_data_manager.get_all_strays() # Fetches all stray pet reports

        # Clear existing stray displays
        for widget in self.stray_pets_scroll_frame.winfo_children(): # Removes all widgets from stray pets scroll frame
            widget.destroy()
        
        # Update summary on dashboard (also counts captured strays)
        num_strays_active = sum(1 for stray in strays.values() if stray.get('status') == 'stray') # Counts active strays
        num_strays_captured = sum(1 for stray in strays.values() if stray.get('status') == 'found_captured') # Counts captured strays
        self.lost_stray_summary_label.configure(text=f"There are currently {num_strays_active} active stray reports and {num_strays_captured} strays have been found/captured.") # Updates summary label

        if strays:
            row = 0
            for stray_id, stray_data in strays.items(): # Iterates through each stray report
                stray_frame = self._create_stray_display_frame(self.stray_pets_scroll_frame, stray_data) # Creates stray display frame
                stray_frame.grid(row=row, column=0, padx=5, pady=5, sticky="ew") # Places stray frame
                row += 1
        else:
            customtkinter.CTkLabel(self.stray_pets_scroll_frame, text="No stray pet reports to display.").grid(row=0, column=0, padx=10, pady=10) # Message if no stray reports

    def _create_stray_display_frame(self, parent_frame, stray_data):
        """
        Helper function to create a frame displaying stray pet details.
        """
        stray_frame = customtkinter.CTkFrame(parent_frame, fg_color="transparent") # Creates a transparent frame for stray details
        stray_frame.grid_columnconfigure(1, weight=1) # Makes the second column expandable for text details

        # Display stray details
        customtkinter.CTkLabel(stray_frame, text=f"ID: {stray_data.get('stray_id', 'N/A')}", font=customtkinter.CTkFont(weight="bold")).grid(row=0, column=1, sticky="w") # Stray ID
        customtkinter.CTkLabel(stray_frame, text=f"Species: {stray_data.get('species', 'N/A')}").grid(row=1, column=1, sticky="w") # Species
        customtkinter.CTkLabel(stray_frame, text=f"Location: {stray_data.get('location', 'N/A')}").grid(row=2, column=1, sticky="w") # Location
        customtkinter.CTkLabel(stray_frame, text=f"Breed: {stray_data.get('breed', 'N/A')}").grid(row=3, column=1, sticky="w") # Breed
        customtkinter.CTkLabel(stray_frame, text=f"Color: {stray_data.get('color', 'N/A')}").grid(row=4, column=1, sticky="w") # Color
        customtkinter.CTkLabel(stray_frame, text=f"Description: {stray_data.get('description', 'N/A')}").grid(row=5, column=1, sticky="w") # Description
        customtkinter.CTkLabel(stray_frame, text=f"Reported Date: {stray_data.get('reported_date', 'N/A')}").grid(row=6, column=1, sticky="w") # Reported date
        customtkinter.CTkLabel(stray_frame, text=f"Status: {stray_data.get('status', 'N/A').replace('_', ' ').title()}", font=customtkinter.CTkFont(weight="bold")).grid(row=7, column=1, sticky="w") # Status, formatted

        # Display contact info if available
        contact_info = stray_data.get('contact_info', {}) # Gets contact info dictionary
        if contact_info:
            contact_text = "Contact: " # Prefix for contact info
            if contact_info.get('email'):
                contact_text += f"Email: {contact_info['email']} " # Adds email if present
            if contact_info.get('phone'):
                contact_text += f"Phone: {contact_info['phone']}" # Adds phone if present
            customtkinter.CTkLabel(stray_frame, text=contact_text.strip()).grid(row=8, column=1, sticky="w") # Places contact info label

        # Mark Found/Captured button for active strays
        if stray_data.get('status') == 'stray': # Only show if stray is active
            mark_found_button = customtkinter.CTkButton(stray_frame, text="Mark Found/Captured", command=lambda: self._mark_stray_found_captured(stray_data['stray_id'])) # Mark found button
            mark_found_button.grid(row=0, column=2, rowspan=9, padx=10, sticky="e") # Places button
        
        return stray_frame # Returns the created stray display frame


    def load_reports_data(self):
        """
        Loads and displays various application reports in the Reports tab.
        """
        # Get total users
        total_users = self.user_manager.get_total_users() # Fetches total number of users
        self.total_users_label.configure(text=f"Total Registered Users: {total_users}") # Updates total users label

        # Get total registered pets (all pets, including lost ones)
        all_registered_pets = self.report_manager.get_all_registered_pets_data() # Fetches all registered pets
        self.total_pets_label.configure(text=f"Total Registered Pets: {len(all_registered_pets)}") # Updates total pets label

        # Get lost pets
        lost_pets = self.report_manager.get_all_lost_pets_data() # Fetches all lost pets
        self.lost_pets_label.configure(text=f"Number of Lost Pets Reported: {len(lost_pets)}") # Updates lost pets label

        # Get stray pets (active and captured)
        stray_reports = self.report_manager.get_stray_report_data() # Fetches all stray reports
        num_active_strays = sum(1 for stray in stray_reports.values() if stray.get('status') == 'stray') # Counts active strays
        self.stray_pets_report_label.configure(text=f"Total Stray Pet Reports: {len(stray_reports)} ({num_active_strays} active)") # Updates stray reports label

        # Clear existing lost pet displays
        for widget in self.lost_pets_scroll_frame.winfo_children(): # Removes all widgets from lost pets scroll frame
            widget.destroy()

        if lost_pets:
            row = 0
            for pet_id, pet_data in lost_pets.items(): # Iterates through each lost pet
                lost_pet_frame = self._create_lost_pet_display_frame(self.lost_pets_scroll_frame, pet_data) # Creates lost pet display frame
                lost_pet_frame.grid(row=row, column=0, padx=5, pady=5, sticky="ew") # Places lost pet frame
                row += 1
        else:
            customtkinter.CTkLabel(self.lost_pets_scroll_frame, text="No lost pets reported.").grid(row=0, column=0, padx=10, pady=10) # Message if no lost pets


    def _create_lost_pet_display_frame(self, parent_frame, pet_data):
        """
        Helper function to create a frame displaying lost pet details for the reports tab.
        """
        lost_pet_frame = customtkinter.CTkFrame(parent_frame, fg_color="transparent") # Creates a transparent frame
        lost_pet_frame.grid_columnconfigure(1, weight=1) # Makes the second column expandable for text details

        # Load and display pet image if available
        if pet_data.get('image_path') and os.path.exists(pet_data['image_path']): # Checks if image path exists
            try:
                img = Image.open(pet_data['image_path']) # Opens image
                img.thumbnail((70, 70)) # Resizes image
                pet_image = ImageTk.PhotoImage(img) # Converts to PhotoImage
                lost_pet_frame.image = pet_image # Stores image reference
                image_label = customtkinter.CTkLabel(lost_pet_frame, image=pet_image, text="") # Creates label for image
                image_label.grid(row=0, column=0, rowspan=6, padx=10, pady=5, sticky="n") # Places image label
            except Exception as e:
                logger.error(f"Error loading image {pet_data['image_path']}: {e}") # Logs error
                image_label = customtkinter.CTkLabel(lost_pet_frame, text="No Image", width=70, height=70, fg_color="gray") # Placeholder
                image_label.grid(row=0, column=0, rowspan=6, padx=10, pady=5, sticky="n")
        else:
            image_label = customtkinter.CTkLabel(lost_pet_frame, text="No Image", width=70, height=70, fg_color="gray") # Placeholder
            image_label.grid(row=0, column=0, rowspan=6, padx=10, pady=5, sticky="n")

        # Display lost pet details
        customtkinter.CTkLabel(lost_pet_frame, text=f"Name: {pet_data.get('pet_name', 'N/A')}", font=customtkinter.CTkFont(weight="bold")).grid(row=0, column=1, sticky="w") # Pet name
        customtkinter.CTkLabel(lost_pet_frame, text=f"Species: {pet_data.get('species', 'N/A')}").grid(row=1, column=1, sticky="w") # Species
        customtkinter.CTkLabel(lost_pet_frame, text=f"Breed: {pet_data.get('breed', 'N/A')}").grid(row=2, column=1, sticky="w") # Breed
        customtkinter.CTkLabel(lost_pet_frame, text=f"Color: {pet_data.get('color', 'N/A')}").grid(row=3, column=1, sticky="w") # Color
        customtkinter.CTkLabel(lost_pet_frame, text=f"Owner ID: {pet_data.get('owner_id', 'N/A')}").grid(row=4, column=1, sticky="w") # Owner ID
        
        lost_details = pet_data.get('lost_details', {}) # Gets lost details
        customtkinter.CTkLabel(lost_pet_frame, text=f"Last Seen: {lost_details.get('location', 'N/A')} on {lost_details.get('timestamp', 'N/A')}").grid(row=5, column=1, sticky="w") # Lost location and timestamp

        return lost_pet_frame # Returns the created lost pet display frame


    def _add_pet(self):
        """
        Handles adding a new pet for the current user.
        Retrieves data from the pet registration form and calls PetDataManager.
        """
        pet_name = self.pet_form_widgets["pet_name_entry"].get().strip() # Gets pet name
        species = self.pet_form_widgets["species_optionmenu"].get().strip() # Gets species
        breed = self.pet_form_widgets["breed_entry"].get().strip() # Gets breed
        age_str = self.pet_form_widgets["age_entry"].get().strip() # Gets age as string
        color = self.pet_form_widgets["color_entry"].get().strip() # Gets color
        image_path = self.pet_form_widgets["image_path_entry"].get().strip() # Gets image path

        # Basic validation
        if not pet_name or not species or not color: # Checks for mandatory fields
            messagebox.showerror("Input Error", "Pet Name, Species, and Color cannot be empty.") # Shows error if mandatory fields are empty
            return

        age = None
        if age_str:
            try:
                age = float(age_str) # Converts age to float
                if age < 0: # Validates age is not negative
                    messagebox.showerror("Input Error", "Age cannot be negative.")
                    return
            except ValueError:
                messagebox.showerror("Input Error", "Age must be a number (e.g., 2 or 0.5).") # Error if age is not a valid number
                return

        # Call PetDataManager to add the pet
        if self.current_user_id: # Ensures a user is logged in
            pet_id = self.pet_data_manager.add_pet(
                owner_id=self.current_user_id,
                pet_name=pet_name,
                species=species,
                breed=breed if breed else None, # Stores empty string as None
                age=age,
                color=color,
                image_path=image_path if image_path else None # Stores empty string as None
            )
            if pet_id:
                messagebox.showinfo("Success", f"Pet '{pet_name}' added successfully with ID: {pet_id}!") # Success message
                self.clear_pet_form() # Clears the form after successful addition
                self.load_pet_data(self.current_user_id) # Reloads pet data to update lists
            else:
                messagebox.showerror("Error", "Failed to add pet.") # Error message if pet addition fails
                logger.error(f"Failed to add pet for user {self.current_user_id}") # Logs the error
        else:
            messagebox.showerror("Error", "No user logged in to add a pet.") # Error if no user is logged in


    def clear_pet_form(self):
        """Clears all input fields in the Add Pet form."""
        self.pet_form_widgets["pet_name_entry"].delete(0, customtkinter.END) # Clears pet name entry
        self.pet_form_widgets["breed_entry"].delete(0, customtkinter.END) # Clears breed entry
        self.pet_form_widgets["age_entry"].delete(0, customtkinter.END) # Clears age entry
        self.pet_form_widgets["color_entry"].delete(0, customtkinter.END) # Clears color entry
        self.pet_form_widgets["image_path_entry"].delete(0, customtkinter.END) # Clears image path entry
        self.pet_form_widgets["species_optionmenu"].set("Dog") # Resets species to default


    def _open_update_pet_dialog(self, pet_id):
        """
        Opens the UpdatePetDialog for a selected pet.
        """
        pet_details = self.pet_data_manager.get_pet(pet_id) # Fetches details of the pet to be updated
        if pet_details:
            dialog = UpdatePetDialog(self.master, pet_details) # Creates an instance of the update dialog
            self.master.wait_window(dialog) # Waits for the dialog to close

            if dialog.updated_data: # Checks if the dialog returned updated data
                if self.pet_data_manager.update_pet(pet_id, dialog.updated_data): # Calls PetDataManager to update
                    messagebox.showinfo("Success", "Pet details updated successfully!") # Success message
                    self.load_pet_data(self.current_user_id) # Reloads pet data to reflect changes
                else:
                    messagebox.showerror("Error", "Failed to update pet details.") # Error message
                    logger.error(f"Failed to update pet {pet_id} with data {dialog.updated_data}") # Logs the error
        else:
            messagebox.showerror("Error", "Pet not found for update.") # Error if pet details can't be fetched


    def _delete_pet(self, pet_id):
        """
        Handles deleting a selected pet.
        Confirms with the user before proceeding.
        """
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this pet? This action cannot be undone."): # Asks for user confirmation
            if self.pet_data_manager.delete_pet(pet_id): # Calls PetDataManager to delete
                messagebox.showinfo("Success", "Pet deleted successfully!") # Success message
                self.load_pet_data(self.current_user_id) # Reloads pet data to update lists
            else:
                messagebox.showerror("Error", "Failed to delete pet.") # Error message
                logger.error(f"Failed to delete pet {pet_id}") # Logs the error


    def _report_lost_pet(self, pet_id):
        """
        Handles reporting a pet as lost.
        Prompts for last seen location.
        """
        last_seen_location = customtkinter.CTkInputDialog(text="Enter last seen location:", title="Report Lost Pet").get_input() # Prompts user for location
        if last_seen_location:
            if self.report_manager.report_lost_pet(pet_id, last_seen_location): # Calls ReportManager to mark as lost
                messagebox.showinfo("Success", f"Pet {pet_id} reported as lost at {last_seen_location}.") # Success message
                self.load_pet_data(self.current_user_id) # Reloads pet data to update status
            else:
                messagebox.showerror("Error", "Failed to report pet as lost.") # Error message
                logger.error(f"Failed to report pet {pet_id} as lost.") # Logs the error
        elif last_seen_location == "": # Handles empty input
            messagebox.showwarning("Input Required", "Last seen location cannot be empty.") # Warning for empty input


    def _mark_pet_found(self, pet_id):
        """
        Handles marking a lost pet as found.
        """
        if messagebox.askyesno("Confirm Found", "Are you sure you want to mark this pet as found?"): # Confirms with user
            if self.report_manager.mark_pet_found(pet_id): # Calls ReportManager to mark as found
                messagebox.showinfo("Success", f"Pet {pet_id} marked as found.") # Success message
                self.load_pet_data(self.current_user_id) # Reloads pet data to update status
            else:
                messagebox.showerror("Error", "Failed to mark pet as found.") # Error message
                logger.error(f"Failed to mark pet {pet_id} as found.") # Logs the error


    def _report_stray_pet(self):
        """
        Handles reporting a new stray pet.
        Retrieves data from the stray reporting form and calls PetDataManager.
        """
        species = self.stray_form_widgets["stray_species_optionmenu"].get().strip() # Gets species
        location = self.stray_form_widgets["stray_location_entry"].get().strip() # Gets location
        breed = self.stray_form_widgets["stray_breed_entry"].get().strip() # Gets breed
        color = self.stray_form_widgets["stray_color_entry"].get().strip() # Gets color
        description = self.stray_form_widgets["stray_description_entry"].get("1.0", customtkinter.END).strip() # Gets description from textbox
        contact_email = self.stray_form_widgets["stray_email_entry"].get().strip() # Gets contact email
        contact_phone = self.stray_form_widgets["stray_phone_entry"].get().strip() # Gets contact phone

        # Basic validation
        if not species or not location or not color: # Checks for mandatory fields
            messagebox.showerror("Input Error", "Species, Location, and Color cannot be empty for a stray report.") # Error for empty mandatory fields
            return

        contact_info = {} # Dictionary to store contact info
        if contact_email:
            contact_info['email'] = contact_email # Adds email if provided
        if contact_phone:
            contact_info['phone'] = contact_phone # Adds phone if provided

        # Calls PetDataManager to add stray pet report
        stray_id = self.pet_data_manager.add_stray_pet_report(
            reporter_id=self.current_user_id, # Reporter ID (can be None if user not logged in, but here we assume logged in)
            species=species,
            location=location,
            breed=breed if breed else None,
            color=color,
            description=description if description else None,
            contact_info=contact_info if contact_info else None
        )
        if stray_id:
            messagebox.showinfo("Success", f"Stray pet reported successfully with ID: {stray_id}!") # Success message
            self.clear_stray_form() # Clears the form
            self.load_stray_data() # Reloads stray data to update list
        else:
            messagebox.showerror("Error", "Failed to report stray pet.") # Error message
            logger.error("Failed to report stray pet.") # Logs the error


    def clear_stray_form(self):
        """Clears all input fields in the Report Stray Pet form."""
        self.stray_form_widgets["stray_location_entry"].delete(0, customtkinter.END) # Clears location entry
        self.stray_form_widgets["stray_breed_entry"].delete(0, customtkinter.END) # Clears breed entry
        self.stray_form_widgets["stray_color_entry"].delete(0, customtkinter.END) # Clears color entry
        self.stray_form_widgets["stray_description_entry"].delete("1.0", customtkinter.END) # Clears description textbox
        self.stray_form_widgets["stray_email_entry"].delete(0, customtkinter.END) # Clears email entry
        self.stray_form_widgets["stray_phone_entry"].delete(0, customtkinter.END) # Clears phone entry
        self.stray_form_widgets["stray_species_optionmenu"].set("Dog") # Resets species to default


    def _mark_stray_found_captured(self, stray_id):
        """
        Handles marking a reported stray pet as found/captured.
        """
        if messagebox.askyesno("Confirm Action", "Are you sure you want to mark this stray pet as found/captured?"): # Confirms with user
            if self.pet_data_manager.mark_stray_found_captured(stray_id): # Calls PetDataManager to mark as found
                messagebox.showinfo("Success", f"Stray pet {stray_id} marked as found/captured.") # Success message
                self.load_stray_data() # Reloads stray data to update list
                self.load_reports_data() # Reloads reports data to update counts
            else:
                messagebox.showerror("Error", "Failed to mark stray pet as found/captured.") # Error message
                logger.error(f"Failed to mark stray pet {stray_id} as found/captured.") # Logs the error


    def _update_profile(self):
        """
        Handles updating the current user's profile information.
        """
        new_username = self.settings_widgets["username_entry"].get().strip() # Gets new username
        new_email = self.settings_widgets["email_entry"].get().strip() # Gets new email
        new_phone = self.settings_widgets["phone_entry"].get().strip() # Gets new phone
        new_password = self.settings_widgets["new_password_entry"].get().strip() # Gets new password
        confirm_new_password = self.settings_widgets["confirm_new_password_entry"].get().strip() # Gets confirmed new password

        updates = {} # Dictionary to store updates
        user_data = self.user_manager.get_user(self.current_user_id) # Fetches current user data

        if not user_data: # Error if user data not found
            messagebox.showerror("Error", "Could not retrieve current user data for update.")
            logger.error(f"Attempted to update profile for non-existent user ID: {self.current_user_id}")
            return

        current_username = user_data.get('username') # Current username

        # Username validation
        if new_username and new_username != current_username: # Checks if username is changed and not empty
            updates['username'] = new_username # Adds new username to updates
            if self.user_manager.get_user_by_username(new_username): # Checks if new username is already taken
                messagebox.showerror("Update Error", f"Username '{new_username}' is already taken.")
                return
        elif not new_username: # If username field is empty
             messagebox.showerror("Input Error", "Username cannot be empty.")
             return

        # Password validation
        if new_password: # If a new password is provided
            if new_password != confirm_new_password: # Checks if passwords match
                messagebox.showerror("Update Error", "New passwords do not match.")
                return
            updates['password'] = new_password # Adds new password to updates (UserManager will hash it)

        # Contact info
        new_contact_info = {} # Dictionary for new contact info
        if new_email:
            new_contact_info['email'] = new_email # Adds email if provided
        if new_phone:
            new_contact_info['phone'] = new_phone # Adds phone if provided
        
        updates['contact_info'] = new_contact_info # Adds contact info to updates

        # Call UserManager to update
        if self.user_manager.update_user(self.current_user_id, updates): # Calls UserManager to update user
            messagebox.showinfo("Success", "Profile updated successfully!") # Success message
            self.load_user_data(self.current_user_id) # Refresh dashboard user info
        else:
            messagebox.showerror("Error", "Failed to update profile.") # Error message
            logger.error(f"Failed to update profile for user {self.current_user_id}") # Logs the error


    def _delete_account(self):
        """
        Handles the deletion of the current user's account.
        Requires strong confirmation due to irreversible nature.
        """
        if messagebox.askyesno("Confirm Account Deletion", "Are you absolutely sure you want to delete your account? This action cannot be undone and will delete all your registered pets!", icon='warning'): # Asks for strong confirmation
            # Potentially add a re-authentication step here for security
            if self.user_manager.delete_user(self.current_user_id): # Calls UserManager to delete user
                messagebox.showinfo("Account Deleted", "Your account has been successfully deleted.") # Success message
                self.switch_to_login_callback() # Go back to login screen
            else:
                messagebox.showerror("Error", "Failed to delete account.") # Error message
                logger.error(f"Failed to delete account for user {self.current_user_id}") # Logs the error