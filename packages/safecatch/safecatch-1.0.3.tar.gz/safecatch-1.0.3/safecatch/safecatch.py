from functools import wraps
from typing import Any, Type, Callable, Union

# A fallback can be a literal or a function taking (*args, **kwargs) -> Any
Fallback = Union[Any, Callable[..., Any]]


def safecatch_handler(
    exc_type: Type[Exception], fallback: Fallback
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator that catches a specified exception and either:
      • returns a literal fallback value, or
      • calls a fallback function with the same args/kwargs and returns its result.

    :param exc_type:  Exception type to catch (e.g., ValueError, ZeroDivisionError, etc.)
    :param fallback:  Either a literal return value or a callable(*args, **kwargs) -> return value
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except exc_type:
                # if fallback is a function, invoke it; otherwise return it directly
                if callable(fallback):
                    return fallback(*args, **kwargs)
                return fallback

        return wrapper

    return decorator
