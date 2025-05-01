import importlib
import os
from typing import Any, Dict, Optional, Set

from dimwiddle.application.protocols.config_protocol import ConfigProtocol
from dimwiddle.infrastructure.config import EnvConfig
from dimwiddle.domain.service_definition import ServiceDefinition
from dimwiddle.infrastructure.tagged_iterator import TaggedIterator


class Container:
    def __init__(self, 
                 definitions: Dict[str, ServiceDefinition], 
                 config: Optional[ConfigProtocol] = None,
                 services_file_path: Optional[str] = None):
        """
        Initialize the dependency injection container.
        
        Args:
            definitions: Dictionary of service definitions
            config: Optional configuration provider
            services_file_path: Optional path to the services YAML file for resolving references
        """
        self.definitions = definitions
        self.singletons: Dict[str, Any] = {}
        self.resolving: Set[str] = set()
        self.config = config or EnvConfig()
        self.services_file_path = services_file_path

    def get(self, service_name: str) -> Any:
        """
        Get a service from the container.
        
        Args:
            service_name: The name of the service to retrieve
            
        Returns:
            The service instance
            
        Raises:
            RuntimeError: If a circular dependency is detected
            KeyError: If no definition exists for the service
        """
        # Check if it's already instantiated
        if service_name in self.singletons:
            return self.singletons[service_name]

        # Detect circular references
        if service_name in self.resolving:
            raise RuntimeError(f"Circular dependency detected: {service_name}")
        self.resolving.add(service_name)

        definition = self.definitions.get(service_name)
        if not definition:
            self.resolving.remove(service_name)
            raise KeyError(f"No definition for service: {service_name}")

        # Resolve positional arguments
        resolved_pos_args = [self._resolve_argument(arg) for arg in definition.pos_args]

        # Resolve keyword arguments
        resolved_kw_args = {
            key: self._resolve_argument(arg)
            for key, arg in definition.kw_args.items()
        }

        # Decide how to create the instance
        if definition.factory:
            # Factory-based instantiation
            instance = self._call_factory(definition.factory, resolved_pos_args, resolved_kw_args)
        else:
            # Direct class instantiation
            if not definition.cls:
                raise ValueError(
                    f"Service '{service_name}' has no 'cls' or 'factory' defined."
                )
            if definition.inject_class:
                instance = definition.cls
            else:
                instance = definition.cls(*resolved_pos_args, **resolved_kw_args)

        self.singletons[service_name] = instance
        self.resolving.remove(service_name)

        return instance

    def _call_factory(self, factory_info, pos_args, kw_args) -> Any:
        """
        Call a factory to create a service.
        
        Args:
            factory_info: A 2-tuple/list of [factory_service_ref, factory_method_name]
            pos_args: Positional arguments to pass to the factory method
            kw_args: Keyword arguments to pass to the factory method
            
        Returns:
            The instance created by the factory
            
        Raises:
            ValueError: If the factory_info format is invalid
        """
        if not isinstance(factory_info, (list, tuple)) or len(factory_info) != 2:
            raise ValueError(f"Invalid factory format: {factory_info}")

        factory_ref, method_name = factory_info

        # If there's an '@', remove it and get that service
        if isinstance(factory_ref, str) and factory_ref.startswith('@'):
            factory_ref = factory_ref[1:]

        # Retrieve the factory service instance
        factory_service = self.get(factory_ref)

        # Call the specified method with the resolved arguments
        factory_method = getattr(factory_service, method_name)
        return factory_method(*pos_args, **kw_args)

    def _resolve_argument(self, arg: Any) -> Any:
        """
        Resolve an argument value, handling service references, environment variables,
        YAML references, etc.
        
        Args:
            arg: The argument to resolve
            
        Returns:
            The resolved argument value
        """
        # New syntax: if arg is a string that starts with "~", load YAML from file.
        if isinstance(arg, str) and arg.startswith("~"):
            return self._resolve_yaml_reference(arg)
        
        # Handle configuration variables
        if isinstance(arg, str) and arg.startswith('%') and arg.endswith('%'):
            env_var = arg[1:-1]
            return self.config.require(env_var)
        
        # Handle service references
        if isinstance(arg, str) and arg.startswith('@'):
            return self.get(arg[1:])

        # Handle tagged iterators
        if isinstance(arg, TaggedIterator):
            return self._build_tagged_collection(arg)

        # Handle dictionaries
        if isinstance(arg, dict):
            return {
                key: self._resolve_argument(value) for key, value in arg.items()
            }
        
        # Handle lists
        if isinstance(arg, list):
            return [self._resolve_argument(item) for item in arg]

        # Otherwise, it's literal
        return arg
        
    def _resolve_yaml_reference(self, arg: str) -> Any:
        """
        Resolve a YAML reference in the format "~/path/to/file.yaml:sub.path.to.definition"
        or "~path/to/file.yaml:sub.path.to.definition".
        
        Args:
            arg: The YAML reference string
            
        Returns:
            The loaded YAML content
            
        Raises:
            ValueError: If the reference format is invalid or no services_file_path is provided
        """
        # Expected format: "~/path/to/file.yaml:sub.path.to.definition"
        arg_clean = arg[2:] if arg.startswith("~/") else arg[1:]
        if ":" in arg_clean:
            file_part, subpath_str = arg_clean.split(":", 1)
            
            # If the path starts with a '/', it's an absolute path, otherwise resolve it
            # relative to the services file location
            if file_part.startswith('/'):
                file_path = file_part
            elif self.services_file_path:
                # Use the directory of the services file as the base directory
                base_dir = os.path.dirname(self.services_file_path)
                file_path = os.path.join(base_dir, file_part)
            else:
                raise ValueError(
                    "Cannot resolve relative YAML path without services_file_path."
                )
                
            subpath = subpath_str.split(".")
            
            # Dynamically import the YamlLoader to avoid circular import
            from dimwiddle.infrastructure.yaml_loader import YamlLoader
            loader = YamlLoader()
            return loader.load_yaml(file_path, subpath)
        else:
            raise ValueError("Invalid syntax for YAML loader: missing colon separator.")

    def _build_tagged_collection(self, tagged_iter: TaggedIterator) -> Dict[str, Any]:
        """
        Build a collection of services that have a specific tag.
        
        Args:
            tagged_iter: A TaggedIterator instance with tag and index_by properties
            
        Returns:
            A dictionary of services with the specified tag
        """
        result = {}
        for service_name, definition in self.definitions.items():
            for tag_obj in definition.tags:
                if tag_obj.get("name") == tagged_iter.tag:
                    key_for_dict = tag_obj.get(tagged_iter.index_by, service_name)
                    result[key_for_dict] = self.get(service_name)
        return result