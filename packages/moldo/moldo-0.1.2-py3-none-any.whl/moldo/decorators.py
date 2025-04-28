from functools import wraps
from typing import Any, Callable, Optional

class MoldoFunction:
    def __init__(self, func: Callable, reference_name: Optional[str] = None):
        self.func = func
        self.reference_name = reference_name or func.__name__
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__
        self.__module__ = func.__module__

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.func(*args, **kwargs)

def moldo_function(reference_name: Optional[str] = None) -> Callable:
    """
    Decorator to mark a Python function as usable in Moldo.
    
    Args:
        reference_name: Optional name to use when referencing this function in Moldo.
                       If not provided, the function's name will be used.
    
    Example:
        @moldo_function(reference_name="add_numbers")
        def add(a: int, b: int) -> int:
            return a + b
    """
    def decorator(func: Callable) -> MoldoFunction:
        return MoldoFunction(func, reference_name)
    return decorator
