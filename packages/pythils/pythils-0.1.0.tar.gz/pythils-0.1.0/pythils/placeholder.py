from abc import ABCMeta
from typing import Callable, Optional

class Placeholder(metaclass=ABCMeta):
    """
    A placeholder class that can be used to create a placeholder 
    for a function, a class, an attribute, etc.
    """
    __slots__ = ()

    def __getattr__(self, name: str) -> 'Placeholder':
        """
        This method is called when an attribute is accessed on the placeholder.
        It returns a new instance of the placeholder with the attribute name.
        """
        return BoundedAttributePlaceholder(name=name, instance=self)
    
    def __setattr__(self, name: str, value: object):
        """
        This method is called when an attribute is set on the placeholder.
        It raises an AttributeError to prevent setting attributes on the placeholder. (for now)
        """
        if name in self.__slots__:
            object.__setattr__(self, name, value)
        else:
            raise AttributeError(f"Cannot set attribute '{name}' on placeholder.")

    def __call__(self, *args, **kwargs) -> 'Placeholder':
        """
        This method is called when the placeholder is called as a function.
        It returns a new instance of the placeholder with the function name.
        """
        return CalledPlaceholder(func=self, args=args, kwargs=kwargs)
    
    def _value(self, *args, **kwargs) -> object:
        """
        This method should be overridden in subclasses to provide the actual value.
        """
        raise NotImplementedError("Placeholder subclasses must implement _value method.")
    

class LazyWrapper(Placeholder):
    __slots__ = ('_obj',)
    def __init__(self, obj: object):
        self._obj = obj
    def _value(self, *args, **kwargs):
        return self._obj

lazy = LazyWrapper

NOT_SET = object()

class ManualPlaceholder(Placeholder):
    __slots__ = ("_value_object",)
    def __init__(self, value: object = NOT_SET):
        self._value_object = value
    
    def _is_set(self) -> bool:
        return self._value_object is not NOT_SET
    
    def _set(self, value: object):
        if self._value_object is NOT_SET:
            self._value_object = value
        else:
            raise RuntimeError("Value already set")
    
    def _value(self, *args, **kwargs):
        if self._value_object is NOT_SET:
            raise RuntimeError("Value not set")
        return self._value_object


class ModifiablePlaceholder(Placeholder):
    class _AttributePlaceholder:
        __slots__ = ("_name")
        def __init__(self, name: str):
            self._name = name
        
        def __get__(self, instance, _) -> Placeholder:
            if instance is None:
                return self
            else:
                return instance.__getattr__(self._name)
        
        def __set__(self, instance, value):
            if instance is None:
                raise AttributeError(f"Cannot set attribute '{self._name}' on placeholder.")
            else:
                instance.__setattr__(self._name, value)

    __slots__ = ("_initial_object", "_modifiers", "_value_object", "_root")
    __add__ = _AttributePlaceholder("__add__")
    __sub__ = _AttributePlaceholder("__sub__")
    __mul__ = _AttributePlaceholder("__mul__")
    __truediv__ = _AttributePlaceholder("__truediv__")
    __floordiv__ = _AttributePlaceholder("__floordiv__")
    __mod__ = _AttributePlaceholder("__mod__")
    __pow__ = _AttributePlaceholder("__pow__")
    __neg__ = _AttributePlaceholder("__neg__")
    __pos__ = _AttributePlaceholder("__pos__")
    __abs__ = _AttributePlaceholder("__abs__")
    __lshift__ = _AttributePlaceholder("__lshift__")
    __rshift__ = _AttributePlaceholder("__rshift__")
    __and__ = _AttributePlaceholder("__and__")
    __or__ = _AttributePlaceholder("__or__")
    __xor__ = _AttributePlaceholder("__xor__")
    __lt__ = _AttributePlaceholder("__lt__")
    __le__ = _AttributePlaceholder("__le__")
    __eq__ = _AttributePlaceholder("__eq__")
    __ne__ = _AttributePlaceholder("__ne__")
    __gt__ = _AttributePlaceholder("__gt__")
    __ge__ = _AttributePlaceholder("__ge__")
    __contains__ = _AttributePlaceholder("__contains__")
    __getitem__ = _AttributePlaceholder("__getitem__")
    __setitem__ = _AttributePlaceholder("__setitem__")
    __delitem__ = _AttributePlaceholder("__delitem__")
    __iter__ = _AttributePlaceholder("__iter__")
    __next__ = _AttributePlaceholder("__next__")
    __iadd__ = _AttributePlaceholder("__iadd__")
    __isub__ = _AttributePlaceholder("__isub__")
    __imul__ = _AttributePlaceholder("__imul__")
    __itruediv__ = _AttributePlaceholder("__itruediv__")
    __ifloordiv__ = _AttributePlaceholder("__ifloordiv__")
    __imod__ = _AttributePlaceholder("__imod__")
    __ipow__ = _AttributePlaceholder("__ipow__")
    __ilshift__ = _AttributePlaceholder("__ilshift__")
    __irshift__ = _AttributePlaceholder("__irshift__")
    __iand__ = _AttributePlaceholder("__iand__")
    __ior__ = _AttributePlaceholder("__ior__")
    __ixor__ = _AttributePlaceholder("__ixor__")
    #__len__ = _AttributePlaceholder("__len__")

    def __init__(self, initial_object: object, _root: Optional['ModifiablePlaceholder'] = None):
        object.__setattr__(self,'_initial_object', initial_object)
        if _root is None:
            _modifiers = [(self, lambda *args, **kwargs: initial_object._value(*args, **kwargs) if isinstance(initial_object, Placeholder) else initial_object)]
            object.__setattr__(self,'_modifiers', _modifiers)
            _root = self
        
        object.__setattr__(self,'_root', _root)
        object.__setattr__(self,'_value_object', NOT_SET)
    
    def _is_set(self) -> bool:
        return self._value_object is not NOT_SET and self is not self._root

    def __getattr__(self, name):
        if name in self.__slots__:
            return object.__getattribute__(self, name)
        if self._is_set():
            return getattr(self._value_object, name)
        
        if name in ('__imul__', '__iadd__', '__isub__', '__imul__', '__itruediv__', '__ifloordiv__', '__imod__', '__ipow__', '__ilshift__', '__irshift__', '__iand__', '__ior__', '__ixor__'):
            def inplace_op_modifier(*args, **kwargs):
                def inplace_op(value):
                    if name == '__iadd__':
                        self._value_object += value
                    elif name == '__isub__':
                        self._value_object -= value
                    elif name == '__imul__':
                        self._value_object *= value
                    elif name == '__itruediv__':
                        self._value_object /= value
                    elif name == '__ifloordiv__':
                        self._value_object //= value
                    elif name == '__imod__':
                        self._value_object %= value
                    elif name == '__ipow__':
                        self._value_object **= value
                    elif name == '__ilshift__':
                        self._value_object <<= value
                    elif name == '__irshift__':
                        self._value_object >>= value
                    elif name == '__iand__':
                        self._value_object &= value
                    elif name == '__ior__':
                        self._value_object |= value
                    elif name == '__ixor__':
                        self._value_object ^= value
                    return self._value_object
                return inplace_op
            res_ph = ModifiablePlaceholder(self, self._root)
            self._root._modifiers.append((res_ph, inplace_op_modifier))
            return res_ph

        def get_modifier(*args, **kwargs):
                return getattr(self._value_object, name)
        res_ph = ModifiablePlaceholder(self, self._root)
        self._root._modifiers.append((res_ph, get_modifier))
        return res_ph

    def __setattr__(self, name, value):
        if name in self.__slots__:
            object.__setattr__(self, name, value)
            return
        if self._value_object is not NOT_SET:
            setattr(self._value_object, name, value)
            return
        else:
            def set_modifier(*args, **kwargs):
                setattr(self._value_object, name, value)
            res_ph = ModifiablePlaceholder(self, self._root)
            self._root._modifiers.append((res_ph, set_modifier))
    
    def __call__(self, *call_args, **call_kwargs):
        if self._value_object is not NOT_SET:
            return self._value_object(*call_args, **call_kwargs)
        
        def call_modifier(*args, **kwargs):
            _cargs = [arg._value(*args, **kwargs) if isinstance(arg, Placeholder) else arg for arg in call_args]
            _ckwargs = {k: (v._value(*args, **kwargs) if isinstance(v, Placeholder) else v) for k, v in call_kwargs.items()}
            return self._value_object(*_cargs, **_ckwargs)
        res_ph = ModifiablePlaceholder(self, self._root)
        self._root._modifiers.append((res_ph, call_modifier))
        return res_ph
    
    def _calc_value(self, _target:'ModifiablePlaceholder', *args, **kwargs):
        if self is not _target._root:
            return _target._root._calc_value(_target, *args, **kwargs)
        while not _target._is_set() and self._modifiers:
            res_ph, modifier = self._modifiers.pop(0)
            res_ph._value_object = modifier(*args, **kwargs)
    
    def _value(self, *args, **kwargs):
        if self._is_set():
            return self._value_object
        self._root._calc_value(self, *args, **kwargs)
        return self._value_object


class BoundedAttributePlaceholder(Placeholder):
    __slots__ = ("_name", "_instance")
    def __init__(self, name: str, instance: object):
        self._name = name
        self._instance = instance
    
    def _value(self, *args, **kwargs):
        if isinstance(self._instance, Placeholder):
            instance = self._instance._value(*args, **kwargs)
        else:
            instance = self._instance
        return getattr(instance, self._name)

class CalledPlaceholder(Placeholder):
    __slots__ = ("_func", "_args", "_kwargs")
    def __init__(self, func:Placeholder|Callable, args, kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def _value(self, *args, **kwargs):
        if isinstance(self._func, Placeholder):
            func = self._func._value(*args, **kwargs)
        else:
            func = self._func

        if not callable(func):
            raise TypeError(f"Expected a callable, got {type(func).__name__}")
        
        args = [(arg if not isinstance(arg, Placeholder) else arg._value(*args, **kwargs)) for arg in self._args]
        kwargs = {k: (v if not isinstance(v, Placeholder) else v._value(*args, **kwargs)) for k, v in self._kwargs.items()}
        return func(*args, **kwargs)

class AttributePlaceholder:
    """
    A placeholder for class attributes.
    """
    __slots__ = ("_name", "_owner")
    def __init__(self, name: str, owner: type = None):
        self._name = name
        self._owner = owner

    def __get__(self, instance, owner) -> Placeholder:
        if instance is None and self._owner is not None:
            return self
        elif instance is None and self._owner is None:
            return AttributePlaceholder(self._name, owner)
        else: # instance is not None
            return BoundedAttributePlaceholder(self._name, instance)
    
    def __repr__(self):
        if self._owner is not None:
            return f"AttributePlaceholder({self._name} of type {self._owner.__name__})"
        return f"AttributePlaceholder({self._name})"
    

