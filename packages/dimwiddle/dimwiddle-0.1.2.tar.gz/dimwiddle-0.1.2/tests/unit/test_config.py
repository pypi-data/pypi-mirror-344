import os
import unittest
from unittest.mock import patch

from dimwiddle.application.protocols.config_protocol import ConfigProtocol
from dimwiddle.infrastructure.config import EnvConfig, DictConfig


class TestDictConfig(unittest.TestCase):
    """Test the DictConfig implementation."""
    
    def setUp(self):
        """Set up a DictConfig with test values."""
        self.config_dict = {
            "KEY1": "value1",
            "KEY2": "value2",
            "EMPTY_KEY": ""
        }
        self.config = DictConfig(self.config_dict)
    
    def test_get_existing_key(self):
        """Test getting an existing key."""
        self.assertEqual(self.config.get("KEY1"), "value1")
        self.assertEqual(self.config.get("KEY2"), "value2")
    
    def test_get_nonexistent_key(self):
        """Test getting a nonexistent key with default value."""
        self.assertIsNone(self.config.get("NONEXISTENT"))
        self.assertEqual(self.config.get("NONEXISTENT", "default"), "default")
    
    def test_require_existing_key(self):
        """Test requiring an existing key."""
        self.assertEqual(self.config.require("KEY1"), "value1")
    
    def test_require_nonexistent_key(self):
        """Test requiring a nonexistent key raises ValueError."""
        with self.assertRaises(ValueError):
            self.config.require("NONEXISTENT")
            
    def test_empty_value(self):
        """Test that an empty string value is not treated as missing."""
        self.assertEqual(self.config.get("EMPTY_KEY"), "")
        self.assertEqual(self.config.require("EMPTY_KEY"), "")


class TestEnvConfig(unittest.TestCase):
    """Test the EnvConfig implementation."""
    
    def setUp(self):
        """Set up an EnvConfig with test environment variables."""
        self.env_vars = {
            "TEST_KEY1": "test_value1",
            "TEST_KEY2": "test_value2",
            "TEST_EMPTY": ""
        }
        # Create config with mock env vars instead of actual environment
        self.config = EnvConfig(env_vars=self.env_vars)
    
    def test_get_existing_key(self):
        """Test getting an existing environment variable."""
        self.assertEqual(self.config.get("TEST_KEY1"), "test_value1")
        self.assertEqual(self.config.get("TEST_KEY2"), "test_value2")
    
    def test_get_nonexistent_key(self):
        """Test getting a nonexistent environment variable with default value."""
        self.assertIsNone(self.config.get("NONEXISTENT"))
        self.assertEqual(self.config.get("NONEXISTENT", "default"), "default")
    
    def test_require_existing_key(self):
        """Test requiring an existing environment variable."""
        self.assertEqual(self.config.require("TEST_KEY1"), "test_value1")
    
    def test_require_nonexistent_key(self):
        """Test requiring a nonexistent environment variable raises ValueError."""
        with self.assertRaises(ValueError):
            self.config.require("NONEXISTENT")
    
    def test_empty_value(self):
        """Test that an empty environment variable is not treated as missing."""
        self.assertEqual(self.config.get("TEST_EMPTY"), "")
        self.assertEqual(self.config.require("TEST_EMPTY"), "")
    
    def test_dotenv_loading(self):
        """Test that the EnvConfig loads environment variables from a .env file."""
        # Patch the load_dotenv function directly in the module
        with patch('dimwiddle.infrastructure.config.load_dotenv') as mock_load_dotenv:
            # Create config with dotenv_path
            EnvConfig(dotenv_path="/path/to/.env")
            
            # Verify load_dotenv was called with the correct arguments
            mock_load_dotenv.assert_called_once_with("/path/to/.env", override=False)


if __name__ == "__main__":
    unittest.main()