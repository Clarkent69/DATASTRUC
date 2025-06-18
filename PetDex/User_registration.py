"""
this will handle the user data also using a hash table.
it will store the user data in a hash table and provide methods to add, remove, and retrieve user data.
moreover it will handle user registration and login.
"""
import json
import os
import logging
# For a real application, you'd use a strong password hashing library like bcrypt or Argon2
# For this example, we'll use a basic placeholder for demonstration.
# pip install passlib bcrypt
# from passlib.hash import bcrypt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UserManager:
    def __init__(self):
        self.users = {}
        self._next_user_id = 1
        self.load_users()
        self.users_status_message = ""

    def _get_next_user_id(self):
        """Generates a unique user ID."""
        while f"USR-{self._next_user_id:04d}" in self.users:
            self._next_user_id += 1
        return f"USR-{self._next_user_id:04d}"

    def hash_password(self, password):
        """
        Hashes a password.
        In a production application, use a robust library like bcrypt.
        """
        # For demonstration purposes, we'll return a simple hashed string.
        # This is NOT secure for production!
        return f"hashed_{password}_securely" # Placeholder
        # return bcrypt.hash(password) # Use this with passlib.hash.bcrypt

    def verify_password(self, password, hashed_password):
        """
        Verifies a password against a hashed one.
        In a production application, use a robust library like bcrypt.
        """
        # For demonstration purposes, this is a simple string comparison.
        # This is NOT secure for production!
        return hashed_password == f"hashed_{password}_securely" # Placeholder
        # return bcrypt.verify(password, hashed_password) # Use this with passlib.hash.bcrypt


    def register_user(self, username, password, contact_info=None):
        """
        Registers a new user.
        Returns user_id if successful, None if username already exists.
        """
        if username in [user_data['username'] for user_data in self.users.values()]:
            self.users_status_message = f"Username '{username}' already exists. Please choose a different one." # Set message
            logger.warning(f"Registration failed: Username '{username}' already exists.")
            return None

        user_id = self._get_next_user_id()
        hashed_password = self.hash_password(password)

        user_details = {
            "user_id": user_id,
            "username": username,
            "password_hash": hashed_password,
            "contact_info": contact_info if contact_info else {},
            "registered_pets": []
        }
        self.users[user_id] = user_details
        self.save_users()
        self.users_status_message = "Registration successful!"
        logger.info(f"User '{username}' registered successfully with ID: {user_id}")
        return user_id

    def login_user(self, username, password):
        for user_id, user_data in self.users.items():
            if user_data['username'] == username:
                if self.verify_password(password, user_data['password_hash']):
                    self.users_status_message = "Login successful!"
                    logger.info(f"User '{username}' logged in successfully.")
                    return user_id
                else:
                    self.users_status_message = "Incorrect password."
                    logger.warning(f"Login failed for '{username}': Incorrect password.")
                    return None
        self.users_status_message = f"Username '{username}' not found."
        logger.warning(f"Login failed: Username '{username}' not found.")
        return None

    def get_user(self, user_id):
        """Retrieves user details by user ID."""
        user_details = self.users.get(user_id)
        if user_details:
            logger.info(f"Retrieved user with ID {user_id}: {user_details.get('username', 'Unknown')}")
        else:
            logger.info(f"User with ID {user_id} not found.")
        return user_details

    def get_user_by_username(self, username):
        """Retrieves user details by username."""
        for user_id, user_data in self.users.items():
            if user_data['username'] == username:
                return user_data
        return None

    def update_user(self, user_id, new_details):
        """Updates details of an existing user."""
        if user_id in self.users:
            self.users[user_id].update(new_details)
            self.save_users()
            logger.info(f"Updated user with ID {user_id}.")
            return True
        logger.warning(f"User with ID {user_id} not found for update.")
        return False

    def delete_user(self, user_id):
        """Deletes a user from the system."""
        if user_id in self.users:
            username = self.users[user_id]['username']
            del self.users[user_id]
            self.save_users()
            logger.info(f"Deleted user '{username}' with ID {user_id}.")
            return True
        logger.warning(f"User with ID {user_id} not found for deletion.")
        return False

    def save_users(self):
        """Saves user data to a JSON file."""
        data = {
            'users': self.users,
            '_next_user_id': self._next_user_id
        }
        try:
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=4)
            logger.info("User data saved successfully.")
        except Exception as e:
            logger.error(f"Error saving user data: {e}")

    def load_users(self):
        """Loads user data from a JSON file."""
        if os.path.exists('users.json'):
            try:
                with open('users.json', 'r') as f:
                    data = json.load(f)
                    self.users = data.get('users', {})
                    # Ensure that user_id in self.users are strings (JSON keys are always strings)
                    self.users = {k: v for k, v in self.users.items()}
                    self._next_user_id = data.get('_next_user_id', 1)
                logger.info("User data loaded successfully.")
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON from users.json: {e}")
                self.users = {}
                self._next_user_id = 1
            except Exception as e:
                logger.error(f"Error loading user data from users.json: {e}")
                self.users = {}
                self._next_user_id = 1
        else:
            logger.info("users.json not found, starting with empty user data.")