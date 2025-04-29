from abc import ABCMeta, abstractmethod
import importlib
from inspect import signature
from typing import Any, Dict, List, Type, TypeVar
import pkgutil  # Add this import

T = TypeVar("T", bound="DynamicInterface")

class DynamicInterface(metaclass=ABCMeta):
    """Helper class that provides a standard way to create an Interface using
    inheritance.
    """
    __slots__ = ()

    # Interfaces should redefine these attributes.
    ## The package where the implementations are located.
    __implementation_package__: str = None
    ## The default implementation to use if none is provided.
    __default_implementation__: str = None

    @classmethod
    def get_implementation(cls: Type['T'], implementation: str = None) -> Type['T']:
        """Get the implementation of the interface."""
        if implementation is None and cls.__default_implementation__ is None:
            raise ValueError(f"No implementation provided for {cls.__name__}")
        
        implementation = implementation or cls.__default_implementation__
        try:
            module = importlib.import_module("."+implementation, cls.__implementation_package__)
        except Exception as e:
            raise ImportError(f"Could not import module {cls.__implementation_package__}.{implementation}: {e}") from None
        
        class_name = getattr(module, "__implementation__", cls.__name__)
        try:
            impl_class = getattr(module, class_name)
        except AttributeError as e:
            raise AttributeError(f"Module {cls.__implementation_package__}.{implementation} does not have class {class_name}: {e}") from None
        
        if not issubclass(impl_class, cls):
            raise TypeError(f"{impl_class.__name__} is not a subclass of {cls.__name__}")
        
        return impl_class
    
    @classmethod
    def get_implementations(cls: Type['T']) -> List[str]:
        """Get the list of available implementations."""
        if cls.__implementation_package__ is None:
            return []
        
        try:
            implementation_package = importlib.import_module(cls.__implementation_package__)
            return [name for _, name, ispkg in pkgutil.iter_modules(implementation_package.__path__) 
                   if not ispkg]
        except ImportError:
            return []

    @classmethod
    def get_init_parameters(cls: Type['T']) -> List[str]:
        """Get the initialization arguments for the interface."""
        return list(signature(cls).parameters.keys())
    
    @classmethod
    def create_instance(cls: Type['T'], config_dict: Dict[str,Any] = {}, **kwargs) -> 'T':
        """Create an instance of the interface."""

        if len(config_dict) == 0:
            config_dict = kwargs
        
        implementation = config_dict.get("implementation", cls.__default_implementation__)
        cls = cls.get_implementation(implementation)

        params_dict = config_dict.get(implementation, config_dict).copy()
        args = []
        kwargs = {}
        positional_missing = []
        for name, param in signature(cls).parameters.items():
            if param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD):
                if name in params_dict:
                    args.append(params_dict.pop(name))
                else:
                    positional_missing.append(name)
            elif param.kind == param.VAR_POSITIONAL:
                if name in params_dict:
                    args.extend(params_dict.pop(name))
            elif param.kind == param.KEYWORD_ONLY:
                if param.default is not param.empty:
                    kwargs[name] = params_dict.pop(name, param.default)
                elif name in params_dict:
                    kwargs[name] = params_dict.pop(name)
                else:
                    positional_missing.append(name)
            else: # if param.kind == param.VAR_KEYWORD:
                kwargs.update(params_dict.pop(name, {}))
                kwargs.update(params_dict)
        
        if positional_missing:
            raise TypeError(f"Missing required arguments: {', '.join(positional_missing)}")
        
        return cls(*args, **kwargs)

