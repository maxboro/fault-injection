import random
import time
from functools import wraps
from typing import Any, Callable

Decorator = Callable[[Callable[..., Any]], Callable[..., Any]]


def delay(time_s: float = 0.1, disable: bool = False) -> Decorator:
    """Return a decorator that injects a fixed delay before function execution.

    Args:
        time_s: Sleep duration in seconds. Must be non-negative.
        disable: If ``True``, the delay is skipped.

    Raises:
        ValueError: If ``time_s`` is negative.
    """
    if time_s < 0:
        raise ValueError("delay should have positive time_s")

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """Wrap ``func`` with a fixed pre-execution delay."""
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not disable:
                time.sleep(time_s)
            return func(*args, **kwargs)
        return wrapper

    return decorator


def delay_random(max_time_s: float = 0.1, disable: bool = False) -> Decorator:
    """Return a decorator that injects a uniform random delay before execution.

    Args:
        max_time_s: Maximum sleep duration in seconds. Must be non-negative.
        disable: If ``True``, the random delay is skipped.

    Raises:
        ValueError: If ``max_time_s`` is negative.
    """
    if max_time_s < 0:
        raise ValueError("delay_random should have positive max_time_s")

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """Wrap ``func`` with a random delay in ``[0, max_time_s]``."""
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not disable:
                rnd = random.random()
                time_s = max_time_s * rnd
                time.sleep(time_s)
            return func(*args, **kwargs)
        return wrapper

    return decorator


def delay_random_norm(
    mean_time_s: float = 0.3,
    std_time_s: float = 0.1,
    disable: bool = False,
) -> Decorator:
    """Return a decorator that injects a Gaussian random delay before execution.

    The sampled delay is clamped to zero to avoid negative sleep times.

    Args:
        mean_time_s: Mean of the Gaussian distribution in seconds.
        std_time_s: Standard deviation of the Gaussian distribution in seconds.
        disable: If ``True``, the random delay is skipped.

    Raises:
        ValueError: If ``mean_time_s`` or ``std_time_s`` is negative.
    """
    if mean_time_s < 0:
        raise ValueError("delay_random_norm should have positive mean_time_s")
    if std_time_s < 0:
        raise ValueError("delay_random_norm should have positive std_time_s")

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """Wrap ``func`` with a non-negative Gaussian random delay."""
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not disable:
                time_s = random.gauss(mean_time_s, std_time_s)
                time_s = max(0, time_s)
                time.sleep(time_s)
            return func(*args, **kwargs)
        return wrapper

    return decorator
