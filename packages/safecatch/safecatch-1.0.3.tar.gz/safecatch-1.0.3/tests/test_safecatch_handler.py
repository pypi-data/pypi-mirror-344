import pytest
import math

from safecatch.safecatch import safecatch_handler


@safecatch_handler(ZeroDivisionError, 0)
def divide(a, b):
    return a / b


def test_divide_success():
    # When no exception occurs, the function should return the correct result.
    assert divide(10, 2) == 5


def test_divide_exception():
    # When a ZeroDivisionError occurs, the decorator should return 0.
    assert divide(10, 0) == 0


def test_unhandled_exception():
    # If the raised exception is not the one handled, it should propagate.
    @safecatch_handler(ValueError, "handled")
    def raise_type_error():
        raise TypeError("This is a TypeError")

    with pytest.raises(TypeError):
        raise_type_error()


def error_callback(x: float) -> None:
    """Prints an error message for negative inputs."""
    print(f"[ERROR] Cannot take sqrt of negative number: {x}")


@safecatch_handler(ValueError, error_callback)
def sqrt(x: float) -> float:
    """
    Returns the square root of x.
    Raises ValueError on negative input.
    """
    if x < 0:
        raise ValueError("x must be non-negative")
    return math.sqrt(x)


@pytest.mark.parametrize(
    "input_value, expected_result",
    [
        (-4, None),
        (9, 3.0),
        (0, 0.0),
    ],
)
def test_sqrt_with_invalid_and_valid_inputs(input_value, expected_result):
    result = sqrt(input_value)
    # Check that the return value is correct
    assert result == expected_result
