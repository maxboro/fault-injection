"""
python -m examples.decorator_raise_nth_multiple
"""
import random
from src.fault_injection import raise_at_nth_call

@raise_at_nth_call(n=2, func_id=1)
def add(a, b):
    return a + b

@raise_at_nth_call(n=4, func_id=2)
def print_(text: str):
    print(text)

for _ in range(10):
    try:
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        c = add(a, b)
        print_(c)
    except Exception as error:
        print(f"Error occurred: {error}")
 