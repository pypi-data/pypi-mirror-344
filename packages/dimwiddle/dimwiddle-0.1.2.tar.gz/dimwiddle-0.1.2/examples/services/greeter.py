from examples.services.greeting_service import GreetingService

class Greeter:
    """
    A service that uses a GreetingService to greet users.
    
    This demonstrates service dependencies in the DI container.
    """
    
    def __init__(self, greeting_service: GreetingService):
        """
        Initialize the greeter with a greeting service.
        
        Args:
            greeting_service: The service to use for generating greetings
        """
        self.greeting_service = greeting_service
        
    def greet_user(self, user: str) -> str:
        """
        Greet a user by name.
        
        Args:
            user: The name of the user to greet
            
        Returns:
            A greeting message for the user
        """
        return self.greeting_service.greet(user)