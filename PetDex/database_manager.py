import logging # Import the logging module for recording application events

logger = logging.getLogger(__name__) # Get a logger instance for this module

class InMemoryDBManager:
    def __init__(self):
        """
        Initializes the in-memory database.
        self.users: A dictionary where user_id (string) is the key,
                     and user data (another dictionary) is the value.
                     This dictionary acts as our primary "hash table" for user data.
        self.username_to_id: A dictionary to quickly look up user_id by username.
                              This also functions like a hash table for username indexing.
        """
        self.users = {} # Main hash table (dictionary) to store user records, keyed by user_id
        self.username_to_id = {} # Secondary hash table (dictionary) for quick username-to-user_id lookups
        self.pets = {} # Hash table (dictionary) to store pet records, keyed by pet_id
        self.strays = {} # Hash table (dictionary) to store stray reports, keyed by stray_id
        logger.info("InMemoryDBManager initialized. Data will not be persistent.") # Log initialization status

    def connect(self):
        # This method is kept for compatibility with the main application flow (Main.py)
        # It does not perform actual database connection for an in-memory database
        logger.info("In-memory database is always 'connected'.") # Log that connection is implicit
        pass # No operation needed as data is in memory

    def close(self):
        # This method is kept for compatibility with the main application flow (Main.py)
        # In a persistent database, this would close the connection. Here, data is lost on exit.
        logger.info("In-memory database closed (data will be lost).") # Log that data will be lost
        pass # No operation needed as data is managed by Python's garbage collector on exit

    def create_tables(self):
        # This method is kept for compatibility with the main application flow (Main.py)
        # For an in-memory dictionary-based database, 'tables' implicitly exist as dictionaries.
        logger.info("In-memory database tables implicitly exist (dictionaries).") # Log that tables are implicit
        pass # No operation needed as no SQL tables are created

    def _execute_query(self, query=None, params=(), fetch_one=False, fetch_all=False):
        """
        Placeholder for compatibility. In-memory operations are direct dictionary manipulations.
        This method will essentially do nothing as it's not needed for dict operations.
        """
        pass # This method is a leftover from the SQLite implementation and is not used here.

    # --- User Management Methods ---

    def add_user(self, user_id, username, password_hash, contact_info, registration_date):
        """
        Adds a new user to the in-memory database.
        Returns True if successful, False if username already exists.
        """
        if username in self.username_to_id: # Check if the username already exists in the username-to-ID hash table
            logger.warning(f"In-memory DB: Username '{username}' already exists. Cannot add user.") # Log warning
            return False # Return False if username is already taken

        user_data = { # Create a dictionary to store all user-related data
            'user_id': user_id,
            'username': username,
            'password_hash': password_hash,
            'contact_info': contact_info, # Store contact_info directly as a dictionary
            'registration_date': registration_date
        }
        self.users[user_id] = user_data # Add the new user data to the main users hash table, keyed by user_id
        self.username_to_id[username] = user_id # Add the username-to-user_id mapping to the secondary hash table
        logger.info(f"In-memory DB: User '{username}' added.") # Log successful addition
        return True # Indicate successful addition

    def get_user_by_username(self, username):
        """
        Retrieves user details by username from the in-memory database.
        """
        user_id = self.username_to_id.get(username) # Get the user_id from the username-to-ID hash table
        if user_id: # If a user_id was found for the given username
            user_data = self.users.get(user_id) # Retrieve the full user data from the main users hash table using the user_id
            logger.info(f"In-memory DB: Retrieved user by username '{username}'.") # Log successful retrieval
            return user_data # Return the user data
        logger.info(f"In-memory DB: User by username '{username}' not found.") # Log if username not found
        return None # Return None if username not found

    def get_user_by_id(self, user_id):
        """
        Retrieves user details by user ID from the in-memory database.
        """
        user_data = self.users.get(user_id) # Retrieve user data directly from the main users hash table using user_id
        if user_data: # If user data was found
            logger.info(f"In-memory DB: Retrieved user by ID '{user_id}'.") # Log successful retrieval
        else: # If user data was not found
            logger.info(f"In-memory DB: User by ID '{user_id}' not found.") # Log if user_id not found
        return user_data # Return user data or None

    def update_user(self, user_id, new_details):
        """
        Updates details of an existing user in the in-memory database.
        """
        if user_id in self.users: # Check if the user_id exists in the main users hash table
            current_username = self.users[user_id]['username'] # Get the current username of the user
            
            # If a new username is provided and it's different from the current one
            if 'username' in new_details and new_details['username'] != current_username:
                new_username = new_details['username'] # Get the new username
                # Check if the new username is already taken by another user
                if new_username in self.username_to_id and self.username_to_id[new_username] != user_id:
                    logger.warning(f"In-memory DB: Cannot update user {user_id}. New username '{new_username}' is already taken.") # Log conflict
                    return False # Return False if the new username is taken

                # Remove the old username mapping from the secondary hash table
                if current_username in self.username_to_id:
                    del self.username_to_id[current_username]
                self.username_to_id[new_username] = user_id # Add the new username-to-ID mapping
            
            self.users[user_id].update(new_details) # Update the user's details in the main users hash table
            logger.info(f"In-memory DB: User '{user_id}' updated.") # Log successful update
            return True # Indicate successful update
        logger.warning(f"In-memory DB: User '{user_id}' not found for update.") # Log if user not found for update
        return False # Return False if user_id not found

    def delete_user(self, user_id):
        """
        Deletes a user from the in-memory database by user ID.
        Also deletes associated pets and stray reports (simplified for in-memory).
        """
        if user_id in self.users: # Check if the user_id exists in the main users hash table
            username = self.users[user_id]['username'] # Get the username before deleting the user record
            del self.users[user_id] # Delete the user record from the main users hash table
            if username in self.username_to_id: # Check if the username exists in the secondary hash table
                del self.username_to_id[username] # Delete the username-to-ID mapping
            logger.info(f"In-memory DB: User '{user_id}' deleted.") # Log successful deletion

            # Simplified cascade deletion for in-memory: find and delete associated pet and stray records
            # This demonstrates handling relationships in an in-memory context.
            pets_to_delete = [pid for pid, pet in self.pets.items() if pet.get('owner_id') == user_id] # Find pets owned by this user
            for pid in pets_to_delete: # Iterate through pets to delete
                del self.pets[pid] # Delete each associated pet from the pets hash table
                logger.info(f"In-memory DB: Deleted associated pet {pid} for user {user_id}.") # Log pet deletion

            strays_to_delete = [sid for sid, stray in self.strays.items() if stray.get('reporter_id') == user_id] # Find stray reports by this user
            for sid in strays_to_delete: # Iterate through stray reports to delete
                del self.strays[sid] # Delete each associated stray report from the strays hash table
                logger.info(f"In-memory DB: Deleted associated stray report {sid} by user {user_id}.") # Log stray deletion

            return True # Indicate successful deletion
        logger.warning(f"In-memory DB: User '{user_id}' not found for deletion.") # Log if user not found for deletion
        return False # Return False if user_id not found
    
    def get_total_users(self):
        """Counts the total number of users in the in-memory database."""
        return len(self.users) # Return the number of entries in the users hash table

    # --- Pet Management Methods ---
    
    def add_pet(self, pet_id, owner_id, pet_name, species, breed, age, color, image_path, registration_date):
        """Adds a new pet to the in-memory database."""
        if pet_id in self.pets: # Check if the pet_id already exists in the pets hash table
            logger.warning(f"In-memory DB: Pet ID '{pet_id}' already exists. Cannot add pet.") # Log warning
            return False # Return False if pet_id is already taken
        
        pet_data = { # Create a dictionary to store all pet-related data
            'pet_id': pet_id,
            'owner_id': owner_id,
            'pet_name': pet_name,
            'species': species,
            'breed': breed,
            'age': age,
            'color': color,
            'image_path': image_path,
            'registration_date': registration_date,
            'status': 'registered', # Initial status of a new pet
            'lost_details': None # Initialize lost_details as None
        }
        self.pets[pet_id] = pet_data # Add the new pet data to the pets hash table, keyed by pet_id
        logger.info(f"In-memory DB: Pet '{pet_name}' added for owner '{owner_id}'.") # Log successful addition
        return True # Indicate successful addition

    def get_pet(self, pet_id):
        """Retrieves pet details by pet ID."""
        pet_data = self.pets.get(pet_id) # Retrieve pet data directly from the pets hash table using pet_id
        if pet_data: # If pet data was found
            logger.info(f"In-memory DB: Retrieved pet by ID '{pet_id}'.") # Log successful retrieval
        else: # If pet data was not found
            logger.info(f"In-memory DB: Pet by ID '{pet_id}' not found.") # Log if pet_id not found
        return pet_data # Return pet data or None

    def get_all_pets_by_owner(self, owner_id):
        """Retrieves all pets registered to a specific owner."""
        # Use a dictionary comprehension to filter pets by owner_id and create a new dictionary
        owner_pets = {pet_id: pet_data for pet_id, pet_data in self.pets.items() if pet_data.get('owner_id') == owner_id}
        logger.info(f"In-memory DB: Retrieved {len(owner_pets)} pets for owner '{owner_id}'.") # Log count of retrieved pets
        return owner_pets # Return the dictionary of pets owned by the specified owner

    def get_all_registered_pets(self):
        """Retrieves all registered pets."""
        logger.info("In-memory DB: Retrieved all registered pets.") # Log that all pets are being retrieved
        return self.pets # Return the entire pets hash table (all registered pets)

    def update_pet(self, pet_id, new_details):
        """Updates details of an existing pet."""
        if pet_id in self.pets: # Check if the pet_id exists in the pets hash table
            self.pets[pet_id].update(new_details) # Update the pet's details in the pets hash table
            logger.info(f"In-memory DB: Pet '{pet_id}' updated.") # Log successful update
            return True # Indicate successful update
        logger.warning(f"In-memory DB: Pet '{pet_id}' not found for update.") # Log if pet not found for update
        return False # Return False if pet_id not found

    def delete_pet(self, pet_id):
        """Deletes a pet from the in-memory database by pet ID."""
        if pet_id in self.pets: # Check if the pet_id exists in the pets hash table
            del self.pets[pet_id] # Delete the pet record from the pets hash table
            logger.info(f"In-memory DB: Pet '{pet_id}' deleted.") # Log successful deletion
            return True # Indicate successful deletion
        logger.warning(f"In-memory DB: Pet '{pet_id}' not found for deletion.") # Log if pet not found for deletion
        return False # Return False if pet_id not found

    def get_all_lost_pets(self):
        """Retrieves all pets currently marked as 'lost'."""
        # Use a dictionary comprehension to filter pets that have 'status' set to 'lost'
        lost_pets = {pet_id: pet_data for pet_id, pet_data in self.pets.items() if pet_data.get('status') == 'lost'}
        logger.info(f"In-memory DB: Retrieved {len(lost_pets)} lost pets.") # Log count of lost pets
        return lost_pets # Return the dictionary of lost pets

    # --- Stray Pet Management Methods ---
    
    def add_stray_pet_report(self, stray_id, reporter_id, species, location, breed, color, description, contact_info, reported_date):
        """Adds a new stray pet report to the in-memory database."""
        if stray_id in self.strays: # Check if the stray_id already exists in the strays hash table
            logger.warning(f"In-memory DB: Stray ID '{stray_id}' already exists. Cannot add report.") # Log warning
            return False # Return False if stray_id is already taken
        
        stray_data = { # Create a dictionary to store all stray report data
            'stray_id': stray_id,
            'reporter_id': reporter_id,
            'species': species,
            'location': location,
            'breed': breed,
            'color': color,
            'description': description,
            'contact_info': contact_info, # Store contact_info directly as a dictionary
            'reported_date': reported_date,
            'status': 'stray' # Initial status of a new stray report
        }
        self.strays[stray_id] = stray_data # Add the new stray report data to the strays hash table, keyed by stray_id
        logger.info(f"In-memory DB: Stray report '{stray_id}' added.") # Log successful addition
        return True # Indicate successful addition

    def get_stray_pet(self, stray_id):
        """Retrieves stray pet details by stray ID."""
        stray_data = self.strays.get(stray_id) # Retrieve stray data directly from the strays hash table using stray_id
        if stray_data: # If stray data was found
            logger.info(f"In-memory DB: Retrieved stray pet by ID '{stray_id}'.") # Log successful retrieval
        else: # If stray data was not found
            logger.info(f"In-memory DB: Stray pet by ID '{stray_id}' not found.") # Log if stray_id not found
        return stray_data # Return stray data or None

    def get_all_stray_pets(self):
        """Retrieves all stray pets."""
        logger.info("In-memory DB: Retrieved all stray reports.") # Log that all stray reports are being retrieved
        return self.strays # Return the entire strays hash table (all stray reports)

    def mark_stray_found_captured(self, stray_id):
        """Marks a stray pet report as found/captured."""
        if stray_id in self.strays: # Check if the stray_id exists in the strays hash table
            self.strays[stray_id]['status'] = 'found_captured' # Update the 'status' field of the stray report
            logger.info(f"In-memory DB: Stray report '{stray_id}' marked as found/captured.") # Log successful update
            return True # Indicate successful update
        logger.warning(f"In-memory DB: Stray report '{stray_id}' not found for status update.") # Log if stray not found for update
        return False # Return False if stray_id not found