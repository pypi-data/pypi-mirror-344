import abc 
import typing
import inspect
import json 
from datetime import datetime
from truffle.common import get_logger

class BaseRuntime(metaclass=abc.ABCMeta):
    def __init__(self):
        # Simple model cache
        self._models = {}  # model_id -> ModelDescription
        self._model_usage = {}  # model_id -> dict with basic usage stats
        self._last_update = datetime.now().timestamp()

    @abc.abstractmethod
    def build(self, class_instance: typing.Any) -> None:
        pass

    def get_available_models(self) -> typing.List[typing.Any]:
        """Return list of available models from the cache."""
        return list(self._models.values())

    def register_model(self, model: typing.Any) -> None:
        """Register a model with the runtime."""
        from .types.models import ModelDescription  # Lazy import
        if not isinstance(model, ModelDescription):
            raise TypeError(f"Expected ModelDescription, got {type(model)}")
        self._models[model.model_id] = model
        if model.model_id not in self._model_usage:
            self._model_usage[model.model_id] = {
                'request_count': 0,
                'total_tokens': 0,
                'error_count': 0,
                'last_latency': 0.0
            }
        self._last_update = datetime.now().timestamp()

    def get_model(self, model_id: int) -> typing.Optional[typing.Any]:
        """Get a specific model by ID."""
        return self._models.get(model_id)

    def update_model_usage(
        self,
        model_id: int,
        latency: float,
        tokens: int,
        error: bool = False
    ) -> None:
        """Update basic usage stats for a model."""
        if model_id in self._model_usage:
            stats = self._model_usage[model_id]
            stats['request_count'] += 1
            stats['total_tokens'] += tokens
            stats['last_latency'] = latency
            if error:
                stats['error_count'] += 1

    def is_cache_stale(self, max_age_seconds: int = 300) -> bool:
        """Check if the model cache is stale."""
        if not self._models:
            return True
        age = datetime.now().timestamp() - self._last_update
        return age > max_age_seconds


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


def get_members(obj : typing.Any, pred: typing.Callable) -> typing.Dict[str, typing.Any]:
    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and pred(value):
            pr[name] = value
    return pr

def get_non_function_members(obj):
    return get_members(obj, lambda o: not inspect.ismethod(o))

def get_function_members(obj):
    return get_members(obj, inspect.ismethod)
    

def args_from_func(func : typing.Callable) -> typing.Dict[str, typing.Any]:
    type_hints = typing.get_type_hints(func)
    assert callable(func), f"Expected a function, got type: {type(func)} {func}."
    assert type_hints, f"Function {func.__name__} must have type hints."
    
    assert "return" in type_hints, f"Function {func.__name__} must have a return value and type hint."

    args_dict = {}
    for param_name, param in type_hints.items():
        param_type = type_hints.get(param_name, type(None))
        assert param_type.__name__ != "NoneType", (
            f"Function {func.__name__}: Parameter '{param_name}' has no type hint. Make sure to include a type hint."
        )
        args_dict[param_name] = param_type

    assert "return" in args_dict, f"Args dict missing return value for function {func.__name__}."
    return args_dict


def get_truffle_tool_fns(obj):
    tools = {}
    for name, func in get_function_members(obj).items():
        if hasattr(func, "__truffle_tool__"):
            if hasattr(func, "__self__"):
                tools[name] = func.__func__
            else:
                tools[name] = func
                get_logger().warning(f"Function {func.__name__} missing self parameter. Trying to make it work.")
    assert len(tools) > 0, f"Object {obj.__name__} has no truffle tools defined."
    return tools


def verify_func(func : typing.Callable) -> bool:
    assert len(args_from_func(func)), f"Function {func.__name__} invalid"
    return True

def verify_arg_descriptions(fn_name :str, kwargs : typing.Dict[str, typing.Any]) -> bool:
    assert len(kwargs) > 0, f"{fn_name} - truffle.args() requires at least one [name, description] pair, got none"
    for key, value in kwargs.items():
        assert isinstance(key, str),   f"{fn_name}.args({key}='{value}') - Expected string, got type {type(key)} {key}."
        assert isinstance(value, str), f"{fn_name}.args({key}='{value}') - Expected string, got type {type(value)} {value}."
    return True


def verify_predicate(func : typing.Callable) -> bool:
    assert callable(func), f"Predicate for {func.__name__} must be callable"
    assert inspect.isfunction(func), f"Predicate for {func.__name__} must be a function"
    # assert no args
    assert len(inspect.signature(func).parameters) == 0, f"Predicate for {func.__name__} must have no arguments"
    # should assert returns bool, but we don't want to call it, so we will just wrap it in something that deals with that

    return True


def check_groups(obj : typing.Any) -> bool:
    groups = {}
    for name, func in get_function_members(obj).items():
        if getattr(func, "__truffle_group__", None) is not None:
            is_leader = getattr(func, "__truffle_group_leader__", False)
            group_name = str(func.__truffle_group__)
            if group_name not in groups:
                groups[group_name] = {"leaders": [], "members": []}
            if is_leader:
                groups[group_name]["leaders"].append(func)
            else:
                groups[group_name]["members"].append(func)

    for group_name, group in groups.items():
        assert len(group["leaders"]) > 0, f"Group {group_name} has no leaders, so all tools in the group will be ignored."
        if len(group["members"]) == 0:
            get_logger().warning(f"Group {group_name} has no members, so all tools in the group will be available")

    return True
           