# Pet_data_manager.py (Ensuring mark_pet_found is correct)

import json
import os
import logging
import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PetDataManager:
    def __init__(self):
        self.pets = {}
        self.strays = {}
        self._next_pet_id = 1
        self._next_stray_id = 1
        self.load_data()

    def _get_next_pet_id(self):
        while f"PET-{self._next_pet_id:04d}" in self.pets:
            self._next_pet_id += 1
        return f"PET-{self._next_pet_id:04d}"

    def _get_next_stray_id(self):
        while f"STRAY-{self._next_stray_id:04d}" in self.strays:
            self._next_stray_id += 1
        return f"STRAY-{self._next_stray_id:04d}"

    def add_pet(self, owner_id, pet_name, species, breed=None, age=None, color=None, image_path=None):
        pet_id = self._get_next_pet_id()
        if pet_id:
            self.pets[pet_id] = {
                "owner_id": owner_id,
                "pet_name": pet_name,
                "species": species,
                "breed": breed,
                "age": age,
                "color": color,
                "image_path": image_path,
                "status": "owned",
                "registration_date": str(datetime.date.today())
            }
            self._next_pet_id += 1
            self.save_data()
            logger.info(f"Pet added: {pet_id} - {pet_name} by owner {owner_id}")
            return pet_id
        logger.error("Failed to generate a unique pet ID.")
        return None

    def get_pet(self, pet_id):
        return self.pets.get(pet_id)

    def get_pets_by_owner(self, owner_id):
        return {p_id: details for p_id, details in self.pets.items() if details.get('owner_id') == owner_id}

    def update_pet(self, pet_id, new_details):
        if pet_id in self.pets:
            self.pets[pet_id].update(new_details)
            self.save_data()
            logger.info(f"Pet updated: {pet_id}")
            return True
        logger.warning(f"Attempted to update non-existent pet: {pet_id}")
        return False

    def delete_pet(self, pet_id):
        if pet_id in self.pets:
            del self.pets[pet_id]
            self.save_data()
            logger.info(f"Pet deleted: {pet_id}")
            return True
        logger.warning(f"Attempted to delete non-existent pet: {pet_id}")
        return False

    def mark_pet_lost(self, pet_id, lost_details):
        if pet_id in self.pets and self.pets[pet_id]['status'] != 'lost':
            self.pets[pet_id]['status'] = 'lost'
            self.pets[pet_id]['lost_details'] = lost_details
            self.save_data()
            logger.info(f"Pet {pet_id} marked as lost.")
            return True
        logger.warning(f"Could not mark pet {pet_id} as lost (not found or already lost).")
        return False

    def mark_pet_found(self, pet_id): # This method correctly marks a pet as found
        if pet_id in self.pets and self.pets[pet_id]['status'] == 'lost':
            self.pets[pet_id]['status'] = 'owned'
            if 'lost_details' in self.pets[pet_id]:
                del self.pets[pet_id]['lost_details']
            self.save_data()
            logger.info(f"Pet {pet_id} marked as found.")
            return True
        logger.warning(f"Could not mark pet {pet_id} as found (not found or not lost).")
        return False

    def add_stray_pet_report(self, stray_details):
        """
        Adds a new stray animal report to the database.
        :param stray_details: A dictionary containing details of the stray animal,
                              including 'reporter_id', 'species', 'breed', 'color',
                              'location', 'description', 'contact_info', 'reported_date', 'status'.
        :return: The ID of the newly added stray report if successful, None otherwise.
        """
        stray_id = self._get_next_stray_id()
        if stray_id:
            self.strays[stray_id] = stray_details
            self._next_stray_id += 1
            self.save_data()
            logger.info(f"Stray pet report added: {stray_id}")
            return stray_id
        logger.error("Failed to generate a unique stray ID.")
        return None

    def get_stray_pet_report(self, stray_id):
        return self.strays.get(stray_id)

    def get_all_strays(self):
        return {s_id: details for s_id, details in self.strays.items() if details.get('status', 'stray') == 'stray'}

    def mark_stray_found_captured(self, stray_id):
        if stray_id in self.strays:
            self.strays[stray_id]['status'] = 'found_captured'
            self.save_data()
            logger.info(f"Stray report {stray_id} marked as found/captured.")
            return True
        logger.warning(f"Could not mark stray {stray_id} as found/captured (not found).")
        return False

    def save_data(self):
        data_to_save = {
            'pets': self.pets,
            'strays': self.strays,
            '_next_pet_id': self._next_pet_id,
            '_next_stray_id': self._next_stray_id
        }
        try:
            with open('pet_data.json', 'w') as f:
                json.dump(data_to_save, f, indent=4)
            logger.info("Pet and stray data saved successfully.")
        except Exception as e:
            logger.error(f"Error saving data to pet_data.json: {e}")

    def load_data(self):
        if os.path.exists('pet_data.json'):
            try:
                with open('pet_data.json', 'r') as f:
                    data = json.load(f)
                    self.pets = data.get('pets', {})
                    self.pets = {k: v for k, v in self.pets.items()}

                    self.strays = data.get('strays', {})
                    self.strays = {k: v for k, v in self.strays.items()}

                    self._next_pet_id = data.get('_next_pet_id', 1)
                    self._next_stray_id = data.get('_next_stray_id', 1)
                logger.info("Pet and stray data loaded successfully.")
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON from pet_data.json: {e}")
                self.pets = {}
                self.strays = {}
                self._next_pet_id = 1
                self._next_stray_id = 1
            except Exception as e:
                logger.error(f"Error loading data from pet_data.json: {e}")
                self.pets = {}
                self.strays = {}
                self._next_pet_id = 1
                self._next_stray_id = 1
        else:
            logger.info("pet_data.json not found. Starting with empty data.")