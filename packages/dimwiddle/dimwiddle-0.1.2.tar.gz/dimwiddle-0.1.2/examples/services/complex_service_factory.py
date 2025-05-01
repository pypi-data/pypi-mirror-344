from typing import Dict, Any
from examples.services.complex_service import ComplexService

class ComplexServiceFactory:
    """
    Factory for creating complex service instances.
    
    This demonstrates how to use factories in the dependency injection container.
    """
    
    def create(self, api_key: str, options: Dict[str, Any]) -> ComplexService:
        """
        Create a new ComplexService instance.
        
        Args:
            api_key: API key for the service
            options: Configuration options
            
        Returns:
            A configured and connected ComplexService
        """
        # Create the service
        service = ComplexService(api_key, options)
        
        # Additional setup that can't be done in the constructor
        service.connect()
        
        return service