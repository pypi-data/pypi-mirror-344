# patterna

[![PyPI](https://img.shields.io/pypi/v/patterna.svg)](https://pypi.org/project/patterna/)
[![Python](https://img.shields.io/badge/python-3.7%2C%203.8%2C%203.9%2C%203.10%2C%203.11%2C%203.12-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Pure Python library for simple pattern matching on `dicts`, `lists`, `tuples`, and `objects` — inspired by Python 3.10 `match/case`, but portable to Python 3.7+.


<p style="text-align: center">
  <img src="assets/patterna.svg" style="max-width: 100%; height: auto;" alt="">
</p>


## Usage

```python3
from patterna import match

@match
def classify(animal):
    case {"type": "cat", "age": lambda age: age > 2}:
        return "Adult Cat"
    
    case {"type": "cat"}:
        return "Kitten"
    
    case {"type": "dog"}:
        return "Doggo"
    
    case _:
        return "Unknown animal"
```
### Error Handling
If no case matches and no `case _:` is provided, `patterna` raises a `ValueError`.

```python3
from patterna import match

@match
def check(value):
    case 1:
        return "One"

# check(2) → raises ValueError("No pattern matched")
```

## Features
* Simple and readable pattern matching
* Supports dictionaries, tuples, lists, types, and callables
* Works on Python 3.7+
* Zero dependencies
* Lightweight

## Installation
```bash
pip install patterna
```

