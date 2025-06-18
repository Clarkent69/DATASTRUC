import customtkinter
import tkinter.messagebox as messagebox # Import messagebox for validation errors

class UpdatePetDialog(customtkinter.CTkToplevel):
    def __init__(self, master, pet_details):
        super().__init__(master)
        self.title(f"Update {pet_details.get('pet_name', 'Pet')} Details")
        self.geometry("400x350")
        self.resizable(False, False)
        self.grab_set() # Make window modal
        self.focus_set() # Focus on this window

        self.updated_data = None # This will store the dictionary of updated fields or None if cancelled

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=0) # Auto-size rows

        # --- Widgets for Pet Details ---
        row_idx = 0

        customtkinter.CTkLabel(self, text="Pet Name:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
        self.name_entry = customtkinter.CTkEntry(self, width=250)
        self.name_entry.insert(0, pet_details.get('pet_name', ''))
        self.name_entry.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
        row_idx += 1

        customtkinter.CTkLabel(self, text="Species:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
        self.species_optionmenu = customtkinter.CTkOptionMenu(self, values=["Dog", "Cat", "Other"])
        self.species_optionmenu.set(pet_details.get('species', 'Dog'))
        self.species_optionmenu.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
        row_idx += 1

        customtkinter.CTkLabel(self, text="Breed:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
        self.breed_entry = customtkinter.CTkEntry(self, width=250)
        self.breed_entry.insert(0, pet_details.get('breed', ''))
        self.breed_entry.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
        row_idx += 1

        customtkinter.CTkLabel(self, text="Color:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
        self.color_entry = customtkinter.CTkEntry(self, width=250)
        self.color_entry.insert(0, pet_details.get('color', ''))
        self.color_entry.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
        row_idx += 1

        customtkinter.CTkLabel(self, text="Age (years/months):").grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
        self.age_entry = customtkinter.CTkEntry(self, width=250)
        # Ensure age is displayed correctly, even if it's None or a float
        self.age_entry.insert(0, str(pet_details['age']) if pet_details.get('age') is not None else '')
        self.age_entry.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
        row_idx += 1

        # --- Buttons ---
        self.button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=row_idx, column=0, columnspan=2, pady=20)
        self.button_frame.grid_columnconfigure((0,1), weight=1) # Center buttons

        self.ok_button = customtkinter.CTkButton(self.button_frame, text="OK", command=self._on_ok)
        self.ok_button.grid(row=0, column=0, padx=10)

        self.cancel_button = customtkinter.CTkButton(self.button_frame, text="Cancel", command=self._on_cancel)
        self.cancel_button.grid(row=0, column=1, padx=10)

    def _on_ok(self):
        # Validate and collect data
        new_name = self.name_entry.get().strip()
        new_species = self.species_optionmenu.get().strip()
        new_breed = self.breed_entry.get().strip()
        new_color = self.color_entry.get().strip()
        new_age_str = self.age_entry.get().strip()

        if not new_name or not new_species or not new_breed or not new_color:
            messagebox.showerror("Input Error", "Pet name, species, breed, and color cannot be empty.")
            return

        new_age = None
        if new_age_str:
            try:
                new_age = float(new_age_str)
                if new_age < 0:
                    messagebox.showerror("Input Error", "Age cannot be negative.")
                    return
            except ValueError:
                messagebox.showerror("Input Error", "Age must be a number (e.g., 2 or 0.5).")
                return

        self.updated_data = {
            'pet_name': new_name,
            'species': new_species,
            'breed': new_breed,
            'color': new_color,
            'age': new_age
        }
        self.destroy() # Close the dialog

    def _on_cancel(self):
        self.updated_data = None # Set to None to indicate cancellation
        self.destroy() # Close the dialog

    def get_input(self):
        self.master.wait_window(self) # Wait until this window is closed
        return self.updated_data