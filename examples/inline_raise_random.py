"""
python -m examples.inline_raise_random
"""
import random
from fault_injection import raise_random_inline

def add(a, b):
    raise_random_inline(prob_of_raise=0.2)
    return a + b

for _ in range(100):
    try:
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        c = add(a, b)
        print(c)
    except Exception as error:
        print(f"Error occurred: {error}")
 