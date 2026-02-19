"""
python -m examples.inline_raise
"""
import random
from src.fault_injection import raise_inline

def add(a, b):
    raise_inline()
    return a + b

for _ in range(10):
    try:
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        c = add(a, b)
        print(c)
    except Exception as error:
        print(f"Error occurred: {error}")
 