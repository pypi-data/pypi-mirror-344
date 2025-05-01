import os
import unittest
import tempfile
from typing import Dict, Any

from dimwiddle.domain.container import Container
from dimwiddle.domain.service_definition import ServiceDefinition
from dimwiddle.application.load_definitions import create_container_from_yaml
from dimwiddle.infrastructure.config import DictConfig


class SimpleService:
    def __init__(self, value: str):
        self.value = value
        
    def get_value(self) -> str:
        return self.value


class ServiceWithDependency:
    def __init__(self, simple_service: SimpleService, prefix: str = "Result: "):
        self.simple_service = simple_service
        self.prefix = prefix
        
    def get_result(self) -> str:
        return f"{self.prefix}{self.simple_service.get_value()}"


class IntegrationTest(unittest.TestCase):
    """Test that all components work together correctly."""
    
    def test_end_to_end_container_usage(self):
        """Test the entire flow from YAML to service usage."""
        # Create a test YAML file
        test_yaml = """
services:
  config:
    class: dimwiddle.infrastructure.config.DictConfig
    arguments:
      config_dict: 
        KEY1: "config_value1"
        KEY2: "config_value2"
  
  simple:
    class: tests.integration.test_integration.SimpleService
    arguments: ["%KEY1%"]
    
  with_dependency:
    class: tests.integration.test_integration.ServiceWithDependency
    arguments: ["@simple", "%KEY2%"]
"""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp_file:
            temp_file.write(test_yaml.encode('utf-8'))
            temp_file_path = temp_file.name
            
        try:
            # Test with config from dictionary
            config = DictConfig({"KEY1": "value1", "KEY2": "Prefix: "})
            
            # Create the container
            container = create_container_from_yaml(temp_file_path, config=config)
            
            # Get and test the service with dependency
            service = container.get("with_dependency")
            self.assertEqual(service.get_result(), "Prefix: value1")
            
        finally:
            # Clean up
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)


if __name__ == "__main__":
    unittest.main()