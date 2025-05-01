import re
from typing import Optional

class URLValidator:
    """
    A service that validates URLs.
    """
    
    def __init__(self):
        # Simple URL regex pattern
        self.url_pattern = re.compile(
            r'^(https?|ftp)://'  # scheme
            r'([a-zA-Z0-9.-]+)'  # domain
            r'(\.[a-zA-Z]{2,})'  # top-level domain
            r'(:[0-9]+)?'        # optional port
            r'(/.*)?$'           # optional path
        )
    
    def validate(self, value: str) -> bool:
        """
        Validate that the given string is a valid URL.
        
        Args:
            value: The string to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not value:
            return False
        return bool(self.url_pattern.match(value))
    
    def get_error_message(self) -> str:
        """
        Get the error message for invalid URLs.
        
        Returns:
            Error message string
        """
        return "Invalid URL format"