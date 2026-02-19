import random
from functools import wraps


def random_raise(prob_of_raise=0.1):
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
