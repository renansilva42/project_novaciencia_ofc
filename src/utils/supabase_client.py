import os
from supabase import create_client, Client
from loguru import logger

class SupabaseClient:
    """
    Client for interacting with Supabase for authentication and data storage.
    """
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client = self._initialize_client()
        
    def _initialize_client(self) -> Client:
        """Initialize the Supabase client."""
        try:
            client = create_client(self.url, self.key)
            logger.info("Supabase client initialized successfully")
            return client
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {str(e)}")
            raise
            
    def sign_up(self, email, password):
        """
        Sign up a new user with email and password.
        
        Args:
            email: User's email address
            password: User's password
            
        Returns:
            User data if successful, None otherwise
        """
        try:
            response = self.client.auth.sign_up({
                "email": email,
                "password": password
            })
            logger.info(f"User signed up: {email}")
            return response.user
        except Exception as e:
            logger.error(f"Sign up failed: {str(e)}")
            raise
            
    def sign_in(self, email, password):
        """
        Sign in an existing user with email and password.
        
        Args:
            email: User's email address
            password: User's password
            
        Returns:
            User data if successful, None otherwise
        """
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            logger.info(f"User signed in: {email}")
            return response.user
        except Exception as e:
            logger.error(f"Sign in failed: {str(e)}")
            raise
            
    def sign_out(self):
        """Sign out the current user."""
        try:
            self.client.auth.sign_out()
            logger.info("User signed out")
        except Exception as e:
            logger.error(f"Sign out failed: {str(e)}")
            raise
            
    def get_user(self):
        """Get the current user."""
        try:
            return self.client.auth.get_user()
        except Exception as e:
            logger.error(f"Failed to get user: {str(e)}")
            return None
            
    def get_session(self):
        """Get the current session."""
        try:
            return self.client.auth.get_session()
        except Exception as e:
            logger.error(f"Failed to get session: {str(e)}")
            return None