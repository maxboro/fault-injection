"""
python -m examples.inline_delay_nth
"""
import random
import time
from src.fault_injection import delay_at_nth_call_inline

def add_slowed(a, b):
    delay_at_nth_call_inline(time_s=0.5, n=4)
    return a + b


print("With delay")
for _ in range(10):
    start = time.perf_counter()
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    c = add_slowed(a, b)
    print(f"Result: {c}, duration {time.perf_counter() - start:.2f}s")
