"""Exception-based fault injection helpers."""

import random
from functools import wraps
from typing import Any, Callable

Decorator = Callable[[Callable[..., Any]], Callable[..., Any]]


def raise_inline(msg: str = "raise_inline exception is raised", disable: bool = False) -> None:
    """Raise ``RuntimeError`` immediately unless disabled.

    Args:
        msg: Exception message.
        disable: If ``True``, raising is skipped.
    """
    if not disable:
        raise RuntimeError(msg)


def raise_(msg: str = "raise_ exception is raised", disable: bool = False) -> Decorator:
    """Return a decorator that always raises ``RuntimeError`` unless disabled.

    Args:
        msg: Exception message. This is the first positional argument.
        disable: If ``True``, no exception is injected and the function executes.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """Wrap ``func`` with deterministic exception injection."""
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if disable:
                return func(*args, **kwargs)
            raise RuntimeError(msg)
        return wrapper
    return decorator


def raise_at_nth_call_inline(
        msg: str = "raise_at_nth_call_inline exception is raised",
        n: int = 5,
        func_id = 1,
        disable: bool = False
    ) -> None:
    """Raise ``RuntimeError`` at the n-th call for a given ``func_id``.

    Args:
        msg: Exception message.
        n: 1-based call number at which to raise.
        func_id: Counter key used to isolate different call sites. Calls that use the same
            ``func_id`` share the same counter.
        disable: If ``True``, raising is skipped.

    Raises:
        ValueError: If ``n`` is not a positive integer.
    """
    if n < 1 or not isinstance(n, int):
        raise ValueError("n should be a positive interger.")

    if not hasattr(raise_at_nth_call_inline, "n_called_dict"):
        raise_at_nth_call_inline.n_called_dict = {}

    if func_id not in raise_at_nth_call_inline.n_called_dict.keys():
        raise_at_nth_call_inline.n_called_dict[func_id] = 0
    raise_at_nth_call_inline.n_called_dict[func_id] += 1
    if raise_at_nth_call_inline.n_called_dict[func_id] == n and not disable:
        raise RuntimeError(msg + f"\nFunc id {func_id}")


def raise_at_nth_call(
        msg: str = "raise_at_nth_call exception is raised",
        n: int = 5,
        func_id = 1,
        disable: bool = False
    ) -> Decorator:
    """Return a decorator that raises ``RuntimeError`` on the n-th call.

    Args:
        msg: Exception message. This is the first positional argument.
        n: 1-based call number at which to raise.
        func_id: Counter key used to isolate different decorated functions. Decorators that
            use the same ``func_id`` share the same counter.
        disable: If ``True``, no exception is injected and the function executes.

    Raises:
        ValueError: If ``n`` is not a positive integer.
    """
    if n < 1 or not isinstance(n, int):
        raise ValueError("n should be a positive interger.")

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """Wrap ``func`` with deterministic exception injection."""
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not hasattr(raise_at_nth_call, "n_called_dict"):
                raise_at_nth_call.n_called_dict = {}

            if func_id not in raise_at_nth_call.n_called_dict.keys():
                raise_at_nth_call.n_called_dict[func_id] = 0
            raise_at_nth_call.n_called_dict[func_id] += 1
            if raise_at_nth_call.n_called_dict[func_id] == n and not disable:
                raise RuntimeError(msg + f"\nFunc id {func_id}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def raise_random_inline(
    msg: str = "raise_random exception is raised",
    prob_of_raise: float = 0.1,
    disable: bool = False,
) -> None:
    """Raise ``RuntimeError`` with probability ``prob_of_raise`` unless disabled.

    Args:
        msg: Exception message.
        prob_of_raise: Probability in ``[0, 1]`` used to raise an exception.
        disable: If ``True``, raising is skipped.

    Raises:
        ValueError: If ``prob_of_raise`` is outside ``[0, 1]``.
    """
    if not 0 <= prob_of_raise <= 1:
        raise ValueError("prob_of_raise should be 0-1")
    if not disable:
        rnd = random.random()
        if rnd < prob_of_raise:
            raise RuntimeError(msg)


def raise_random(
    msg: str = "raise_random exception is raised",
    prob_of_raise: float = 0.1,
    disable: bool = False,
) -> Decorator:
    """Return a decorator that raises ``RuntimeError`` with a set probability.

    Args:
        msg: Exception message. This is the first positional argument.
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
                    raise RuntimeError(msg)
            return func(*args, **kwargs)
        return wrapper
    return decorator
