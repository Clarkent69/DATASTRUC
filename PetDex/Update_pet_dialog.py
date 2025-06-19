import customtkinter # Imports the CustomTkinter library for modern GUI elements
import tkinter.messagebox as messagebox # Imports messagebox for displaying pop-up messages (e.g., validation errors)

class UpdatePetDialog(customtkinter.CTkToplevel):
    def __init__(self, master, pet_details):
        super().__init__(master) # Calls the constructor of the parent class (customtkinter.CTkToplevel)
        self.title(f"Update {pet_details.get('pet_name', 'Pet')} Details") # Sets the window title dynamically based on pet name
        self.geometry("400x450") # Sets the fixed size of the dialog window
        self.resizable(False, False) # Prevents the dialog window from being resized by the user
        self.grab_set() # Makes the dialog modal, blocking interaction with the main window until closed
        self.focus_set() # Sets focus to the dialog window

        self.updated_data = None # Initializes a variable to store the dictionary of updated fields, or None if cancelled
        self.pet_details = pet_details # Stores the original pet details passed to the dialog

        # Configure grid for the dialog content
        self.grid_columnconfigure(1, weight=1) # Makes the second column (entry fields) expandable
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=0) # Sets rows to auto-size based on content

        # --- Widgets for Pet Details ---
        row_idx = 0 # Initializes row index for grid layout

        # Pet ID (Read-only)
        customtkinter.CTkLabel(self, text="Pet ID:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="w") # Label for Pet ID
        self.pet_id_label = customtkinter.CTkLabel(self, text=pet_details.get('pet_id', 'N/A'), font=customtkinter.CTkFont(weight="bold")) # Displays the Pet ID
        self.pet_id_label.grid(row=row_idx, column=1, padx=10, pady=5, sticky="w") # Places Pet ID label
        row_idx += 1 # Increment row index

        # Pet Name Entry
        customtkinter.CTkLabel(self, text="Pet Name:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="w") # Label for Pet Name
        self.name_entry = customtkinter.CTkEntry(self) # Entry field for pet name
        self.name_entry.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew") # Places pet name entry
        self.name_entry.insert(0, pet_details.get('pet_name', '')) # Populates with current pet name
        row_idx += 1

        # Species Option Menu
        customtkinter.CTkLabel(self, text="Species:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="w") # Label for Species
        self.species_optionmenu = customtkinter.CTkOptionMenu(self, values=["Dog", "Cat"]) # Dropdown for species
        self.species_optionmenu.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew") # Places species dropdown
        self.species_optionmenu.set(pet_details.get('species', 'Dog')) # Sets current species
        row_idx += 1

        # Breed Entry
        customtkinter.CTkLabel(self, text="Breed (Optional):").grid(row=row_idx, column=0, padx=10, pady=5, sticky="w") # Label for Breed
        self.breed_entry = customtkinter.CTkEntry(self) # Entry field for breed
        self.breed_entry.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew") # Places breed entry
        self.breed_entry.insert(0, pet_details.get('breed', '')) # Populates with current breed
        row_idx += 1

        # Age Entry
        customtkinter.CTkLabel(self, text="Age (Years):").grid(row=row_idx, column=0, padx=10, pady=5, sticky="w") # Label for Age
        self.age_entry = customtkinter.CTkEntry(self) # Entry field for age
        self.age_entry.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew") # Places age entry
        self.age_entry.insert(0, str(pet_details.get('age', ''))) # Populates with current age (converted to string)
        row_idx += 1

        # Color Entry
        customtkinter.CTkLabel(self, text="Color:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="w") # Label for Color
        self.color_entry = customtkinter.CTkEntry(self) # Entry field for color
        self.color_entry.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew") # Places color entry
        self.color_entry.insert(0, pet_details.get('color', '')) # Populates with current color
        row_idx += 1

        # Image Path Entry
        customtkinter.CTkLabel(self, text="Image Path (Optional):").grid(row=row_idx, column=0, padx=10, pady=5, sticky="w") # Label for Image Path
        self.image_path_entry = customtkinter.CTkEntry(self) # Entry field for image path
        self.image_path_entry.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew") # Places image path entry
        self.image_path_entry.insert(0, str(pet_details.get('image_path', ''))) # Populates with current image path
        row_idx += 1

        # --- Action Buttons ---
        self.button_frame = customtkinter.CTkFrame(self, fg_color="transparent") # Frame for buttons
        self.button_frame.grid(row=row_idx, column=0, columnspan=2, pady=10) # Places button frame below entries
        self.button_frame.grid_columnconfigure((0, 1), weight=1) # Makes button columns expandable

        self.ok_button = customtkinter.CTkButton(self.button_frame, text="OK", command=self._on_ok) # OK button
        self.ok_button.grid(row=0, column=0, padx=5) # Places OK button

        self.cancel_button = customtkinter.CTkButton(self.button_frame, text="Cancel", command=self._on_cancel) # Cancel button
        self.cancel_button.grid(row=0, column=1, padx=5) # Places Cancel button

    def _on_cancel(self):
        """
        Handles the Cancel button click.
        Closes the dialog without storing any updated data.
        """
        self.updated_data = None # Ensures no data is returned
        self.destroy() # Destroys the dialog window

    def _on_ok(self):
        """
        Handles the OK button click.
        Validates input, collects updated data, and stores it in self.updated_data.
        """
        # Validate and collect data from input fields
        new_name = self.name_entry.get().strip() # Gets new pet name
        new_species = self.species_optionmenu.get().strip() # Gets new species
        new_breed = self.breed_entry.get().strip() # Gets new breed
        new_color = self.color_entry.get().strip() # Gets new color
        new_age_str = self.age_entry.get().strip() # Gets new age as string
        new_image_path = self.image_path_entry.get().strip() # Gets new image path

        # Basic validation for mandatory fields
        if not new_name or not new_species or not new_color: # Checks if mandatory fields are empty
            messagebox.showerror("Input Error", "Pet name, species, and color cannot be empty.") # Displays error message
            return # Stops function execution

        new_age = None # Initializes new_age to None
        if new_age_str: # If age is provided
            try:
                new_age = float(new_age_str) # Converts age to float
                if new_age < 0: # Checks for negative age
                    messagebox.showerror("Input Error", "Age cannot be negative.") # Displays error for negative age
                    return # Stops function execution
            except ValueError: # Catches error if age is not a valid number
                messagebox.showerror("Input Error", "Age must be a number (e.g., 2 or 0.5).") # Displays error for invalid age format
                return # Stops function execution

        # Store the collected and validated data
        self.updated_data = {
            'pet_name': new_name, # Stores new name
            'species': new_species, # Stores new species
            'breed': new_breed if new_breed else None, # Stores breed, converting empty string to None
            'color': new_color, # Stores new color
            'age': new_age, # Stores new age
            'image_path': new_image_path if new_image_path else None # Stores image path, converting empty string to None
        }

        self.destroy() # Destroys the dialog window after collecting data