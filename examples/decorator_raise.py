"""
python -m examples.decorator_raise
"""
import random
from src.fault_injection.decorators import raise_

@raise_()
def add(a, b):
    return a + b

for _ in range(10):
    try:
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        c = add(a, b)
        print(c)
    except Exception as error:
        print(f"Error occurred: {error}")
 