#!/usr/bin/env python3
"""
Example usage of the Dimwiddle dependency injection container.

This script demonstrates how to load and use services defined in YAML.
"""

import os
import sys
from pathlib import Path

# Add project root to path to allow imports during development
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dimwiddle import create_container_from_yaml, DictConfig


def main():
    """Run the example demonstration."""
    # Path to the services file
    services_file = os.path.join(project_root, "examples", "services.yaml")
    
    # For this example, we'll use a Dictionary config to simulate environment variables
    # In a real application, you might use EnvConfig with a .env file
    config = DictConfig({
        "NAME": "World",
        "API_URL": "https://api.example.com",
        "API_KEY": "secret-api-key",
        "LOG_LEVEL": "info"
    })
    
    # Create the container
    print(f"Loading services from {services_file}...\n")
    container = create_container_from_yaml(services_file, config=config)
    
    # Use the greeting service directly
    greeting_service = container.get("greeting")
    print(f"Greeting service: {greeting_service.greet('Direct User')}")
    
    # Use the greeter service which depends on the greeting service
    greeter = container.get("greeter")
    print(f"Greeter service: {greeter.greet_user('Dependency User')}")
    
    # Use the validation service with tagged validators
    validation_service = container.get("validation_service")
    
    # Test the validators
    test_email = "user@example.com"
    is_valid_email = validation_service.validate("email", test_email)
    print(f"Email '{test_email}' is {'valid' if is_valid_email else 'invalid'}")
    
    test_url = "https://example.com"
    is_valid_url = validation_service.validate("url", test_url)
    print(f"URL '{test_url}' is {'valid' if is_valid_url else 'invalid'}")
    
    # Use the factory-created complex service
    complex_service = container.get("complex_service")
    data = complex_service.get_data("resource-123")
    print(f"Complex service data: {data}")
    
    # Use the API client
    api_client = container.get("api_client")
    print(f"API client configured for: {api_client.api_url}")
    
    print("\nAll services loaded and used successfully!")


if __name__ == "__main__":
    main()