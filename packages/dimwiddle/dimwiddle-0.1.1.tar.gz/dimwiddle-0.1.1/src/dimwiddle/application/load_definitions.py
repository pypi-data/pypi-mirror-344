import importlib
import os
import builtins
from typing import Dict, Optional, Any

from dimwiddle.infrastructure.yaml_loader import YamlLoader
from dimwiddle.domain.service_definition import ServiceDefinition

# Make sure to import tagged_iterator so its constructor is registered!
from dimwiddle.infrastructure.tagged_iterator import tagged_iterator_constructor  # noqa

def load_definitions_from_yaml(file_path: str) -> Dict[str, ServiceDefinition]:
    """
    Load service definitions from a YAML file.
    
    Args:
        file_path: Path to the YAML file containing service definitions
        
    Returns:
        Dictionary of service definitions keyed by service name
    """
    loader = YamlLoader()
    services_data = loader.load_yaml(file_path, "services") or {}
    definitions: Dict[str, ServiceDefinition] = {}

    for service_name, raw in services_data.items():
        # 'class' might be omitted if there's a factory-based definition
        cls = None
        if 'class' in raw:
            class_path = raw['class']
            
            # Special handling for built-in types
            if hasattr(builtins, class_path):
                cls = getattr(builtins, class_path)
            else:
                # Handle case where class_path might be malformed
                try:
                    mod_name, cls_name = class_path.rsplit('.', 1)
                    module = importlib.import_module(mod_name)
                    cls = getattr(module, cls_name)
                except (ValueError, ImportError, AttributeError) as e:
                    raise ValueError(f"Error loading class {class_path} for service {service_name}: {str(e)}")

        # 'factory' might look like [ '@some.factory.service', 'methodName' ]
        factory = raw.get('factory', None)

        # 'tags' is optional
        tags = raw.get('tags', [])

        # Determine if 'arguments' is a list (positional) or dict (keyword)
        arguments = raw.get('arguments', [])
        if isinstance(arguments, list):
            pos_args = arguments
            kw_args = {}
        elif isinstance(arguments, dict):
            pos_args = []
            kw_args = arguments
        else:
            raise TypeError(
                f"'arguments' for service '{service_name}' must be list or dict, got: {type(arguments)}"
            )

        definition = ServiceDefinition(
            cls=cls,
            pos_args=pos_args,
            kw_args=kw_args,
            tags=tags,
            factory=factory,
            inject_class=raw.get('inject_class', False)
        )
        definitions[service_name] = definition

    return definitions


def create_container_from_yaml(file_path: str, config=None) -> 'Container':
    """
    Create a dependency injection container from a YAML file.
    
    Args:
        file_path: Path to the YAML file containing service definitions
        config: Optional configuration object
        
    Returns:
        A configured Container instance
    """
    # Import here to avoid circular import
    from dimwiddle.domain.container import Container
    
    definitions = load_definitions_from_yaml(file_path)
    return Container(definitions, config=config, services_file_path=file_path)