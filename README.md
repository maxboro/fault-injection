# fault-injection

Lightweight fault injection decorators for Python functions.

This project provides small decorators to intentionally inject failures or latency so you can test resiliency and error-handling paths.

## Features

- `raise_`: always raises a `RuntimeError` (unless disabled)
- `raise_random`: raises a `RuntimeError` with configurable probability
- `delay`: adds a fixed delay before function execution
- `delay_random`: adds a random delay between `0` and `max_time_s`
- `delay_random_norm`: adds a Gaussian delay with clamp at `0`

## Project structure

- `src/fault_injection/`: library code
- `examples/`: runnable examples
- `tests/`: unit tests (`unittest` + standard library only)

## Usage

Import decorators from `src.fault_injection`:

```python
from src.fault_injection import (
    raise_,
    raise_random,
    delay,
    delay_random,
    delay_random_norm,
)
```

### `raise_`

```python
from src.fault_injection import raise_

@raise_()
def do_work():
    return "ok"

# Raises RuntimeError("raise_ exception is raised")
do_work()
```

### `raise_random`

```python
from src.fault_injection import raise_random

@raise_random(prob_of_raise=0.2)
def do_work():
    return "ok"

# Raises RuntimeError about 20% of calls
do_work()
```

### `delay`

```python
from src.fault_injection import delay

@delay(time_s=0.5)
def do_work():
    return "ok"

# Sleeps 0.5s, then returns
print(do_work())
```

### `delay_random`

```python
from src.fault_injection import delay_random

@delay_random(max_time_s=0.5)
def do_work():
    return "ok"

# Sleeps random time in [0, 0.5], then returns
print(do_work())
```

### `delay_random_norm`

```python
from src.fault_injection import delay_random_norm

@delay_random_norm(mean_time_s=0.3, std_time_s=0.1)
def do_work():
    return "ok"

# Sleeps max(0, gauss(mean, std)), then returns
print(do_work())
```

## Validation behavior

- `raise_random(prob_of_raise=...)` requires `0 <= prob_of_raise <= 1`
- `delay(time_s=...)` requires `time_s >= 0`
- `delay_random(max_time_s=...)` requires `max_time_s >= 0`
- `delay_random_norm(mean_time_s=..., std_time_s=...)` requires both `>= 0`

Invalid values raise `ValueError`.

## Disable behavior

Every decorator supports `disable=True` to bypass fault injection:

```python
@delay(0.5, disable=True)
def do_work():
    return "ok"
```

## Run examples

From repository root:

```bash
python -m examples.decorator_raise
python -m examples.decorator_random_raise
python -m examples.decorator_delay
python -m examples.decorator_delay_random
python -m examples.decorator_delay_random_norm
```

## Run tests

This project uses only the Python standard library for tests:

```bash
python -m unittest discover -s tests -v
```

## License

MIT (see `LICENSE`).
