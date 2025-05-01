from functools import wraps
from typing import Any, Callable, Dict, Type, Union

# A fallback can be a value (Any) or a function that accepts
# the decorated function’s args/kwargs and returns Any.
Fallback = Union[Any, Callable[..., Any]]


def multi_safecatch_handler(
    exception_map: Dict[Type[Exception], Fallback]
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator that catches specified exceptions and either:
      • returns a literal fallback, or
      • calls a fallback function with the same args/kwargs and returns its result.

    :param exception_map: map from Exception types to either:
                          - a literal return value, or
                          - a callable(*args, **kwargs) → return value
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                for exc_type, fallback in exception_map.items():
                    if isinstance(e, exc_type):
                        if callable(fallback):
                            # invoke fallback with original arguments
                            return fallback(*args, **kwargs)
                        return fallback
                        return fallback
                # not one of our handled exceptions → re-raise
                raise

        return wrapper

    return decorator
