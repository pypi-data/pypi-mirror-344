import unittest
import importlib
from inspect import Parameter, Signature
from unittest.mock import patch, MagicMock

from pythils.interface import DynamicInterface

from tests.interface_test import InterfaceTest

# Mock implementations for testing
class MockInterface(DynamicInterface):
    __implementation_package__ = "tests.mock_implementations"
    __default_implementation__ = "default_impl"

class RegularParamImplementation(MockInterface):
    def __init__(self, required_arg, optional_arg="default"):
        self.required_arg = required_arg
        self.optional_arg = optional_arg

class AllParamTypesImplementation(MockInterface):
    def __init__(self, pos_only, /, pos_or_kw, *, kw_only, **extra_kwargs):
        self.pos_only = pos_only
        self.pos_or_kw = pos_or_kw
        self.kw_only = kw_only
        self.extra_kwargs = extra_kwargs

class VarArgsImplementation(MockInterface):
    def __init__(self, first, *args, **kwargs):
        self.first = first
        self.args = args
        self.kwargs = kwargs

class TestDynamicInterface(unittest.TestCase):
    def setUp(self):
        # Create mock modules and classes for our tests
        self.mock_modules = {
            "tests.mock_implementations.default_impl": MagicMock(),
            "tests.mock_implementations.regular_impl": MagicMock(),
            "tests.mock_implementations.invalid_impl": MagicMock(),
            "tests.mock_implementations.all_param_types": MagicMock(),
            "tests.mock_implementations.var_args": MagicMock(),
        }
        
        # Configure mock modules
        self.mock_modules["tests.mock_implementations.default_impl"].MockInterface = RegularParamImplementation
        self.mock_modules["tests.mock_implementations.regular_impl"].MockInterface = RegularParamImplementation
        self.mock_modules["tests.mock_implementations.invalid_impl"].__implementation__ = "NonExistentClass"
        self.mock_modules["tests.mock_implementations.all_param_types"].MockInterface = AllParamTypesImplementation
        self.mock_modules["tests.mock_implementations.var_args"].MockInterface = VarArgsImplementation
        
        # Save the real import_module to restore later
        self.real_import_module = importlib.import_module
        
        # Replace import_module with our mock version
        def mock_import_module(name, package=None):
            if name.startswith("."):
                full_name = f"{package}{name}"
            else:
                full_name = name
                
            if full_name in self.mock_modules:
                return self.mock_modules[full_name]
            
            if name == "tests.mock_implementations.nonexistent":
                raise ImportError("No module named 'nonexistent'")
                
            return self.real_import_module(name, package)
            
        importlib.import_module = mock_import_module
        
    def tearDown(self):
        # Restore the real import_module
        importlib.import_module = self.real_import_module

    def test_get_implementation_no_default_no_provided(self):
        # Create a subclass with no default implementation
        class NoDefaultInterface(DynamicInterface):
            __implementation_package__ = "tests.mock_implementations"
            __default_implementation__ = None
            
        with self.assertRaises(ValueError) as cm:
            NoDefaultInterface.get_implementation()
        self.assertIn("No implementation provided for NoDefaultInterface", str(cm.exception))
    
    def test_get_implementation_default(self):
        impl_class = MockInterface.get_implementation()
        self.assertEqual(impl_class, RegularParamImplementation)
    
    def test_get_implementation_provided(self):
        impl_class = MockInterface.get_implementation("regular_impl")
        self.assertEqual(impl_class, RegularParamImplementation)
    
    def test_get_implementation_import_error(self):
        with self.assertRaises(ImportError) as cm:
            InterfaceTest.get_implementation("nonexistent")
        self.assertIn("Could not import module", str(cm.exception))
    
    def test_get_implementation_attribute_error(self):
        with self.assertRaises(AttributeError) as cm:
            InterfaceTest.get_implementation("invalid_impl")
        self.assertIn("does not have class NonExistentClass", str(cm.exception))
    
    @patch('pythils.interface.signature')
    def test_get_init_parameters(self, mock_signature):
        mock_signature.return_value = Signature([
            Parameter("self", Parameter.POSITIONAL_OR_KEYWORD),
            Parameter("arg1", Parameter.POSITIONAL_OR_KEYWORD),
            Parameter("arg2", Parameter.POSITIONAL_OR_KEYWORD)
        ])
        
        params = MockInterface.get_init_parameters()
        self.assertEqual(params, ["self", "arg1", "arg2"])
    
    def test_create_instance_default_impl(self):
        config = {}
        with patch.object(RegularParamImplementation, "__init__", return_value=None) as mock_init:
            instance = MockInterface.create_instance(config)
            mock_init.assert_called_once()
    
    def test_create_instance_specific_impl(self):
        config = {"implementation": "regular_impl", "regular_impl": {"required_arg": "value", "optional_arg": "custom"}}
        instance = MockInterface.create_instance(config)
        self.assertEqual(instance.required_arg, "value")
        self.assertEqual(instance.optional_arg, "custom")
    
    def test_create_instance_missing_required_arg(self):
        config = {"implementation": "regular_impl", "regular_impl": {}}
        with self.assertRaises(TypeError) as cm:
            MockInterface.create_instance(config)
        self.assertIn("Missing required arguments: required_arg", str(cm.exception))
    
    def test_create_instance_positional_only_params(self):
        config = {"implementation": "all_param_types", "all_param_types": {
            "pos_only": "pos_val", 
            "pos_or_kw": "pos_kw_val", 
            "kw_only": "kw_val",
            "extra1": "extra1_val"
        }}
        instance = MockInterface.create_instance(config)
        self.assertEqual(instance.pos_only, "pos_val")
        self.assertEqual(instance.pos_or_kw, "pos_kw_val")
        self.assertEqual(instance.kw_only, "kw_val")
        self.assertEqual(instance.extra_kwargs, {"extra1": "extra1_val"})
    
    def test_create_instance_var_args(self):
        config = {"implementation": "var_args", "var_args": {
            "first": "first_val",
            "args": [1, 2, 3],
            "kwargs": {"k1": "v1", "k2": "v2"},
            "extra": "extra_val"
        }}
        instance = MockInterface.create_instance(config)
        self.assertEqual(instance.first, "first_val")
        self.assertEqual(instance.args, (1, 2, 3))
        self.assertEqual(instance.kwargs, {"k1": "v1", "k2": "v2", "extra": "extra_val"})

    def test_list_implementations(self):
        implementations = InterfaceTest.get_implementations()
        self.assertIn("impl_a", implementations)
        self.assertIn("impl_b", implementations)
        self.assertNotIn("nonexistant", implementations)
    

if __name__ == "__main__":
    unittest.main()