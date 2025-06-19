import logging # Import the logging module for recording application events
import uuid # Import uuid for generating universally unique IDs
from datetime import date # Import date for capturing the current date

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') # Configure basic logging
logger = logging.getLogger(__name__) # Get a logger instance for this module

class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager # Store the database manager instance (InMemoryDBManager in this case)
        self.users_status_message = "" # Initialize a message string for UI feedback

    def hash_password(self, password):
        # This is a Just a String Manipulation function to simulate password verification.
        # For a real application, you should replace this with a robust hashing library.
        return f"hashed_{password}_securely" # Returns a simple "hashed" string for demonstration

    def verify_password(self, password, hashed_password):
        # This is a Just a String Manipulation function to simulate password verification.
        # For a real application, you should replace this with a robust verification method.
        return hashed_password == f"hashed_{password}_securely" # Compares the provided password with the stored hash

    def register_user(self, username, password, contact_info=None):
        """
        Registers a new user.
        Returns user_id if successful, None if username already exists.
        """
        # Check if username already exists by querying the database manager
        if self.db_manager.get_user_by_username(username):
            self.users_status_message = f"Username '{username}' already exists. Please choose a different one." # Set status message for UI
            logger.warning(f"Registration failed: Username '{username}' already exists.") # Log the failure
            return None # Return None as registration failed

        user_id = f"USR-{uuid.uuid4().hex[:8].upper()}" # Generate a unique user ID using UUID
        hashed_password = self.hash_password(password) # Hash the user's password
        registration_date = str(date.today()) # Get the current date as a string

        # Attempt to add the new user to the database via the db_manager
        if self.db_manager.add_user(user_id, username, hashed_password, contact_info or {}, registration_date):
            self.users_status_message = "Registration successful!" # Set success message for UI
            logger.info(f"User '{username}' registered successfully with ID: {user_id}") # Log success
            return user_id # Return the newly registered user's ID
        else:
            self.users_status_message = "Registration failed due to a database error." # Set error message for UI
            logger.error(f"Failed to add user '{username}' to the database.") # Log the database error
            return None # Return None if database addition failed

    def login_user(self, username, password):
        """
        Logs in a user.
        Returns user_id if successful, None otherwise.
        """
        # Retrieve user data from the database manager using the provided username
        user_data = self.db_manager.get_user_by_username(username)
        if user_data: # If user data was found (username exists)
            # Verify the provided password against the stored hashed password
            if self.verify_password(password, user_data['password_hash']):
                self.users_status_message = "Login successful!" # Set success message for UI
                logger.info(f"User '{username}' logged in successfully.") # Log successful login
                return user_data['user_id'] # Return the user's ID
            else: # If password verification fails
                self.users_status_message = "Incorrect password." # Set error message for UI
                logger.warning(f"Login failed for '{username}': Incorrect password.") # Log incorrect password attempt
                return None # Return None as login failed
        self.users_status_message = f"Username '{username}' not found." # Set error message for UI if username not found
        logger.warning(f"Login failed: Username '{username}' not found.") # Log username not found attempt
        return None # Return None as login failed

    def get_user(self, user_id):
        """Retrieves user details by user ID from the database."""
        user_details = self.db_manager.get_user_by_id(user_id) # Delegate to the database manager to get user by ID
        if user_details: # If user details are found
            logger.info(f"Retrieved user with ID {user_id}: {user_details.get('username', 'Unknown')}") # Log success
        else: # If user details are not found
            logger.info(f"User with ID {user_id} not found.") # Log user not found
        return user_details # Return user details or None

    def get_user_by_username(self, username):
        """Retrieves user details by username from the database."""
        # Delegate directly to the database manager to get user by username
        return self.db_manager.get_user_by_username(username)

    def update_user(self, user_id, new_details):
        """Updates details of an existing user in the database."""
        # Delegate to the database manager to update user details
        if self.db_manager.update_user(user_id, new_details):
            logger.info(f"Updated user with ID {user_id} in DB.") # Log successful update
            return True # Indicate successful update
        logger.warning(f"User with ID {user_id} not found for update in DB.") # Log user not found for update
        return False # Return False if update failed

    def delete_user(self, user_id):
        """Deletes a user from the database."""
        # Delegate to the database manager to delete the user
        if self.db_manager.delete_user(user_id):
            logger.info(f"Deleted user with ID {user_id} from DB.") # Log successful deletion
            return True # Indicate successful deletion
        logger.warning(f"User with ID {user_id} not found for deletion in DB.") # Log user not found for deletion
        return False # Return False if deletion failed
    
    def get_total_users(self):
        """
        Retrieves the total number of registered users by delegating to DatabaseManager.
        :return: The total number of users.
        """
        logger.info("UserManager: Fetching total user count.") # Log the action
        return self.db_manager.get_total_users() # Delegate to the database manager to get the total user count