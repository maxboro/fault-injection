import random
from functools import wraps
from typing import Any, Callable

Decorator = Callable[[Callable[..., Any]], Callable[..., Any]]


def raise_(disable: bool = False) -> Decorator:
    """Return a decorator that always raises ``RuntimeError`` unless disabled.

    Args:
        disable: If ``True``, no exception is injected and the function executes.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """Wrap ``func`` with deterministic exception injection."""
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if disable:
                return func(*args, **kwargs)
            raise RuntimeError("raise_ exception is raised")
        return wrapper

    return decorator


def raise_random(
    prob_of_raise: float = 0.1,
    disable: bool = False,
) -> Decorator:
    """Return a decorator that raises ``RuntimeError`` with a set probability.

    Args:
        prob_of_raise: Probability in ``[0, 1]`` used to raise an exception.
        disable: If ``True``, exception injection is skipped.

    Raises:
        ValueError: If ``prob_of_raise`` is outside ``[0, 1]``.
    """
    if not 0 <= prob_of_raise <= 1:
        raise ValueError("prob_of_raise should be 0-1")

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """Wrap ``func`` with probabilistic exception injection."""
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not disable:
                rnd = random.random()
                if rnd < prob_of_raise:
                    raise RuntimeError("random_raise exception is raised")
            return func(*args, **kwargs)
        return wrapper

    return decorator
