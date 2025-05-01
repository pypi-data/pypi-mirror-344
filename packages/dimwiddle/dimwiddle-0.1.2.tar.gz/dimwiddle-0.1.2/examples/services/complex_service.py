from typing import Dict, Any

class ComplexService:
    """
    A more complex service created by a factory.
    """
    
    def __init__(self, api_key: str, options: Dict[str, Any]):
        """
        Initialize the complex service.
        
        Args:
            api_key: API key for the service
            options: Configuration options
        """
        self.api_key = api_key
        self.options = options
        self.connected = False
        
    def connect(self):
        """
        Connect to the service.
        
        Returns:
            True if successful, False otherwise
        """
        # In a real service, this would connect to an external API
        self.connected = True
        return self.connected
        
    def get_data(self, resource_id: str) -> Dict[str, Any]:
        """
        Get data from the service.
        
        Args:
            resource_id: The ID of the resource to fetch
            
        Returns:
            The resource data
            
        Raises:
            RuntimeError: If not connected
        """
        if not self.connected:
            raise RuntimeError("Must connect before getting data")
            
        # In a real service, this would fetch data from an API
        return {
            "id": resource_id,
            "status": "success",
            "data": {
                "option1": self.options.get("option1", False),
                "option2": self.options.get("option2", "")
            }
        }