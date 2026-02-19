"""
python -m examples.decorator_raise_random
"""
import random
from src.fault_injection import raise_random

@raise_random(prob_of_raise=0.2)
def add(a, b):
    return a + b

for _ in range(100):
    try:
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        c = add(a, b)
        print(c)
    except Exception as error:
        print(f"Error occurred: {error}")
 