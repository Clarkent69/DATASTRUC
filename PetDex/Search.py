import logging

logger = logging.getLogger(__name__)

class SearchManager:
    def __init__(self, pet_data_manager):
        """
        Initializes the SearchManager with a reference to the PetDataManager.
        :param pet_data_manager: An instance of PetDataManager to interact with pet data.
        """
        self.pet_data_manager = pet_data_manager

    def search_lost_pets(self, species=None, location=None, breed=None, color=None):
        """
        Searches for lost pets based on provided criteria.
        :param species: Optional species to filter by.
        :param location: Optional last seen location to filter by.
        :param breed: Optional breed to filter by.
        :param color: Optional color to filter by.
        :return: A dictionary of matching lost pets {pet_id: pet_details}.
        """
        matching_pets = {}
        all_pets = self.pet_data_manager.pets # Access the internal pets dictionary directly

        for pet_id, details in all_pets.items():
            # Check if the pet is marked as 'lost'
            if details.get('status') == 'lost':
                match = True
                if species and details.get('species').lower() != species.lower():
                    match = False
                if breed and details.get('breed') and details.get('breed').lower() != breed.lower():
                    match = False
                if color and details.get('color') and details.get('color').lower() != color.lower():
                    match = False
                
                # Check location within lost_details if provided
                if location and 'lost_details' in details:
                    lost_location = details['lost_details'].get('location')
                    if lost_location and lost_location.lower() != location.lower():
                        match = False
                elif location and 'lost_details' not in details: # If location is provided but no lost_details
                    match = False
                    
                if match:
                    matching_pets[pet_id] = details
        
        logger.info(f"Search for lost pets completed. Found {len(matching_pets)} matches.")
        return matching_pets

    def search_stray_pets(self, species=None, location=None, breed=None, color=None):
        """
        Searches for stray pet reports based on provided criteria.
        :param species: Optional species to filter by.
        :param location: Optional location where the stray was found.
        :param breed: Optional breed to filter by.
        :param color: Optional color to filter by.
        :return: A dictionary of matching stray reports {stray_id: stray_details}.
        """
        matching_strays = {}
        all_strays = self.pet_data_manager.strays # Access the internal strays dictionary directly

        for stray_id, details in all_strays.items():
            # Only show strays that are still 'stray' (not 'found_captured')
            if details.get('status') == 'stray':
                match = True
                if species and details.get('species') and details.get('species').lower() != species.lower():
                    match = False
                if location and details.get('location') and details.get('location').lower() != location.lower():
                    match = False
                if breed and details.get('breed') and details.get('breed').lower() != breed.lower():
                    match = False
                if color and details.get('color') and details.get('color').lower() != color.lower():
                    match = False
                    
                if match:
                    matching_strays[stray_id] = details
        
        logger.info(f"Search for stray pets completed. Found {len(matching_strays)} matches.")
        return matching_strays