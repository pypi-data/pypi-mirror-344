import os
import unittest
from typing import Dict, List

from dimwiddle.domain.service_definition import ServiceDefinition
from dimwiddle.domain.container import Container
from dimwiddle.application.load_definitions import load_definitions_from_yaml, create_container_from_yaml
from dimwiddle.infrastructure.config import DictConfig


# Simple test classes for DI container tests
class SampleService:
    def __init__(self, message: str = "Hello"):
        self.message = message
    
    def get_message(self) -> str:
        return self.message


class ServiceFactory:
    def create(self, message: str) -> SampleService:
        return SampleService(message)


class ContainerTest(unittest.TestCase):
    def test_get_service(self):
        # Create service definitions manually
        definitions = {
            "test_service": ServiceDefinition(
                cls=SampleService,
                pos_args=["Hello, World!"]
            )
        }
        
        # Create container
        container = Container(definitions)
        
        # Get the service
        service = container.get("test_service")
        
        # Assertions
        self.assertIsInstance(service, SampleService)
        self.assertEqual(service.get_message(), "Hello, World!")
        
    def test_service_with_dependency(self):
        # Create service definitions with a dependency
        definitions = {
            "message": ServiceDefinition(
                cls=str,
                pos_args=["Dependency Injection Works!"]
            ),
            "test_service": ServiceDefinition(
                cls=SampleService,
                pos_args=["@message"]
            )
        }
        
        # Create container
        container = Container(definitions)
        
        # Get the service
        service = container.get("test_service")
        
        # Assertions
        self.assertIsInstance(service, SampleService)
        self.assertEqual(service.get_message(), "Dependency Injection Works!")
        
    def test_service_with_factory(self):
        # Create service definitions with a factory
        definitions = {
            "factory": ServiceDefinition(
                cls=ServiceFactory
            ),
            "test_service": ServiceDefinition(
                factory=["@factory", "create"],
                pos_args=["Factory Created Service"]
            )
        }
        
        # Create container
        container = Container(definitions)
        
        # Get the service
        service = container.get("test_service")
        
        # Assertions
        self.assertIsInstance(service, SampleService)
        self.assertEqual(service.get_message(), "Factory Created Service")
        
    def test_service_with_config(self):
        # Create simple config
        config = DictConfig({
            "MESSAGE": "Config Works!"
        })
        
        # Create service definitions with config reference
        definitions = {
            "test_service": ServiceDefinition(
                cls=SampleService,
                pos_args=["%MESSAGE%"]
            )
        }
        
        # Create container with config
        container = Container(definitions, config=config)
        
        # Get the service
        service = container.get("test_service")
        
        # Assertions
        self.assertIsInstance(service, SampleService)
        self.assertEqual(service.get_message(), "Config Works!")
        
    def test_tagged_services(self):
        # Create a test YAML file for tagged services
        test_yaml_content = """
services:
  test_service_1:
    class: tests.unit.test_container.SampleService
    arguments: ["Service 1"]
    tags:
      - { name: test_tag, alias: service1 }
      
  test_service_2:
    class: tests.unit.test_container.SampleService
    arguments: ["Service 2"]
    tags:
      - { name: test_tag, alias: service2 }
      
  registry:
    class: dict
    arguments:
      services: !tagged_iterator { tag: test_tag, index_by: alias }
"""
        # Write the YAML to a temp file
        test_yaml_path = os.path.join(os.getcwd(), "tests/unit/test_services.yaml")
        os.makedirs(os.path.dirname(test_yaml_path), exist_ok=True)
        with open(test_yaml_path, "w") as f:
            f.write(test_yaml_content)
            
        try:
            # Import here to avoid potential import issues
            import yaml
            from dimwiddle.infrastructure.tagged_iterator import tagged_iterator_constructor
            
            # Ensure the tagged_iterator constructor is registered
            yaml.SafeLoader.add_constructor('!tagged_iterator', tagged_iterator_constructor)
            
            # Load the container from the YAML
            container = create_container_from_yaml(test_yaml_path)
            
            # Get the registry
            registry = container.get("registry")
            
            # Assertions for the registry
            self.assertIsInstance(registry, dict)
            self.assertIn('services', registry)
            
            # Get the tagged services
            tagged_services = registry['services']
            self.assertEqual(len(tagged_services), 2)
            self.assertIn("service1", tagged_services)
            self.assertIn("service2", tagged_services)
            self.assertEqual(tagged_services["service1"].get_message(), "Service 1")
            self.assertEqual(tagged_services["service2"].get_message(), "Service 2")
        finally:
            # Clean up
            if os.path.exists(test_yaml_path):
                os.remove(test_yaml_path)


if __name__ == "__main__":
    unittest.main()