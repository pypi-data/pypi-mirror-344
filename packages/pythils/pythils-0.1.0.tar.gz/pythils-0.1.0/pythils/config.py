from typing import Any, Dict, Literal, Optional
from .placeholder import Placeholder, AttributePlaceholder

class ConfigRef(Placeholder):
    """
    This class is used to provide a default value based on an other key for configuration.
    """
    __slots__ = ("key",)
    __add__ = AttributePlaceholder("__add__")
    __sub__ = AttributePlaceholder("__sub__")
    __mul__ = AttributePlaceholder("__mul__")
    __truediv__ = AttributePlaceholder("__truediv__")
    __floordiv__ = AttributePlaceholder("__floordiv__")
    __mod__ = AttributePlaceholder("__mod__")
    __pow__ = AttributePlaceholder("__pow__")
    __and__ = AttributePlaceholder("__and__")
    __or__ = AttributePlaceholder("__or__")
    __xor__ = AttributePlaceholder("__xor__")
    __lt__ = AttributePlaceholder("__lt__")
    __le__ = AttributePlaceholder("__le__")
    __eq__ = AttributePlaceholder("__eq__")
    __ne__ = AttributePlaceholder("__ne__")
    __gt__ = AttributePlaceholder("__gt__")
    __ge__ = AttributePlaceholder("__ge__")
    __contains__ = AttributePlaceholder("__contains__")
    __getitem__ = AttributePlaceholder("__getitem__")

    def __init__(self, key: str):
        self.key = key

    def __repr__(self) -> str:
        return f"ConfigRef({self.key})"

    def _is_relative(self) -> bool:
        """
        Check if the reference is relative.
        """
        return self.key.startswith(".")
    
    def _value(self, config: 'ConfigDict', default: Any = None) -> Any:
        """
        Get the value of the reference.
        """
        if self._is_relative():
            return config.get(self.key, default)
        else:
            return config.root.get(self.key, default)


class ConfigDict:
    """
    Configuration management for the application.
    This module provides functions to get, set, and update configuration values,
    to load from a file, and to save to a file.
    """
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None, parent: Optional['ConfigDict'] = None, copy: bool = True) -> None:
        if copy and config_dict:
            self.config_dict = config_dict.copy()
        else:
            self.config_dict = config_dict or {}

        if parent:
            self.parent = parent
            self.root = parent.root
        else:
            self.parent = self.root = self
        
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Get the value of a configuration key.
        If the key does not exist, return the default.
        """
        config = self

        while key.startswith(".."):
            config = config.parent
            key = key[1:]
        if key.startswith("."):
            key = key[1:]

        parts = key.lower().replace("__", ".").split(".")
        not_found = object()
        for i, part in enumerate(parts):
            value = config.config_dict.get(part, not_found)

            if isinstance(value, Placeholder):
                value = value._value(config, not_found)
            
            if value is not_found:
                if "." in config.config_dict:
                    wildcard = config.config_dict["."]
                    if isinstance(wildcard, Placeholder):
                        wildcard = wildcard._value(config, {})
                    elif isinstance(wildcard, dict):
                        wildcard = ConfigDict(wildcard, config.parent, copy=False)

                    value = wildcard.get(part, not_found)
                    if isinstance(value, Placeholder):
                        value = value._value(config, not_found)
                elif self.parent is not self and "*" in config.parent.config_dict:
                    wildcard = config.parent.config_dict["*"]
                    if isinstance(wildcard, Placeholder):
                        wildcard = wildcard._value(config, {})
                    value = wildcard.get(part, not_found)

                    if isinstance(value, Placeholder):
                        value = value._value(config, not_found)
            
            if value is not_found:
                if "*" in self.config_dict:
                    value = self.config_dict["*"]
                    if isinstance(value, Placeholder):
                        value = value._value(config, value)
                    if isinstance(value, dict):
                        value = ConfigDict(value, config, copy=True)
                else:
                    return default

            if isinstance(value, dict):
                value = ConfigDict(value, config, copy=False)
            if isinstance(value, ConfigDict):
                config = value
            elif i < len(parts) - 1:
                # si la valeur n'est pas un dict, on ne peut pas descendre plus bas
                return default
        
        return value
    
    def set(self, key:str, value:Any) -> None:
        """
        Set the value of a configuration key.
        If the key already exists, update its value.
        """
        while key.startswith(".."):
            self = self.parent
            key = key[1:]
        if key.startswith("."):
            key = key[1:]

        parts = key.lower().replace("__", ".").split(".")
        _config = self.config_dict
        for part in parts[:-1]:
            if part not in _config or not isinstance(_config[part], dict):
                _config[part] = {}
            _config = _config[part]
        _config[parts[-1]] = value

    def __contains__(self, key: str) -> bool:
        """
        Check if the configuration contains a key.
        """
        not_found = object()
        return self.get(key, not_found) is not not_found
    
    def __getitem__(self, key: str) -> Any:
        """
        Get the value of a configuration key.
        """
        not_found = object()
        result = self.get(key, not_found)
        if result is not not_found:
            return result
        raise KeyError(f"Key '{key}' not found in configuration.")
    
    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set the value of a configuration key.
        """
        self.set(key, value)
    
    def clear(self) -> None:
        """
        Clear the configuration.
        """
        self.config_dict.clear()
    
    def copy(self) -> 'ConfigDict':
        """
        Create a copy of the configuration.
        """
        return ConfigDict(self.config_dict, self.parent)
    
    def walk(self, prefix: str = ""):
        """
        Walk through the configuration dictionary and yield key-value pairs (non-recursive).
        """
        stack = [(self.config_dict, prefix, self)]
        while stack:
            current_dict, current_prefix, current_config = stack.pop()
            for key, value in current_dict.items():
                if isinstance(value, Placeholder):
                    value = value._value(current_config, None)
                if isinstance(value, dict):
                    stack.append((value, current_prefix + key + ".", ConfigDict(value, current_config, copy=False)))
                else:
                    yield current_prefix + key, value

    def keys(self, recursive: bool = False) -> list[str]:
        """
        Get the keys of the configuration.
        """
        if recursive:
            return [key for key, _ in self.walk()]
        return list(self.config_dict.keys())
    
    def items(self, recursive: bool = False) -> list[tuple[str, Any]]:
        """
        Get the items of the configuration.
        """
        if recursive:
            return list(self.walk())
        return list(self.config_dict.items())
    
    def values(self, recursive: bool = False) -> list[Any]:
        """
        Get the values of the configuration.
        """
        if recursive:
            return [value for _, value in self.walk()]
        return list(self.config_dict.values())
    
    def __iter__(self) -> 'ConfigDict':
        """
        Iterate over the configuration dictionary.
        """
        return iter(self.config_dict)
    
    def __len__(self) -> int:
        """
        Get the length of the configuration dictionary.
        """
        return len(self.config_dict)
    
    def __repr__(self) -> str:
        """
        Get the string representation of the configuration dictionary.
        """
        return f"ConfigDict({self.config_dict})"
    

    def update(self, config_dict: Dict[str, Any], mode: Literal['simple', 'flat', 'recursive'] = 'simple') -> None:
        """
        Update the configuration.
        """
        if mode == 'flat':
            for key, value in config_dict.items():
                self.set(key, value)
        elif mode == 'recursive':
            stack = [(self.config_dict, config_dict)]
            while stack:
                current_dict, config_dict = stack.pop()
                for key, value in config_dict.items():
                    if isinstance(value, dict):
                        if key not in current_dict or not isinstance(current_dict[key], dict):
                            current_dict[key] = {}
                        stack.append((current_dict[key], value))
                    else:
                        current_dict[key] = value
        else:
            self.config_dict.update(config_dict)

    @staticmethod
    def from_env(prefix: str = "") -> 'ConfigDict':
        """
        Create a configuration from environment variables.
        """
        import os
        config_dict = ConfigDict()
        prefix = prefix.upper()
        config_dict.update({key.removeprefix(prefix): value for key, value in os.environ.items() if key.startswith(prefix)}, mode='flat')
        return config_dict
    
    @staticmethod
    def from_file(file_path: str) -> 'ConfigDict':
        """
        Create a configuration from a file.
        """
        if file_path.endswith('.yaml') or file_path.endswith('.yml'):
            import yaml
            with open(file_path, 'r') as f:
                config_dict = yaml.safe_load(f)
        elif file_path.endswith('.json'):
            import json
            with open(file_path, 'r') as f:
                config_dict = json.load(f)
        elif file_path.endswith('.py'):
            import importlib.util
            spec = importlib.util.spec_from_file_location("config", file_path)
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)
            if hasattr(config_module, 'config') and isinstance(config_module.config, dict):
                config_dict = config_module.config
            elif hasattr(config_module, 'config') and isinstance(config_module.config, ConfigDict):
                return config_module.config
            else:
                config_dict = {k: getattr(config_module, k) for k in dir(config_module) if not k.startswith("_")}

        return ConfigDict(config_dict)
