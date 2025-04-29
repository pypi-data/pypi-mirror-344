import unittest
from pythils.config import ConfigRef, ConfigDict

class TestConfigRef(unittest.TestCase):
    def setUp(self):
        # Setup config objects for testing
        self.root_config = ConfigDict({
            'root_key': 'root_value',
            'child_config' : {
                'child_key': 'child_value'
            }
        })
        
        self.child_config = self.root_config['child_config']

    def test_init(self):
        # Test initialization
        ref = ConfigRef('test_key')
        self.assertEqual(ref.key, 'test_key')

    def test_repr(self):
        # Test string representation
        ref = ConfigRef('test_key')
        self.assertEqual(repr(ref), 'ConfigRef(test_key)')

    def test_is_relative_true(self):
        # Test is_relative with a relative key
        ref = ConfigRef('.relative_key')
        self.assertTrue(ref._is_relative())

    def test_is_relative_false(self):
        # Test is_relative with an absolute key
        ref = ConfigRef('absolute_key')
        self.assertFalse(ref._is_relative())

    def test_value_relative_existing(self):
        # Test value with a relative key that exists
        self.child_config['existing_key'] = 'existing_value'
        ref = ConfigRef('.existing_key')
        self.assertEqual(ref._value(self.child_config), 'existing_value')

    def test_value_relative_non_existing_with_default(self):
        # Test value with a relative key that doesn't exist, with default
        ref = ConfigRef('.non_existing_key')
        self.assertEqual(ref._value(self.child_config, 'default_value'), 'default_value')

    def test_value_absolute_existing(self):
        # Test value with an absolute key that exists in root
        ref = ConfigRef('root_key')
        self.assertEqual(ref._value(self.child_config), 'root_value')

    def test_value_absolute_non_existing_with_default(self):
        # Test value with an absolute key that doesn't exist in root, with default
        ref = ConfigRef('non_existing_key')
        self.assertEqual(ref._value(self.child_config, 'default_value'), 'default_value')


if __name__ == '__main__':
    unittest.main()