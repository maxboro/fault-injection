"""
python -m examples.inline_delay
"""
import random
import time
from fault_injection import delay_inline

def add_slowed(a, b):
    delay_inline()
    return a + b

def add(a, b):
    return a + b

print("Without delay")
for _ in range(10):
    start = time.perf_counter()
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    c = add(a, b)
    print(f"Result: {c}, duration {time.perf_counter() - start:.2f}s")


print("With delay")
for _ in range(10):
    start = time.perf_counter()
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    c = add_slowed(a, b)
    print(f"Result: {c}, duration {time.perf_counter() - start:.2f}s")

