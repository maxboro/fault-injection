"""
python -m examples.decorator_delay_nth
"""
import random
import time
from src.fault_injection import delay_at_nth_call

@delay_at_nth_call(time_s=0.5, n=3)
def add_slowed(a, b):
    return a + b

print("With delay")
for _ in range(10):
    start = time.perf_counter()
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    c = add_slowed(a, b)
    print(f"Result: {c}, duration {time.perf_counter() - start:.2f}s")
