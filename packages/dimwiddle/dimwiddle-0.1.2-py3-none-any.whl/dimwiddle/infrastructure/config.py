import os
from typing import Any, Dict, Optional
from dotenv import load_dotenv

from dimwiddle.application.protocols.config_protocol import ConfigProtocol


class EnvConfig(ConfigProtocol):
    """
    A configuration service that reads environment variables
    and falls back to values defined in a .env file.
    """

    def __init__(self, dotenv_path: Optional[str] = None, env_vars: Optional[Dict[str, str]] = None):
        """
        Initialize the Config service, optionally loading a .env file.
        
        Args:
            dotenv_path: Optional path to a .env file to load
            env_vars: Optional dictionary of environment variables to use instead of os.environ
        """
        self.env_vars = env_vars or os.environ
        
        if dotenv_path:
            # Load environment variables from dotenv_path, but do NOT override
            # existing environment variables
            load_dotenv(dotenv_path, override=False)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Return the value for environment variable `key`.
        If it's not found, return `default`.
        
        Args:
            key: The environment variable name
            default: Value to return if key is not found
            
        Returns:
            The environment variable value or default
        """
        return self.env_vars.get(key, default)

    def require(self, key: str) -> Any:
        """
        Return the value for environment variable `key`.
        Raises an error if not found.
        
        Args:
            key: The environment variable name
            
        Returns:
            The environment variable value
            
        Raises:
            ValueError: If the environment variable is not set
        """
        if key not in self.env_vars:
            raise ValueError(f"Required environment variable '{key}' is not set.")
        return self.env_vars[key]


class DictConfig(ConfigProtocol):
    """
    A configuration service that uses a dictionary for configuration values.
    """
    
    def __init__(self, config_dict: Dict[str, Any]):
        """
        Initialize with a dictionary of configuration values.
        
        Args:
            config_dict: Dictionary of configuration values
        """
        self.config = config_dict
        
    def get(self, key: str, default: Any = None) -> Any:
        """
        Return the value for key.
        If it's not found, return `default`.
        
        Args:
            key: The configuration key
            default: Value to return if key is not found
            
        Returns:
            The configuration value or default
        """
        return self.config.get(key, default)
        
    def require(self, key: str) -> Any:
        """
        Return the value for key.
        Raises an error if not found.
        
        Args:
            key: The configuration key
            
        Returns:
            The configuration value
            
        Raises:
            ValueError: If the key is not in the configuration dictionary
        """
        if key not in self.config:
            raise ValueError(f"Required configuration key '{key}' is not set.")
        return self.config[key]