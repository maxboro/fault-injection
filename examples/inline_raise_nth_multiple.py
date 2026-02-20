"""
python -m examples.inline_raise_nth_multiple
"""
import random
from src.fault_injection import raise_at_nth_call_inline

def add(a, b):
    raise_at_nth_call_inline(n=1, func_id=1)
    return a + b

def print_(text: str):
    raise_at_nth_call_inline(n=7, func_id=2)
    print(text)

for _ in range(10):
    try:
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        c = add(a, b)
        print_(c)
    except Exception as error:
        print(f"Error occurred: {error}")
 