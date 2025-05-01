import os
import unittest
import tempfile

from dimwiddle.application.protocols.yaml_loader_protocol import YamlLoaderProtocol
from dimwiddle.infrastructure.yaml_loader import YamlLoader


class TestYamlLoader(unittest.TestCase):
    """Test the YAML loader implementation."""
    
    def setUp(self):
        """Set up a temporary YAML file for testing."""
        self.loader = YamlLoader()
        
        # Create a temporary test file
        self.test_yaml_content = """
top_level:
  nested:
    key1: value1
    key2: value2
  list:
    - item1
    - item2
array:
  - name: obj1
    value: 1
  - name: obj2
    value: 2
"""
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".yaml", delete=False)
        self.temp_file.write(self.test_yaml_content.encode('utf-8'))
        self.temp_file.close()
        
    def tearDown(self):
        """Clean up the temporary file."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_load_entire_yaml(self):
        """Test loading the entire YAML file."""
        result = self.loader.load_yaml(self.temp_file.name)
        
        # Verify the structure matches what we expect
        self.assertIn('top_level', result)
        self.assertIn('nested', result['top_level'])
        self.assertEqual(result['top_level']['nested']['key1'], 'value1')
        self.assertEqual(result['top_level']['nested']['key2'], 'value2')
        self.assertEqual(result['top_level']['list'], ['item1', 'item2'])
        
    def test_load_with_string_subpath(self):
        """Test loading a subpath as a string."""
        result = self.loader.load_yaml(self.temp_file.name, 'top_level')
        
        # Verify we got just the top_level section
        self.assertIn('nested', result)
        self.assertIn('list', result)
        
    def test_load_with_list_subpath(self):
        """Test loading a subpath as a list."""
        result = self.loader.load_yaml(self.temp_file.name, ['top_level', 'nested'])
        
        # Verify we got just the nested section
        self.assertEqual(result['key1'], 'value1')
        self.assertEqual(result['key2'], 'value2')
        
    def test_nonexistent_subpath(self):
        """Test loading a nonexistent subpath returns None."""
        result = self.loader.load_yaml(self.temp_file.name, 'nonexistent')
        self.assertIsNone(result)
        
    def test_invalid_file_type(self):
        """Test that loading a non-YAML file raises ValueError."""
        with tempfile.NamedTemporaryFile(suffix=".txt") as temp_txt:
            with self.assertRaises(ValueError):
                self.loader.load_yaml(temp_txt.name)
                
    def test_invalid_subpath_type(self):
        """Test that an invalid subpath type raises ValueError."""
        with self.assertRaises(ValueError):
            self.loader.load_yaml(self.temp_file.name, 123)  # Integer is invalid


if __name__ == "__main__":
    unittest.main()