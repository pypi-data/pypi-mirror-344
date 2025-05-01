from typing import Dict, Any

class ValidationService:
    """
    A service that provides validation using multiple validators.
    
    This demonstrates using tagged services in the DI container.
    """
    
    def __init__(self, validators: Dict[str, Any]):
        """
        Initialize with a dictionary of validators.
        
        Args:
            validators: A dictionary of validator services, keyed by their alias
        """
        self.validators = validators
        
    def validate(self, type_name: str, value: str) -> bool:
        """
        Validate a value using the appropriate validator.
        
        Args:
            type_name: The type of validation to perform (e.g., 'email', 'url')
            value: The value to validate
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            KeyError: If no validator exists for the given type
        """
        if type_name not in self.validators:
            raise KeyError(f"No validator registered for type: {type_name}")
            
        return self.validators[type_name].validate(value)
    
    def get_error_message(self, type_name: str) -> str:
        """
        Get the error message for a specific validator.
        
        Args:
            type_name: The type of validation (e.g., 'email', 'url')
            
        Returns:
            Error message for the specified validator
            
        Raises:
            KeyError: If no validator exists for the given type
        """
        if type_name not in self.validators:
            raise KeyError(f"No validator registered for type: {type_name}")
            
        return self.validators[type_name].get_error_message()