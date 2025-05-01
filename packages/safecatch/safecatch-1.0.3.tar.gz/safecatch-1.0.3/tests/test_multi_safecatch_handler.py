import pytest

from safecatch.multi_safecatch import multi_safecatch_handler


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (3, 2, 5),  # When no exception occurs, the function should return the correct result.
        (3, 0, 0),  # When a ZeroDivisionError occurs, the decorator should return 0.
        (3, -1, -1),  # When a ValueError occurs, the decorator should return -1.
    ],
)
def test_values_check_func(x: float, y: float, expected: float) -> None:
    assert values_check_func(x, y) == expected


@multi_safecatch_handler({ZeroDivisionError: 0, ValueError: -1})
def values_check_func(x: float, y: float) -> float:
    if y == 0:
        return x / y  # Raises ZeroDivisionError

    elif y < 0:
        raise ValueError("Negative value!")  # Raises ValueError
    else:
        return x + y


def test_unhandled_exception_in_multi():
    # If an exception that is not handled occurs, it should propagate.
    @multi_safecatch_handler({ValueError: -1})
    def raise_type_error():
        raise TypeError("Unhandled exception")

    with pytest.raises(TypeError):
        raise_type_error()


def fallback_zero_div(x: float, y: float) -> float:
    """Handle ZeroDivisionError by logging and returning 0."""
    print(f"ZeroDivisionError caught in check_func with x={x}, y={y}")
    return 0


def fallback_value_error(x: float, y: float) -> float:
    """Handle ValueError by logging and returning -abs(x)."""
    print(f"ValueError caught in check_func with x={x}, y={y}")
    return -abs(x)


@multi_safecatch_handler(
    {ZeroDivisionError: fallback_zero_div, ValueError: fallback_value_error}
)
def functions_check_func(x: float, y: float) -> float:
    if y == 0:
        return x / y  # raises ZeroDivisionError

    if y < 0:
        raise ValueError("Negative value!")  # raises ValueError
    return x + y  # normal path


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (10, 0, 0.0),  # ZeroDivisionError → fallback_zero_div → logs + 0.0
        (10, -2, -10.0),  # ValueError     → fallback_value_error → logs + -abs(10)
        (10, 5, 15.0),  # normal addition
    ],
)
def test_check_func(x: float, y: float, expected: float) -> None:
    assert functions_check_func(x, y) == expected
