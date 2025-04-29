import unittest
import os
import tempfile
import json
from pythils.config import ConfigDict, ConfigRef

class TestConfigDict(unittest.TestCase):
    def setUp(self):
        # Setup basic config objects for testing
        self.empty_config = ConfigDict()
        self.simple_config = ConfigDict({
            'key1': 'value1',
            'key2': 'value2',
            'nested': {
                'key3': 'value3',
                'key4': 'value4'
            }
        })
        
        # Setup parent-child relationship
        self.parent_config = ConfigDict({
            'parent_key': 'parent_value',
            'child': {
                'child_key': 'child_value'
            },
            '*': {
                'wildcard_key': 'wildcard_value'
            }
        })
        self.child_config: ConfigDict = self.parent_config['child']
        
        # Setup config with references
        self.ref_config = ConfigDict({
            'base_key': 'base_value',
            'ref_key': ConfigRef('base_key'),
            'dot_ref': {
                'dot_key': 'dot_value'
            },
            'wild_ref': {
                'wild_key': 'wild_value',
            },
            '*': ConfigRef('wild_ref'),
            'nested': {
                '.': ConfigRef('dot_ref'),
                'nested_key': 'nested_value',
                'ref_to_parent': ConfigRef('..base_key'),
                'ref_to_self': ConfigRef('.nested_key'),
                'ref_to_root': ConfigRef('base_key')
            }
        })
        
        # Setup config with dot wildcard
        self.dot_wildcard_config = ConfigDict({
            '.': {
                'default_key': 'default_value'
            },
            'specific': 'specific_value'
        })

    # Initialization tests
    def test_init_empty(self):
        config = ConfigDict()
        self.assertEqual(config.config_dict, {})
        self.assertEqual(config.parent, config)
        self.assertEqual(config.root, config)

    def test_init_with_dict(self):
        test_dict = {'a': 1, 'b': 2}
        config = ConfigDict(test_dict)
        self.assertEqual(config.config_dict, test_dict)
        # Test copy behavior
        test_dict['c'] = 3
        self.assertNotIn('c', config.config_dict)

    def test_init_with_parent(self):
        parent = ConfigDict({'parent_key': 'parent_value'})
        child = ConfigDict({'child_key': 'child_value'}, parent=parent)
        self.assertEqual(child.parent, parent)
        self.assertEqual(child.root, parent)

    def test_init_without_copy(self):
        test_dict = {'a': 1, 'b': 2}
        config = ConfigDict(test_dict, copy=False)
        test_dict['c'] = 3
        self.assertIn('c', config.config_dict)

    # get method tests
    def test_get_simple_key(self):
        self.assertEqual(self.simple_config.get('key1'), 'value1')
        self.assertEqual(self.simple_config.get('key2'), 'value2')

    def test_get_nested_key(self):
        self.assertEqual(self.simple_config.get('nested.key3'), 'value3')
        self.assertEqual(self.simple_config.get('nested.key4'), 'value4')

    def test_get_missing_key(self):
        self.assertIsNone(self.simple_config.get('nonexistent'))
        self.assertEqual(self.simple_config.get('nonexistent', 'default'), 'default')

    def test_get_parent_navigation(self):
        self.assertEqual(self.child_config.get('..parent_key'), 'parent_value')
        self.assertEqual(self.child_config.get('parent_key'), None)

    def test_get_dot_prefix(self):
        nested_config = self.simple_config['nested']
        self.assertEqual(nested_config.get('.key3'), 'value3')

    def test_get_config_ref(self):
        self.assertEqual(self.ref_config.get('ref_key'), 'base_value')
        self.assertEqual(self.ref_config.get('nested.dot_key'), 'dot_value')
        self.assertEqual(self.ref_config.get('nested.wild_key'), 'wild_value')
        self.assertEqual(self.ref_config.get('inexistant.wild_key'), 'wild_value')
        self.assertEqual(self.ref_config.get('nested.ref_to_parent'), 'base_value')
        self.assertEqual(self.ref_config.get('nested.ref_to_self'), 'nested_value')
        self.assertEqual(self.ref_config.get('nested.ref_to_root'), 'base_value')

    def test_get_wildcard(self):
        # Test * wildcard
        self.assertEqual(self.child_config.get('wildcard_key'), 'wildcard_value')
        self.assertEqual(self.parent_config.get('inexistant.wildcard_key'), 'wildcard_value')
        
        # Test . wildcard
        self.assertEqual(self.dot_wildcard_config.get('default_key'), 'default_value')
        self.assertEqual(self.dot_wildcard_config.get('specific'), 'specific_value')
        self.assertEqual(self.dot_wildcard_config.get('missing', 'missing'), 'missing')

    # set method tests
    def test_set_simple_key(self):
        config = ConfigDict()
        config.set('key', 'value')
        self.assertEqual(config.get('key'), 'value')

    def test_set_nested_key(self):
        config = ConfigDict()
        config.set('nested.key', 'value')
        self.assertEqual(config.get('nested.key'), 'value')
        self.assertIsInstance(config.config_dict['nested'], dict)

    def test_set_parent_navigation(self):
        parent = ConfigDict({'key': 'old_value'})
        child = ConfigDict({}, parent=parent)
        child.set('..key', 'new_value')
        self.assertEqual(parent.get('key'), 'new_value')

    def test_set_dot_prefix(self):
        config = ConfigDict({'nested': {}})
        nested = config['nested']
        nested.set('.key', 'value')
        self.assertEqual(nested.get('key'), 'value')

    # Special methods tests
    def test_contains(self):
        self.assertIn('key1', self.simple_config)
        self.assertIn('nested.key3', self.simple_config)
        self.assertNotIn('nonexistent', self.simple_config)

    def test_getitem(self):
        self.assertEqual(self.simple_config['key1'], 'value1')
        self.assertEqual(self.simple_config['nested']['key3'], 'value3')
        with self.assertRaises(KeyError):
            _ = self.simple_config['nonexistent']

    def test_setitem(self):
        config = ConfigDict()
        config['key'] = 'value'
        self.assertEqual(config.get('key'), 'value')
        config['nested.key'] = 'nested_value'
        self.assertEqual(config.get('nested.key'), 'nested_value')

    def test_len(self):
        self.assertEqual(len(self.empty_config), 0)
        self.assertEqual(len(self.simple_config), 3)  # key1, key2, nested

    def test_iter(self):
        keys = list(self.simple_config)
        self.assertEqual(set(keys), {'key1', 'key2', 'nested'})

    def test_repr(self):
        self.assertEqual(repr(self.empty_config), "ConfigDict({})")
        self.assertTrue(repr(self.simple_config).startswith("ConfigDict("))

    # Utility methods tests
    def test_clear(self):
        config = ConfigDict({'key': 'value'})
        config.clear()
        self.assertEqual(len(config), 0)

    def test_copy(self):
        copy = self.simple_config.copy()
        self.assertEqual(copy.config_dict, self.simple_config.config_dict)
        self.assertIsNot(copy.config_dict, self.simple_config.config_dict)
        self.assertEqual(copy.parent, self.simple_config.parent)

    def test_walk(self):
        items = list(self.simple_config.walk())
        expected = [
            ('key1', 'value1'),
            ('key2', 'value2'),
            ('nested.key3', 'value3'),
            ('nested.key4', 'value4')
        ]
        self.assertEqual(sorted(items), sorted(expected))

    def test_keys(self):
        # Non-recursive
        self.assertEqual(set(self.simple_config.keys()), {'key1', 'key2', 'nested'})
        
        # Recursive
        self.assertEqual(
            set(self.simple_config.keys(recursive=True)),
            {'key1', 'key2', 'nested.key3', 'nested.key4'}
        )

    def test_items(self):
        # Non-recursive
        items = self.simple_config.items()
        self.assertEqual(len(items), 3)
        
        # Recursive
        items = self.simple_config.items(recursive=True)
        self.assertEqual(len(items), 4)

    def test_values(self):
        # Non-recursive
        values = self.simple_config.values()
        self.assertEqual(len(values), 3)
        self.assertIn('value1', values)
        self.assertIn('value2', values)
        
        # Recursive
        values = self.simple_config.values(recursive=True)
        self.assertEqual(len(values), 4)
        self.assertIn('value3', values)
        self.assertIn('value4', values)

    # Update method tests
    def test_update_simple(self):
        config = ConfigDict({'a': 1, 'b': 2})
        config.update({'b': 3, 'c': 4})
        self.assertEqual(config.get('a'), 1)
        self.assertEqual(config.get('b'), 3)
        self.assertEqual(config.get('c'), 4)

    def test_update_flat(self):
        config = ConfigDict({'a': 1, 'nested': {'b': 2}})
        config.update({'nested.b': 3, 'nested.c': 4}, mode='flat')
        self.assertEqual(config.get('nested.b'), 3)
        self.assertEqual(config.get('nested.c'), 4)

    def test_update_recursive(self):
        config = ConfigDict({'a': 1, 'nested': {'b': 2}})
        config.update({'nested': {'c': 3}}, mode='recursive')
        self.assertEqual(config.get('nested.b'), 2)  # Preserved
        self.assertEqual(config.get('nested.c'), 3)  # Added

    # Static methods tests
    def test_from_env(self):
        os.environ['TEST_KEY1'] = 'value1'
        os.environ['TEST_NESTED__KEY2'] = 'value2'
        config = ConfigDict.from_env('TEST_')
        self.assertEqual(config.get('KEY1'), 'value1')
        self.assertEqual(config.get('NESTED.KEY2'), 'value2')
        # Clean up
        del os.environ['TEST_KEY1']
        del os.environ['TEST_NESTED__KEY2']

    def test_from_file_json(self):
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            content = json.dumps({'key': 'value', 'nested': {'key2': 'value2'}})
            f.write(content.encode('utf-8'))
            f.flush()
            path = f.name
        
        try:
            config = ConfigDict.from_file(path)
            self.assertEqual(config.get('key'), 'value')
            self.assertEqual(config.get('nested.key2'), 'value2')
        finally:
            os.unlink(path)


if __name__ == '__main__':
    unittest.main()