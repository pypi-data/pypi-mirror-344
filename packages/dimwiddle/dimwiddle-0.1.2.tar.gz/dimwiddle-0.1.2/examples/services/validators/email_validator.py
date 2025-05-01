import re
from typing import Optional

class EmailValidator:
    """
    A service that validates email addresses.
    """
    
    def __init__(self):
        # Email regex pattern
        self.email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
    
    def validate(self, value: str) -> bool:
        """
        Validate that the given string is a valid email address.
        
        Args:
            value: The string to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not value:
            return False
        return bool(self.email_pattern.match(value))
    
    def get_error_message(self) -> str:
        """
        Get the error message for invalid email addresses.
        
        Returns:
            Error message string
        """
        return "Invalid email address format"