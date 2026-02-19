import random
from functools import wraps


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
    pass

def delay_random(max_time_s=0.1):
    pass