from typing import Any, Optional, Protocol

class ConfigProtocol(Protocol):
    """
    Protocol defining the interface for configuration providers.
    
    This allows different configuration implementations (environment variables,
    YAML files, etc.) to be used interchangeably.
    """
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Get a configuration value by key, with an optional default.
        
        Args:
            key: The configuration key to look up
            default: Value to return if key is not found
            
        Returns:
            The configuration value or default
        """
        ...
    
    def require(self, key: str) -> Any:
        """
        Get a required configuration value by key.
        
        Args:
            key: The configuration key to look up
            
        Returns:
            The configuration value
            
        Raises:
            ValueError: If the key is not found
        """
        ...