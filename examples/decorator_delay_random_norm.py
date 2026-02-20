"""
python -m examples.decorator_delay_random_norm
"""
import random
import time
from fault_injection import delay_random_norm

@delay_random_norm(1, 0.1)
def add_slowed(a, b):
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

