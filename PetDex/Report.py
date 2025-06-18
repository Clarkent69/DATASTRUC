# Report.py

import logging
import datetime

logger = logging.getLogger(__name__)

class ReportManager:
    def __init__(self, pet_data_manager):
        self.pet_data_manager = pet_data_manager

    def report_lost_pet(self, pet_id, last_seen_location):
        if not self.pet_data_manager.get_pet(pet_id):
            logger.warning(f"Report: Pet with ID {pet_id} not found.")
            return False

        lost_details = {
            "location": last_seen_location,
            "timestamp": str(datetime.datetime.now()),
            "reported_by_owner_id": self.pet_data_manager.get_pet(pet_id).get('owner_id')
        }
        if self.pet_data_manager.mark_pet_lost(pet_id, lost_details):
            logger.info(f"Report: Pet {pet_id} successfully marked as lost at {last_seen_location}.")
            return True
        else:
            logger.error(f"Report: Failed to mark pet {pet_id} as lost.")
            return False

    def report_found_pet(self, pet_id):
        """
        Marks a lost pet as found.
        :param pet_id: The ID of the pet to mark as found.
        :return: True if successful, False otherwise.
        """
        # CORRECTED: Call the existing 'mark_pet_found' method in PetDataManager
        if self.pet_data_manager.mark_pet_found(pet_id):
            logger.info(f"Report: Pet {pet_id} successfully marked as found.")
            return True
        else:
            logger.error(f"Report: Failed to mark pet {pet_id} as found.")
            return False

    def report_stray_pet(self, reporter_id, species, location, breed=None, color=None, description=None, contact_info=None):
        """
        Registers a new stray animal report.
        :param reporter_id: The ID of the user reporting the stray animal.
        :param species: The species of the stray animal (e.g., "Dog", "Cat").
        :param location: The location where the stray animal was found.
        :param breed: Optional breed of the stray animal.
        :param color: Optional color of the stray animal.
        :param description: Optional description of the stray animal.
        :param contact_info: Optional contact information of the reporter.
        :return: The ID of the newly reported stray pet if successful, None otherwise.
        """
        stray_details = {
            "reporter_id": reporter_id,
            "species": species,
            "location": location,
            "breed": breed,  # Ensure breed is passed
            "color": color,  # Ensure color is passed
            "description": description,
            "contact_info": contact_info,
            "reported_date": str(datetime.date.today()),
            "status": "stray"
        }
        stray_id = self.pet_data_manager.add_stray_pet_report(stray_details)
        if stray_id:
            logger.info(f"Report: New stray pet reported. ID: {stray_id}, Species: {species}, Location: {location}, Reporter: {reporter_id}")
            return stray_id
        else:
            logger.error(f"Report: Failed to report stray pet. Species: {species}, Location: {location}")
            return None

    def report_stray_found_captured(self, stray_id):
        """
        Marks a stray pet report as found/captured.
        :param stray_id: The ID of the stray report to mark.
        :return: True if successful, False otherwise.
        """
        if self.pet_data_manager.mark_stray_found_captured(stray_id):
            logger.info(f"Report: Stray pet {stray_id} successfully marked as found/captured.")
            return True
        else:
            logger.error(f"Report: Failed to mark stray pet {stray_id} as found/captured.")
            return False