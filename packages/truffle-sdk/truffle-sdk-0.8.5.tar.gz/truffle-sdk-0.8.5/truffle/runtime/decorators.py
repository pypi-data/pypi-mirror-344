import typing
from truffle.common import get_logger
from .base import *

logger = get_logger()

def tool_decorator(description: str = None, icon: str = None, predicate: typing.Callable = None):
    def decorator(func):
        assert verify_func(func), f"Function {func.__name__} cannot be a tool"
        func.__truffle_tool__ = True
        func.__truffle_description__ = description
        func.__truffle_icon__ = icon
        if not hasattr(func, "__truffle_args__"):
            func.__truffle_args__ = None
        if not hasattr(func, "__truffle_group__"):
            func.__truffle_group__ = None
        
        if predicate is not None:
            assert verify_predicate(predicate), f"Function {func.__name__} has an invalid predicate"
            func.__truffle_predicate__ = predicate
        logger.debug(f"@truffle.tool({description},{icon}) - {func.__name__} {' - predicate' if predicate else ''}")
        return func
    return decorator

def args_decorator(**kwargs):
    def decorator(func):
        assert verify_arg_descriptions(func.__name__, kwargs)
        func.__truffle_args__ = kwargs

        logger.debug(f"@truffle.args({kwargs}) for function: {func.__name__}")
        return func
    return decorator

def group_decorator(name: str, leader: bool = False): 
    def decorator(func):
        assert verify_func(func), f"Function {func.__name__} cannot be a group"
        func.__truffle_group__ = name
        func.__truffle_group_leader__ = leader
        logger.debug(f"@truffle.group({name}, {leader}) - {func.__name__}")
        return func
    return decorator

def app_decorator(description: typing.Optional[str] = None):
    """Decorator to mark a class as the main Truffle application and provide metadata."""
    def decorator(cls):
        # Ensure the decorated object is a class
        if not isinstance(cls, type):
            raise TypeError(f"@truffle.app can only decorate classes, not {type(cls).__name__}")
        
        cls.__truffle_app__ = True
        cls.__truffle_app_description__ = description
        
        # Potentially add other app-level metadata here in the future (e.g., icon)
        # cls.__truffle_app_icon__ = icon 
        
        logger.debug(f"@truffle.app applied to class {cls.__name__} with description: '{description}'")
        return cls
    return decorator