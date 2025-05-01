"""
Dimwiddle: A lightweight dependency injection framework for Python.

This package provides a clean, YAML-based dependency injection container
inspired by the Symfony Framework.
"""

try:
    from ._version import __version__
except ImportError:
    __version__ = "0.0.0"  # Fallback version when not installed from package

# Import commonly used classes for easier access
from dimwiddle.domain.container import Container
from dimwiddle.domain.service_definition import ServiceDefinition
from dimwiddle.application.load_definitions import create_container_from_yaml, load_definitions_from_yaml
from dimwiddle.infrastructure.config import EnvConfig, DictConfig
from dimwiddle.infrastructure.tagged_iterator import TaggedIterator, register_tagged_iterator

# Initialize YAML constructor for TaggedIterator
register_tagged_iterator()