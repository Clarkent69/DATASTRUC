import logging # Imports the logging module for application logging
import datetime # Imports datetime for working with dates (e.g., registration date)
import uuid # Imports uuid for generating universally unique identifiers for pets and stray reports

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') # Configures basic logging for the module
logger = logging.getLogger(__name__) # Initializes a logger for this module

class PetDataManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager # Stores an instance of DatabaseManager to interact with the database

    def add_pet(self, owner_id, pet_name, species, breed=None, age=None, color=None, image_path=None):
        """
        Adds a new registered pet to the database.
        Generates a unique pet ID and current registration date.
        """
        pet_id = f"PET-{uuid.uuid4().hex[:8].upper()}" # Generates a unique 8-character hexadecimal ID prefixed with "PET-"
        registration_date = str(datetime.date.today()) # Gets the current date as a string for registration

        # Calls the DatabaseManager to insert the new pet record
        if self.db_manager.add_pet(pet_id, owner_id, pet_name, species, breed, age, color, image_path, registration_date):
            logger.info(f"Pet added: {pet_id} - {pet_name} by owner {owner_id}") # Logs successful pet addition
            return pet_id # Returns the new pet's ID
        logger.error(f"Failed to add pet {pet_name} for owner {owner_id} to the database.") # Logs error if addition fails
        return None # Returns None if pet addition fails

    def get_pet(self, pet_id):
        """Retrieves details of a specific pet by its ID."""
        # Calls DatabaseManager to get pet data
        return self.db_manager.get_pet(pet_id)

    def get_pets_by_owner(self, owner_id):
        """Retrieves all pets owned by a specific user ID."""
        # Calls DatabaseManager to get all pets associated with the owner_id
        return self.db_manager.get_all_pets_by_owner(owner_id)

    def update_pet(self, pet_id, new_details):
        """
        Updates details of an existing pet in the database.
        Delegates the actual database update to DatabaseManager.
        """
        if self.db_manager.update_pet(pet_id, new_details): # Calls DatabaseManager to update pet
            logger.info(f"Pet {pet_id} updated.") # Logs successful update
            return True
        logger.warning(f"Could not update pet {pet_id} (not found or no changes).") # Logs warning if update fails
        return False

    def delete_pet(self, pet_id):
        """
        Deletes a pet from the database.
        Delegates the actual database deletion to DatabaseManager.
        """
        if self.db_manager.delete_pet(pet_id): # Calls DatabaseManager to delete pet
            logger.info(f"Pet {pet_id} deleted.") # Logs successful deletion
            return True
        logger.warning(f"Could not delete pet {pet_id} (not found).") # Logs warning if deletion fails
        return False

    def mark_pet_lost(self, pet_id, lost_details):
        """
        Marks a pet as 'lost' and stores its last known location and timestamp.
        """
        # Updates the pet's status to 'lost' and stores the lost_details
        new_details = {'status': 'lost', 'lost_details': lost_details}
        if self.db_manager.update_pet(pet_id, new_details): # Calls DatabaseManager to update pet status and details
            logger.info(f"Pet {pet_id} marked as lost.") # Logs successful marking
            return True
        logger.warning(f"Could not mark pet {pet_id} as lost (not found).") # Logs warning if marking fails
        return False

    def mark_pet_found(self, pet_id):
        """
        Marks a lost pet as 'registered' (found) and clears its lost details.
        """
        # Updates the pet's status back to 'registered' and clears lost_details
        new_details = {'status': 'registered', 'lost_details': None} # Set lost_details to None to clear it
        if self.db_manager.update_pet(pet_id, new_details): # Calls DatabaseManager to update pet status and clear details
            logger.info(f"Pet {pet_id} marked as found.") # Logs successful marking
            return True
        logger.warning(f"Could not mark pet {pet_id} as found (not found).") # Logs warning if marking fails
        return False

    def get_all_lost_pets(self):
        """Retrieves all pets currently marked as 'lost' from the database."""
        # Calls DatabaseManager to get all lost pets
        return self.db_manager.get_all_lost_pets()

    def add_stray_pet_report(self, reporter_id, species, location, breed=None, color=None, description=None, contact_info=None):
        """
        Adds a new stray pet report to the database.
        Generates a unique stray ID and current reported date.
        """
        stray_id = f"STRAY-{uuid.uuid4().hex[:8].upper()}" # Generates a unique 8-character hexadecimal ID prefixed with "STRAY-"
        reported_date = str(datetime.date.today()) # Gets the current date as a string for the report

        # Calls DatabaseManager to insert the new stray report
        if self.db_manager.add_stray_pet_report(stray_id, reporter_id, species, location, breed, color, description, contact_info or {}, reported_date):
            logger.info(f"Stray pet report added: {stray_id}") # Logs successful report addition
            return stray_id # Returns the new stray report's ID
        logger.error("Failed to generate a unique stray ID or add to database.") # Logs error if addition fails
        return None # Returns None if report addition fails

    def get_stray_pet_report(self, stray_id):
        """Retrieves details of a specific stray pet report by its ID."""
        # Calls DatabaseManager to get stray pet data
        return self.db_manager.get_stray_pet(stray_id)

    def get_all_strays(self):
        """Retrieves all stray pet reports from the database."""
        # Calls DatabaseManager to get all stray pets
        return self.db_manager.get_all_stray_pets()

    def mark_stray_found_captured(self, stray_id):
        """
        Marks a stray pet report as 'found_captured'.
        Delegates the actual database update to DatabaseManager.
        """
        if self.db_manager.mark_stray_found_captured(stray_id): # Calls DatabaseManager to update stray status
            logger.info(f"Stray report {stray_id} marked as found/captured.") # Logs successful marking
            return True
        logger.warning(f"Could not mark stray {stray_id} as found/captured (not found).") # Logs warning if marking fails
        return False