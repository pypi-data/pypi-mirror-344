class GreetingService:
    """
    A simple service that provides a greeting message.
    """
    
    def __init__(self, greeting_format: str = "Hello, {name}!"):
        """
        Initialize the greeting service with a format string.
        
        Args:
            greeting_format: Format string with {name} placeholder
        """
        self.greeting_format = greeting_format
        
    def greet(self, name: str) -> str:
        """
        Generate a greeting for the given name.
        
        Args:
            name: The name to include in the greeting
            
        Returns:
            A personalized greeting string
        """
        return self.greeting_format.format(name=name)