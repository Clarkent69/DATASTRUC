import logging # Imports the logging module for application logging
import datetime # Imports datetime for date/time operations (though currently not directly used for reporting timestamps, pet_data_manager handles that)

logger = logging.getLogger(__name__) # Initializes a logger for this module

class ReportManager:
    def __init__(self, pet_data_manager):
        """
        Initializes the ReportManager with a reference to the PetDataManager.
        :param pet_data_manager: An instance of PetDataManager to interact with pet data.
        """
        self.pet_data_manager = pet_data_manager # Stores an instance of PetDataManager

    def report_lost_pet(self, pet_id, last_seen_location):
        """
        Marks a pet as lost and stores the lost details using PetDataManager.
        :param pet_id: The ID of the pet to mark as lost.
        :param last_seen_location: The last known location of the lost pet.
        :return: True if successful, False otherwise.
        """
        # First, check if the pet actually exists before attempting to mark it as lost
        if not self.pet_data_manager.get_pet(pet_id):
            logger.warning(f"Report: Pet with ID {pet_id} not found.") # Logs a warning if pet not found
            return False

        # Construct the lost_details dictionary
        lost_details = {
            "location": last_seen_location, # Stores the last seen location
            "timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), # Records the current timestamp
            # The owner_id is already part of the pet record, no need to add here again
        }
        # Call the PetDataManager to update the pet's status to 'lost' and save lost details
        if self.pet_data_manager.mark_pet_lost(pet_id, lost_details):
            logger.info(f"Report: Pet {pet_id} marked as lost.") # Logs successful operation
            return True
        else:
            logger.error(f"Report: Failed to mark pet {pet_id} as lost.") # Logs error if operation fails
            return False

    def mark_pet_found(self, pet_id):
        """
        Marks a previously lost pet as found using PetDataManager.
        :param pet_id: The ID of the pet to mark as found.
        :return: True if successful, False otherwise.
        """
        # Call the PetDataManager to update the pet's status to 'registered' (found)
        if self.pet_data_manager.mark_pet_found(pet_id):
            logger.info(f"Report: Pet {pet_id} marked as found.") # Logs successful operation
            return True
        else:
            logger.error(f"Report: Failed to mark pet {pet_id} as found.") # Logs error if operation fails
            return False

    # --- New methods for generating reports ---

    def get_all_lost_pets_data(self):
        """
        Retrieves data for all pets currently marked as 'lost'.
        This method acts as a facade, delegating the call to PetDataManager.
        :return: A dictionary of lost pets {pet_id: pet_details}.
        """
        logger.info("Report: Generating report for all lost pets.") # Logs report generation
        # PetDataManager's get_all_lost_pets already returns filtered lost pets.
        return self.pet_data_manager.get_all_lost_pets()

    def get_stray_report_data(self):
        """
        Retrieves data for all stray pet reports.
        This method acts as a facade, delegating the call to PetDataManager.
        :return: A dictionary of stray reports {stray_id: stray_details}.
        """
        logger.info("Report: Generating report for all stray pet reports.") # Logs report generation
        # PetDataManager's get_all_strays returns all strays, active or captured.
        return self.pet_data_manager.get_all_strays()

    def get_all_registered_pets_data(self):
        """
        Retrieves data for all registered pets (not just owned by current user).
        This includes pets with 'registered', 'lost', 'found' statuses.
        This method acts as a facade, delegating the call to DatabaseManager via PetDataManager.
        :return: A dictionary of all registered pets {pet_id: pet_details}.
        """
        logger.info("Report: Generating report for all registered pets.") # Logs report generation
        # The PetDataManager can access all registered pets via the db_manager
        # Assuming PetDataManager has a method to get all pets, if not, it should be added or called directly via db_manager
        return self.pet_data_manager.db_manager.get_all_registered_pets() # Directly calls db_manager via pet_data_manager
    
    def get_total_users_data(self):
        """
        Retrieves the total count of registered users.
        This method acts as a facade, delegating the call to DatabaseManager.
        :return: The total number of users.
        """
        logger.info("Report: Generating total users count.") # Logs report generation
        # DatabaseManager can directly provide the total user count
        return self.pet_data_manager.db_manager.get_total_users() # Directly calls db_manager via pet_data_manager