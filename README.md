# fault-injection

Lightweight fault injection helpers for Python functions.

This project provides small decorators and inline helpers to intentionally inject failures or latency so you can test resiliency and error-handling paths.

## Features

- `raise_` and `raise_inline`: deterministic exception injection
- `raise_at_nth_call` and `raise_at_nth_call_inline`: deterministic exception injection on the n-th call (`func_id`-scoped counters)
- `raise_random` and `raise_random_inline`: probabilistic exception injection
- `delay` and `delay_inline`: fixed latency injection
- `delay_at_nth_call` and `delay_at_nth_call_inline`: fixed latency injection on the n-th call (`func_id`-scoped counters)
- `delay_random` and `delay_random_inline`: uniform random latency injection
- `delay_random_norm` and `delay_random_norm_inline`: Gaussian latency injection with clamp at `0`

## Project structure

- `fault_injection/`: library code
- `examples/`: runnable examples
- `tests/`: unit tests (`unittest` + standard library only)

## Installation

Install from PyPI:

```bash
python -m pip install fault-injection
```

For local development from this repo:

```bash
python -m pip install -e .
```

## Usage

Import APIs from `fault_injection`:

```python
from fault_injection import (
    raise_,
    raise_inline,
    raise_at_nth_call,
    raise_at_nth_call_inline,
    raise_random,
    raise_random_inline,
    delay,
    delay_inline,
    delay_at_nth_call,
    delay_at_nth_call_inline,
    delay_random,
    delay_random_inline,
    delay_random_norm,
    delay_random_norm_inline,
)
```

### `raise_`

```python
from fault_injection import raise_

@raise_(msg="decorator failure")
def do_work():
    return "ok"

# Raises RuntimeError("decorator failure")
do_work()
```

### `raise_inline`

```python
from fault_injection import raise_inline

def do_work():
    raise_inline(msg="inline failure")
    return "ok"

# Raises RuntimeError("inline failure")
do_work()
```

### `raise_at_nth_call`

```python
from fault_injection import raise_at_nth_call

@raise_at_nth_call(msg="raise on third call", n=3, func_id=1)
def do_work():
    return "ok"

do_work()  # 1st call: ok
do_work()  # 2nd call: ok
do_work()  # 3rd call: raises RuntimeError
```

### `raise_at_nth_call_inline`

```python
from fault_injection import raise_at_nth_call_inline

def do_work():
    raise_at_nth_call_inline(msg="raise on second call", n=2, func_id=9)
    return "ok"
```

### `raise_random`

```python
from fault_injection import raise_random

@raise_random(msg="random decorator failure", prob_of_raise=0.2)
def do_work():
    return "ok"

# Raises RuntimeError about 20% of calls
do_work()
```

### `raise_random_inline`

```python
from fault_injection import raise_random_inline

def do_work():
    raise_random_inline(msg="random inline failure", prob_of_raise=0.2)
    return "ok"
```

### `delay`

```python
from fault_injection import delay

@delay(time_s=0.5)
def do_work():
    return "ok"

# Sleeps 0.5s, then returns
print(do_work())
```

### `delay_inline`

```python
from fault_injection import delay_inline

def do_work():
    delay_inline(time_s=0.5)
    return "ok"
```

### `delay_at_nth_call`

```python
from fault_injection import delay_at_nth_call

@delay_at_nth_call(time_s=0.5, n=3, func_id=1)
def do_work():
    return "ok"

do_work()  # 1st call: no extra delay
do_work()  # 2nd call: no extra delay
do_work()  # 3rd call: sleeps 0.5s, then returns
```

### `delay_at_nth_call_inline`

```python
from fault_injection import delay_at_nth_call_inline

def do_work():
    delay_at_nth_call_inline(time_s=0.5, n=2, func_id=9)
    return "ok"
```

### `delay_random`

```python
from fault_injection import delay_random

@delay_random(max_time_s=0.5)
def do_work():
    return "ok"

# Sleeps random time in [0, 0.5], then returns
print(do_work())
```

### `delay_random_inline`

```python
from fault_injection import delay_random_inline

def do_work():
    delay_random_inline(max_time_s=0.5)
    return "ok"
```

### `delay_random_norm`

```python
from fault_injection import delay_random_norm

@delay_random_norm(mean_time_s=0.3, std_time_s=0.1)
def do_work():
    return "ok"

# Sleeps max(0, gauss(mean, std)), then returns
print(do_work())
```

### `delay_random_norm_inline`

```python
from fault_injection import delay_random_norm_inline

def do_work():
    delay_random_norm_inline(mean_time_s=0.3, std_time_s=0.1)
    return "ok"
```

## Validation behavior

- `raise_random(prob_of_raise=...)` and `raise_random_inline(prob_of_raise=...)` require `0 <= prob_of_raise <= 1`
- `raise_at_nth_call(n=...)` and `raise_at_nth_call_inline(n=...)` require `n` to be a positive integer
- `delay(time_s=...)` requires `time_s >= 0`
- `delay_inline(time_s=...)` requires `time_s >= 0`
- `delay_at_nth_call(time_s=..., n=...)` and `delay_at_nth_call_inline(time_s=..., n=...)` require `time_s >= 0` and `n` to be a positive integer
- `delay_random(max_time_s=...)` and `delay_random_inline(max_time_s=...)` require `max_time_s >= 0`
- `delay_random_norm(mean_time_s=..., std_time_s=...)` and `delay_random_norm_inline(mean_time_s=..., std_time_s=...)` require both `>= 0`

Invalid values raise `ValueError`.

## N-th call counters

`*_at_nth_call*` APIs keep counters on module-level function attributes and key by `func_id`.
Using the same `func_id` means sharing a counter; use different IDs to isolate behavior across call sites.

## Disable behavior

Every API supports `disable=True` to bypass fault injection:

```python
@delay(0.5, disable=True)
def do_work():
    return "ok"

delay_inline(0.5, disable=True)
```

## Run examples

From repository root (after `python -m pip install -e .`):

```bash
python -m examples.decorator_raise
python -m examples.decorator_raise_nth_multiple
python -m examples.decorator_raise_random
python -m examples.decorator_delay
python -m examples.decorator_delay_nth
python -m examples.decorator_delay_random
python -m examples.decorator_delay_random_norm
python -m examples.inline_raise
python -m examples.inline_raise_nth
python -m examples.inline_raise_nth_multiple
python -m examples.inline_raise_random
python -m examples.inline_delay
python -m examples.inline_delay_nth
python -m examples.inline_delay_random
python -m examples.inline_delay_random_norm
```

## Run tests

This project uses only the Python standard library for tests:

```bash
python -m unittest discover -s tests -v
```

No extra `PYTHONPATH` setup is needed with the root `fault_injection/` layout.

## Build and publish

Build distributions:

```bash
python -m pip install --upgrade build twine
python -m build
```

Upload to TestPyPI:

```bash
python -m twine upload --repository testpypi dist/*
```

Upload to PyPI:

```bash
python -m twine upload dist/*
```

## License

MIT (see `LICENSE`).
