import random
from functools import wraps
import time


def raise_():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            raise RuntimeError("raise_ exception is raised")
        return wrapper
    return decorator


def raise_random(prob_of_raise=0.1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            rnd = random.random()
            if rnd < prob_of_raise:
                raise RuntimeError("random_raise exception is raised")
            return func(*args, **kwargs)
        return wrapper

    if not 0 <= prob_of_raise <= 1:
        raise ValueError("prob_of_raise should be 0-1")

    return decorator


def delay(time_s=0.1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(time_s)
            return func(*args, **kwargs)
        return wrapper

    if time_s < 0:
        raise ValueError("delay should have positive time_s")

    return decorator

def delay_random(max_time_s=0.1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            rnd = random.random()
            time_s = max_time_s * rnd
            time.sleep(time_s)
            return func(*args, **kwargs)
        return wrapper

    if max_time_s < 0:
        raise ValueError("delay_random should have positive max_time_s")

    return decorator
