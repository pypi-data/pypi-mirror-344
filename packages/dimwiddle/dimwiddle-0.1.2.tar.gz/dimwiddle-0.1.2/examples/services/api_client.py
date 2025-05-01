import requests
from typing import Dict, Any, Optional

from examples.services.logger import Logger

class APIClient:
    """
    A simple API client that demonstrates configuration injection.
    """
    
    def __init__(self, api_url: str, api_key: str, logger: Logger):
        """
        Initialize the API client.
        
        Args:
            api_url: The base URL for the API
            api_key: The API key for authentication
            logger: Logger for logging requests and responses
        """
        self.api_url = api_url
        self.api_key = api_key
        self.logger = logger
        
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the API.
        
        Args:
            endpoint: The API endpoint to call
            params: Optional query parameters
            
        Returns:
            The JSON response from the API
            
        Raises:
            requests.RequestException: If the request fails
        """
        url = f"{self.api_url}/{endpoint}"
        self.logger.info(f"Making GET request to {url}")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            raise
        
    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a POST request to the API.
        
        Args:
            endpoint: The API endpoint to call
            data: The JSON payload to send
            
        Returns:
            The JSON response from the API
            
        Raises:
            requests.RequestException: If the request fails
        """
        url = f"{self.api_url}/{endpoint}"
        self.logger.info(f"Making POST request to {url}")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            raise