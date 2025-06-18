import customtkinter
import logging
import datetime
import tkinter.messagebox as messagebox
from PIL import Image
import threading # Import the threading module

logger = logging.getLogger(__name__)

class DashboardFrame(customtkinter.CTkFrame):
    def __init__(self, master, user_manager, pet_data_manager, show_main_menu_callback, report_manager, search_manager):
        super().__init__(master)
        self.user_manager = user_manager
        self.pet_data_manager = pet_data_manager
        self.show_main_menu_callback = show_main_menu_callback
        self.report_manager = report_manager
        self.search_manager = search_manager
        self.current_user_id = None

        # Configure grid for the Dashboard frame
        self.grid_columnconfigure(1, weight=1) # Content column
        self.grid_rowconfigure(0, weight=1) # Main content row

        # ------------------------------------------------------------------------- Sidebar Navigation ---------------------------------------------------------------------
        self.sidebar_frame = customtkinter.CTkFrame(self, width=150, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1) # Push logout to bottom

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="PetDex", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        # Navigation Buttons
        self.home_button = customtkinter.CTkButton(self.sidebar_frame, text="Home", command=self.show_home_frame)
        self.home_button.grid(row=1, column=0, padx=20, pady=10)

        self.my_pets_button = customtkinter.CTkButton(self.sidebar_frame, text="My Registered Pets", command=self.show_my_pets_frame)
        self.my_pets_button.grid(row=2, column=0, padx=20, pady=10)

        self.report_pet_button = customtkinter.CTkButton(self.sidebar_frame, text="Report Pet", command=self.show_report_pet_frame)
        self.report_pet_button.grid(row=3, column=0, padx=20, pady=10)

        self.view_strays_button = customtkinter.CTkButton(self.sidebar_frame, text="View All Strays", command=self.show_view_strays_frame)
        self.view_strays_button.grid(row=4, column=0, padx=20, pady=10)

        self.search_button = customtkinter.CTkButton(self.sidebar_frame, text="Search Animals", command=self.show_search_frame)
        self.search_button.grid(row=5, column=0, padx=20, pady=10)

        self.logout_button = customtkinter.CTkButton(self.sidebar_frame, text="Logout", command=self._logout)
        self.logout_button.grid(row=6, column=0, padx=20, pady=10, sticky="s")

        # ------------------------------------------------------------------------- Content Frames ---------------------------------------------------------------------
        self.home_frame = self._create_home_frame()
        self.my_pets_frame = self._create_my_pets_frame()
        self.report_pet_frame = self._create_report_pet_frame()
        self.view_strays_frame = self._create_view_strays_frame()
        self.search_frame = self._create_search_frame()

        self.current_content_frame = None
        self.show_home_frame()

    def set_user_id(self, user_id):
        self.current_user_id = user_id
        self.refresh_my_pets_display()
        self.refresh_strays_display()

    def _logout(self):
        self.current_user_id = None
        self.show_main_menu_callback()
        logger.info("User logged out.")

    def _show_content_frame(self, frame_to_show):
        if self.current_content_frame:
            self.current_content_frame.grid_forget()
        self.current_content_frame = frame_to_show
        self.current_content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    # --- Frame Display Methods ---
    def show_home_frame(self):
        self._show_content_frame(self.home_frame)

    def show_my_pets_frame(self):
        self.refresh_my_pets_display()
        self._show_content_frame(self.my_pets_frame)

    def show_report_pet_frame(self):
        self._show_content_frame(self.report_pet_frame)

    def show_view_strays_frame(self):
        self.refresh_strays_display()
        self._show_content_frame(self.view_strays_frame)

    def show_search_frame(self):
        self._show_content_frame(self.search_frame)

    # --- Frame Creation Methods ---
    def _create_home_frame(self):
        frame = customtkinter.CTkFrame(self, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        label = customtkinter.CTkLabel(frame, text="Welcome to your Dashboard!", font=customtkinter.CTkFont(size=28, weight="bold"))
        label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        return frame

    def _create_my_pets_frame(self):
        frame = customtkinter.CTkFrame(self, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        title_label = customtkinter.CTkLabel(frame, text="My Registered Pets", font=customtkinter.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.my_pets_scroll_frame = customtkinter.CTkScrollableFrame(frame, fg_color="transparent")
        self.my_pets_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.my_pets_scroll_frame.grid_columnconfigure(0, weight=1)
        return frame

    def refresh_my_pets_display(self):
        # Clear existing widgets
        for widget in self.my_pets_scroll_frame.winfo_children():
            widget.destroy()

        user_pets = self.pet_data_manager.get_pets_by_owner(self.current_user_id)
        if user_pets:
            row_idx = 0
            for pet_id, details in user_pets.items():
                status_text = f"Status: {details.get('status', 'N/A').capitalize()}"
                if details.get('status') == 'lost' and 'lost_details' in details:
                    lost_loc = details['lost_details'].get('location', 'N/A')
                    lost_time = details['lost_details'].get('timestamp', 'N/A')
                    status_text += f" (Last seen: {lost_loc} on {lost_time})"

                pet_info_text = (
                    f"ID: {pet_id}\n"
                    f"Name: {details.get('pet_name', 'N/A')}\n"
                    f"Species: {details.get('species', 'N/A')}\n"
                    f"Breed: {details.get('breed', 'N/A')}\n"
                    f"Age: {details.get('age', 'N/A')}\n"
                    f"Color: {details.get('color', 'N/A')}\n"
                    f"{status_text}\n"
                )
                customtkinter.CTkLabel(self.my_pets_scroll_frame, text=pet_info_text, justify="left", wraplength=400).grid(row=row_idx, column=0, padx=5, pady=5, sticky="ew")

                # Buttons for actions
                buttons_frame = customtkinter.CTkFrame(self.my_pets_scroll_frame, fg_color="transparent")
                buttons_frame.grid(row=row_idx, column=1, padx=5, pady=5, sticky="e")

                # Update Pet Button (if you have an update function)
                update_button = customtkinter.CTkButton(buttons_frame, text="Update", command=lambda p_id=pet_id: self._show_update_pet_dialog(p_id))
                update_button.grid(row=0, column=0, padx=5)

                # Delete Pet Button
                delete_button = customtkinter.CTkButton(buttons_frame, text="Delete", command=lambda p_id=pet_id: self._delete_pet_confirmation(p_id))
                delete_button.grid(row=0, column=1, padx=5)

                # Report Lost/Found Button
                if details.get('status') == 'owned':
                    report_lost_button = customtkinter.CTkButton(buttons_frame, text="Report Lost", command=lambda p_id=pet_id: self._show_report_lost_pet_dialog(p_id))
                    report_lost_button.grid(row=0, column=2, padx=5)
                elif details.get('status') == 'lost':
                    report_found_button = customtkinter.CTkButton(buttons_frame, text="Mark Found", command=lambda p_id=pet_id: self._report_pet_found(p_id))
                    report_found_button.grid(row=0, column=2, padx=5)


                customtkinter.CTkFrame(self.my_pets_scroll_frame, height=1, fg_color="gray").grid(row=row_idx+1, column=0, columnspan=2, sticky="ew", pady=5)
                row_idx += 2
        else:
            customtkinter.CTkLabel(self.my_pets_scroll_frame, text="No registered pets found for this user.").grid(row=0, column=0, padx=20, pady=20)


    def _create_report_pet_frame(self):
        frame = customtkinter.CTkFrame(self, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=0) # Title
        frame.grid_rowconfigure(1, weight=1) # Tabview for forms

        title_label = customtkinter.CTkLabel(frame, text="Report Pet Information", font=customtkinter.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        # Tabview for different report types
        self.report_tabview = customtkinter.CTkTabview(frame)
        self.report_tabview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.report_tabview.add("Register New Pet")
        self.report_tabview.add("Report Stray Animal")

        # --- Register New Pet Tab ---
        register_pet_frame = self.report_tabview.tab("Register New Pet")
        register_pet_frame.grid_columnconfigure(0, weight=1)
        register_pet_frame.grid_columnconfigure(1, weight=1)
        register_pet_frame.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=0) # Make rows auto-size
        register_pet_frame.grid_rowconfigure(8, weight=1) # Spacer row

        # Pet Name
        customtkinter.CTkLabel(register_pet_frame, text="Pet Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.reg_pet_name_entry = customtkinter.CTkEntry(register_pet_frame)
        self.reg_pet_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Species
        customtkinter.CTkLabel(register_pet_frame, text="Species (e.g., Dog, Cat):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.reg_species_entry = customtkinter.CTkEntry(register_pet_frame)
        self.reg_species_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Breed
        customtkinter.CTkLabel(register_pet_frame, text="Breed (Optional):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.reg_breed_entry = customtkinter.CTkEntry(register_pet_frame)
        self.reg_breed_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Age
        customtkinter.CTkLabel(register_pet_frame, text="Age (Optional):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.reg_age_entry = customtkinter.CTkEntry(register_pet_frame)
        self.reg_age_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Color
        customtkinter.CTkLabel(register_pet_frame, text="Color (Optional):").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.reg_color_entry = customtkinter.CTkEntry(register_pet_frame)
        self.reg_color_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        # Image Path (Optional)
        customtkinter.CTkLabel(register_pet_frame, text="Image Path (Optional):").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.reg_image_path_entry = customtkinter.CTkEntry(register_pet_frame)
        self.reg_image_path_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        # Register Button
        register_button = customtkinter.CTkButton(register_pet_frame, text="Register Pet", command=self._register_pet)
        register_button.grid(row=6, column=0, columnspan=2, padx=10, pady=20)

        self.reg_pet_message_label = customtkinter.CTkLabel(register_pet_frame, text="", text_color="red")
        self.reg_pet_message_label.grid(row=7, column=0, columnspan=2, padx=10, pady=5)


        # --- Report Stray Animal Tab ---
        report_stray_frame = self.report_tabview.tab("Report Stray Animal")
        report_stray_frame.grid_columnconfigure(0, weight=1)
        report_stray_frame.grid_columnconfigure(1, weight=1)
        report_stray_frame.grid_rowconfigure((0,1,2,3,4,5,6), weight=0)
        report_stray_frame.grid_rowconfigure(7, weight=1) # Spacer

        # Reporter ID (This will be the current_user_id)
        customtkinter.CTkLabel(report_stray_frame, text="Your User ID:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.stray_reporter_id_label = customtkinter.CTkLabel(report_stray_frame, text="")
        self.stray_reporter_id_label.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Species
        customtkinter.CTkLabel(report_stray_frame, text="Species (e.g., Dog, Cat):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.stray_species_entry = customtkinter.CTkEntry(report_stray_frame)
        self.stray_species_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Breed
        customtkinter.CTkLabel(report_stray_frame, text="Breed (Optional):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.stray_breed_entry = customtkinter.CTkEntry(report_stray_frame)
        self.stray_breed_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Color
        customtkinter.CTkLabel(report_stray_frame, text="Color (Optional):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.stray_color_entry = customtkinter.CTkEntry(report_stray_frame)
        self.stray_color_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Location
        customtkinter.CTkLabel(report_stray_frame, text="Location Found:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.stray_location_entry = customtkinter.CTkEntry(report_stray_frame)
        self.stray_location_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        # Description
        customtkinter.CTkLabel(report_stray_frame, text="Description (Optional):").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.stray_description_entry = customtkinter.CTkEntry(report_stray_frame)
        self.stray_description_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        # Contact Info
        customtkinter.CTkLabel(report_stray_frame, text="Contact Info (Optional):").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.stray_contact_info_entry = customtkinter.CTkEntry(report_stray_frame)
        self.stray_contact_info_entry.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

        # Report Button
        report_stray_button = customtkinter.CTkButton(report_stray_frame, text="Report Stray Animal", command=self._report_stray_animal)
        report_stray_button.grid(row=7, column=0, columnspan=2, padx=10, pady=20)

        self.stray_message_label = customtkinter.CTkLabel(report_stray_frame, text="", text_color="red")
        self.stray_message_label.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

        return frame

    def _register_pet(self):
        owner_id = self.current_user_id
        pet_name = self.reg_pet_name_entry.get().strip()
        species = self.reg_species_entry.get().strip()
        breed = self.reg_breed_entry.get().strip() or None
        age = self.reg_age_entry.get().strip() or None
        color = self.reg_color_entry.get().strip() or None
        image_path = self.reg_image_path_entry.get().strip() or None

        if not pet_name or not species:
            self.reg_pet_message_label.configure(text="Pet Name and Species are required.", text_color="red")
            return

        if self.pet_data_manager.add_pet(owner_id, pet_name, species, breed, age, color, image_path):
            self.reg_pet_message_label.configure(text=f"Pet '{pet_name}' registered successfully!", text_color="green")
            # Clear fields
            self.reg_pet_name_entry.delete(0, customtkinter.END)
            self.reg_species_entry.delete(0, customtkinter.END)
            self.reg_breed_entry.delete(0, customtkinter.END)
            self.reg_age_entry.delete(0, customtkinter.END)
            self.reg_color_entry.delete(0, customtkinter.END)
            self.reg_image_path_entry.delete(0, customtkinter.END)
            self.refresh_my_pets_display() # Refresh 'My Registered Pets' tab
        else:
            self.reg_pet_message_label.configure(text="Failed to register pet. Please try again.", text_color="red")


    def _delete_pet_confirmation(self, pet_id):
        msg_box = messagebox.askyesno("Delete Pet", f"Are you sure you want to delete pet with ID {pet_id}?")
        if msg_box:
            if self.pet_data_manager.delete_pet(pet_id):
                messagebox.showinfo("Success", f"Pet {pet_id} deleted successfully.")
                self.refresh_my_pets_display()
            else:
                messagebox.showerror("Error", f"Failed to delete pet {pet_id}.")

    def _show_update_pet_dialog(self, pet_id):
        # Placeholder for update pet dialog logic
        messagebox.showinfo("Update Pet", f"Feature to update pet {pet_id} coming soon!")


    def _show_report_lost_pet_dialog(self, pet_id):
        pet_details = self.pet_data_manager.get_pet(pet_id)
        if not pet_details:
            messagebox.showerror("Error", "Pet not found!")
            return

        dialog = customtkinter.CTkInputDialog(text=f"Report {pet_details['pet_name']} as Lost.\nLocation last seen:", title="Report Lost Pet")

        lost_location = dialog.get_input()

        if lost_location is not None:
            if self.report_manager.report_lost_pet(pet_id, lost_location):
                messagebox.showinfo("Success", f"Pet {pet_id} reported as lost at {lost_location}.")
                self.refresh_my_pets_display()
            else:
                messagebox.showerror("Error", f"Failed to report pet {pet_id} as lost. It might already be reported.")
        else:
            logger.info("Report lost pet cancelled.")

    def _report_pet_found(self, pet_id):
        msg_box = messagebox.askyesno("Confirm Found", f"Are you sure you want to mark pet with ID {pet_id} as found?")
        if msg_box:
            if self.report_manager.report_found_pet(pet_id):
                messagebox.showinfo("Success", f"Pet {pet_id} marked as found.")
                self.refresh_my_pets_display()
            else:
                messagebox.showerror("Error", f"Failed to mark pet {pet_id} as found.")


    def _report_stray_animal_threaded(self):
        reporter_id = self.current_user_id
        species = self.stray_species_entry.get().strip()
        breed = self.stray_breed_entry.get().strip() or None
        color = self.stray_color_entry.get().strip() or None
        location = self.stray_location_entry.get().strip()
        description = self.stray_description_entry.get().strip() or None
        contact_info = self.stray_contact_info_entry.get().strip() or None

        if not species or not location:
            self.master.after(0, lambda: self.stray_message_label.configure(text="Species and Location are required.", text_color="red"))
            return

        # Perform the actual reporting in the thread
        stray_id = self.report_manager.report_stray_pet(reporter_id, species, location, breed, color, description, contact_info)

        # Update GUI on the main thread after the operation is complete
        self.master.after(0, lambda: self._handle_stray_report_result(stray_id, species, location))

    def _handle_stray_report_result(self, stray_id, species, location):
        if stray_id:
            self.stray_message_label.configure(text=f"Stray animal ({species}) reported successfully! ID: {stray_id}", text_color="green")
            # Clear fields after successful registration
            self.stray_species_entry.delete(0, customtkinter.END)
            self.stray_breed_entry.delete(0, customtkinter.END)
            self.stray_color_entry.delete(0, customtkinter.END)
            self.stray_location_entry.delete(0, customtkinter.END)
            self.stray_description_entry.delete(0, customtkinter.END)
            self.stray_contact_info_entry.delete(0, customtkinter.END)
            self.refresh_strays_display() # Refresh the 'View All Strays' tab
        else:
            self.stray_message_label.configure(text="Failed to report stray animal. Please try again.", text_color="red")


    def _report_stray_animal(self):
        """Starts the stray animal reporting in a new thread."""
        # Clear previous message
        self.stray_message_label.configure(text="Reporting stray animal...", text_color="orange")
        self.update_idletasks() # Force GUI update to show "Reporting..." message

        thread = threading.Thread(target=self._report_stray_animal_threaded)
        thread.start()

    def _create_view_strays_frame(self):
        frame = customtkinter.CTkFrame(self, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1) # Allow scrollable frame to expand
        title_label = customtkinter.CTkLabel(frame, text="All Reported Stray Animals", font=customtkinter.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.strays_scroll_frame = customtkinter.CTkScrollableFrame(frame, fg_color="transparent")
        self.strays_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.strays_scroll_frame.grid_columnconfigure(0, weight=1)
        return frame

    def refresh_strays_display(self):
        # Clear existing widgets
        for widget in self.strays_scroll_frame.winfo_children():
            widget.destroy()

        all_strays = self.pet_data_manager.get_all_strays()
        if all_strays:
            row_idx = 0
            for stray_id, details in all_strays.items():
                stray_info_text = (
                    f"Stray ID: {stray_id}\n"
                    f"Species: {details.get('species', 'N/A')}\n"
                    f"Breed: {details.get('breed', 'N/A')}\n"
                    f"Color: {details.get('color', 'N/A')}\n"
                    f"Location: {details.get('location', 'N/A')}\n"
                    f"Description: {details.get('description', 'N/A')}\n"
                    f"Reported Date: {details.get('reported_date', 'N/A')}\n"
                    f"Status: {details.get('status', 'N/A').capitalize()}\n"
                    f"Contact Info: {details.get('contact_info', 'N/A')}"
                )
                customtkinter.CTkLabel(self.strays_scroll_frame, text=stray_info_text, justify="left", wraplength=400).grid(row=row_idx, column=0, padx=5, pady=5, sticky="ew")

                # Add a "Mark Found/Captured" button for each stray
                mark_found_button = customtkinter.CTkButton(self.strays_scroll_frame, text="Mark Found/Captured", command=lambda s_id=stray_id: self._mark_stray_found_confirmation(s_id))
                mark_found_button.grid(row=row_idx, column=1, padx=5, pady=5, sticky="e")

                customtkinter.CTkFrame(self.strays_scroll_frame, height=1, fg_color="gray").grid(row=row_idx+1, column=0, columnspan=2, sticky="ew", pady=5)
                row_idx += 2
        else:
            customtkinter.CTkLabel(self.strays_scroll_frame, text="No stray animal reports found.").grid(row=0, column=0, padx=20, pady=20)


    def _mark_stray_found_confirmation(self, stray_id):
        msg_box = messagebox.askyesno("Confirm Found", f"Are you sure you want to mark stray report {stray_id} as found/captured?")
        if msg_box:
            if self.report_manager.report_stray_found_captured(stray_id):
                messagebox.showinfo("Success", f"Stray report {stray_id} marked as found/captured.")
                self.refresh_strays_display()
            else:
                messagebox.showerror("Error", f"Failed to mark stray report {stray_id} as found/captured.")


    def _create_search_frame(self):
        frame = customtkinter.CTkFrame(self, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1) # Allow tabview to expand

        title_label = customtkinter.CTkLabel(frame, text="Search Animals", font=customtkinter.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.search_tabview = customtkinter.CTkTabview(frame)
        self.search_tabview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.search_tabview.add("Lost Pets")
        self.search_tabview.add("Stray Animals")

        # --- Lost Pets Search Tab ---
        lost_search_frame = self.search_tabview.tab("Lost Pets")
        lost_search_frame.grid_columnconfigure((0,1), weight=1)
        lost_search_frame.grid_rowconfigure(5, weight=1) # Results frame

        customtkinter.CTkLabel(lost_search_frame, text="Species (Optional):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.lost_species_entry = customtkinter.CTkEntry(lost_search_frame)
        self.lost_species_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        customtkinter.CTkLabel(lost_search_frame, text="Location Last Seen (Optional):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.lost_location_entry = customtkinter.CTkEntry(lost_search_frame)
        self.lost_location_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        customtkinter.CTkLabel(lost_search_frame, text="Breed (Optional):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.lost_breed_entry = customtkinter.CTkEntry(lost_search_frame)
        self.lost_breed_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        customtkinter.CTkLabel(lost_search_frame, text="Color (Optional):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.lost_color_entry = customtkinter.CTkEntry(lost_search_frame)
        self.lost_color_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        search_lost_button = customtkinter.CTkButton(lost_search_frame, text="Search Lost Pets", command=self._perform_search)
        search_lost_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

        self.lost_results_scroll_frame = customtkinter.CTkScrollableFrame(lost_search_frame, fg_color="transparent")
        self.lost_results_scroll_frame.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.lost_results_scroll_frame.grid_columnconfigure(0, weight=1)

        # --- Stray Animals Search Tab ---
        stray_search_frame = self.search_tabview.tab("Stray Animals")
        stray_search_frame.grid_columnconfigure((0,1), weight=1)
        stray_search_frame.grid_rowconfigure(5, weight=1) # Results frame

        customtkinter.CTkLabel(stray_search_frame, text="Species (Optional):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.stray_search_species_entry = customtkinter.CTkEntry(stray_search_frame)
        self.stray_search_species_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        customtkinter.CTkLabel(stray_search_frame, text="Location Found (Optional):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.stray_search_location_entry = customtkinter.CTkEntry(stray_search_frame)
        self.stray_search_location_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        customtkinter.CTkLabel(stray_search_frame, text="Breed (Optional):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.stray_search_breed_entry = customtkinter.CTkEntry(stray_search_frame)
        self.stray_search_breed_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        customtkinter.CTkLabel(stray_search_frame, text="Color (Optional):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.stray_search_color_entry = customtkinter.CTkEntry(stray_search_frame)
        self.stray_search_color_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        search_stray_button = customtkinter.CTkButton(stray_search_frame, text="Search Stray Animals", command=self._perform_search)
        search_stray_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

        self.stray_results_scroll_frame = customtkinter.CTkScrollableFrame(stray_search_frame, fg_color="transparent")
        self.stray_results_scroll_frame.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.stray_results_scroll_frame.grid_columnconfigure(0, weight=1)

        return frame

    def _perform_search(self):
        # Clear previous results for both tabs
        for widget in self.lost_results_scroll_frame.winfo_children():
            widget.destroy()
        for widget in self.stray_results_scroll_frame.winfo_children():
            widget.destroy()

        # Get values from Lost Pets search fields
        species = self.lost_species_entry.get().strip() or None
        location = self.lost_location_entry.get().strip() or None
        breed = self.lost_breed_entry.get().strip() or None
        color = self.lost_color_entry.get().strip() or None

        # Perform search for lost pets
        lost_results = self.search_manager.search_lost_pets(species, location, breed, color)
        if lost_results:
            row_idx = 0
            for pet_id, details in lost_results.items():
                lost_details = details.get('lost_details', {})
                result_text = (
                    f"ID: {pet_id}\n"
                    f"Name: {details.get('pet_name', 'N/A')}\n"
                    f"Species: {details.get('species', 'N/A')}\n"
                    f"Breed: {details.get('breed', 'N/A')}\n"
                    f"Color: {details.get('color', 'N/A')}\n"
                    f"Last Seen: {lost_details.get('location', 'N/A')} on {lost_details.get('timestamp', 'N/A')}"
                )
                customtkinter.CTkLabel(self.lost_results_scroll_frame, text=result_text, justify="left", wraplength=400).grid(row=row_idx, column=0, padx=5, pady=5, sticky="ew")
                customtkinter.CTkFrame(self.lost_results_scroll_frame, height=1, fg_color="gray").grid(row=row_idx+1, column=0, sticky="ew") # Separator
                row_idx += 2 # Increment by 2 for content and separator
            self.search_tabview.set("Lost Pets") # Switch to Lost Pets tab if results found
        else:
            customtkinter.CTkLabel(self.lost_results_scroll_frame, text="No lost pets found matching your criteria.").grid(row=0, column=0, padx=20, pady=20)


        # Get values from Stray Animals search fields
        stray_species = self.stray_search_species_entry.get().strip() or None
        stray_location = self.stray_search_location_entry.get().strip() or None
        stray_breed = self.stray_search_breed_entry.get().strip() or None
        stray_color = self.stray_search_color_entry.get().strip() or None

        # Perform search for stray animals
        stray_results = self.search_manager.search_stray_pets(stray_species, stray_location, stray_breed, stray_color)
        if stray_results:
            row_idx = 0
            for stray_id, details in stray_results.items():
                result_text = (
                    f"Stray ID: {stray_id}\\n"
                    f"Species: {details.get('species', 'N/A')}\\n"
                    f"Breed: {details.get('breed', 'N/A')}\\n"
                    f"Color: {details.get('color', 'N/A')}\\n"
                    f"Location: {details.get('location', 'N/A')}\\n"
                    f"Description: {details.get('description', 'N/A')}\\n"
                    f"Reported Date: {details.get('reported_date', 'N/A')}\\n"
                    f"Contact Info: {details.get('contact_info', 'N/A')}"
                )
                customtkinter.CTkLabel(self.stray_results_scroll_frame, text=result_text, justify="left", wraplength=400).grid(row=row_idx, column=0, padx=5, pady=5, sticky="ew")
                customtkinter.CTkFrame(self.stray_results_scroll_frame, height=1, fg_color="gray").grid(row=row_idx+1, column=0, sticky="ew") # Separator
                row_idx += 2
            if not lost_results: # Only switch to stray animals tab if no lost pets results
                self.search_tabview.set("Stray Animals")
        else:
            customtkinter.CTkLabel(self.stray_results_scroll_frame, text="No stray animals found matching your criteria.").grid(row=0, column=0, padx=20, pady=20)