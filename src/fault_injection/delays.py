"""Delay-based fault injection helpers."""

import random
import time
from functools import wraps
from typing import Any, Callable

Decorator = Callable[[Callable[..., Any]], Callable[..., Any]]


def delay_inline(time_s: float = 0.1, disable: bool = False) -> None:
    """Inject a fixed delay immediately.

    Args:
        time_s: Sleep duration in seconds. Must be non-negative.
        disable: If ``True``, the delay is skipped.

    Raises:
        ValueError: If ``time_s`` is negative.
    """
    if time_s < 0:
        raise ValueError("delay should have positive time_s")
    if not disable:
        time.sleep(time_s)


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


def delay_at_nth_call_inline(
        time_s: float = 0.1,
        n: int = 5,
        func_id = 1,
        disable: bool = False
    ) -> None:
    """Inject a fixed delay at the n-th call for a given ``func_id``.

    Args:
        time_s: Sleep duration in seconds. Must be non-negative.
        n: 1-based call number at which to inject the delay.
        func_id: Counter key used to isolate different call sites. Calls that use the same
            ``func_id`` share the same counter.
        disable: If ``True``, delay is skipped.

    Raises:
        ValueError: If ``time_s`` is negative.
        ValueError: If ``n`` is not a positive integer.
    """
    if time_s < 0:
        raise ValueError("delay should have positive time_s")
    if n < 1 or not isinstance(n, int):
        raise ValueError("n should be a positive interger.")

    if not hasattr(delay_at_nth_call_inline, "n_called_dict"):
        delay_at_nth_call_inline.n_called_dict = {}

    if func_id not in delay_at_nth_call_inline.n_called_dict.keys():
        delay_at_nth_call_inline.n_called_dict[func_id] = 0
    delay_at_nth_call_inline.n_called_dict[func_id] += 1
    if delay_at_nth_call_inline.n_called_dict[func_id] == n and not disable:
        time.sleep(time_s)


def delay_at_nth_call(
        time_s: float = 0.1,
        n: int = 5,
        func_id = 1,
        disable: bool = False
    ) -> Decorator:
    """Return a decorator that injects a fixed delay on the n-th call.

    Args:
        time_s: Sleep duration in seconds. Must be non-negative.
        n: 1-based call number at which to inject the delay.
        func_id: Counter key used to isolate different decorated functions. Decorators that
            use the same ``func_id`` share the same counter.
        disable: If ``True``, delay is skipped.

    Raises:
        ValueError: If ``time_s`` is negative.
        ValueError: If ``n`` is not a positive integer.
    """
    if time_s < 0:
        raise ValueError("delay should have positive time_s")
    if n < 1 or not isinstance(n, int):
        raise ValueError("n should be a positive interger.")

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not hasattr(delay_at_nth_call, "n_called_dict"):
                delay_at_nth_call.n_called_dict = {}
            if func_id not in delay_at_nth_call.n_called_dict.keys():
                delay_at_nth_call.n_called_dict[func_id] = 0
            delay_at_nth_call.n_called_dict[func_id] += 1
            if delay_at_nth_call.n_called_dict[func_id] == n and not disable:
                time.sleep(time_s)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def delay_random_inline(max_time_s: float = 0.1, disable: bool = False) -> None:
    """Inject a uniform random delay immediately.

    Args:
        max_time_s: Maximum sleep duration in seconds. Must be non-negative.
        disable: If ``True``, the random delay is skipped.

    Raises:
        ValueError: If ``max_time_s`` is negative.
    """
    if max_time_s < 0:
        raise ValueError("delay_random_inline should have positive max_time_s")
    if not disable:
        rnd = random.random()
        time_s = max_time_s * rnd
        time.sleep(time_s)


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


def delay_random_norm_inline(
    mean_time_s: float = 0.3,
    std_time_s: float = 0.1,
    disable: bool = False,
) -> None:
    """Inject a Gaussian random delay immediately.

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
    if not disable:
        time_s = random.gauss(mean_time_s, std_time_s)
        time_s = max(0, time_s)
        time.sleep(time_s)


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
