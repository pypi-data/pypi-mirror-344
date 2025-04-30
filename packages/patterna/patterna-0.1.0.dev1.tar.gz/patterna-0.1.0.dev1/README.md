# Patterna: Python Structural Pattern Matching for 3.7+

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/patterna)
![PyPI - License](https://img.shields.io/pypi/l/patterna)
![PyPI - Version](https://img.shields.io/pypi/v/patterna)

Patterna is a pure Python library that backports the structural pattern matching functionality (match/case statements) introduced in Python 3.10 to earlier Python versions (3.7 and above). It provides a decorator-based approach to enable pattern matching in your code without requiring Python 3.10.

<p style="text-align: center">
  <img src="https://raw.githubusercontent.com/saadmanrafat/patterna/480c4ac6ff6ef8390de18a69546d6ff39c5715ff/assets/patterna.svg" style="max-width: 100%; height: auto;" alt="">
</p>

## Features

Patterna implements nearly all pattern matching features from Python 3.10, including:

- **Literal patterns** (`case 1:`, `case "hello":`, etc.)
- **Wildcard patterns** (`case _:`)
- **Capture patterns** (`case x:`)
- **OR patterns** (`case "yes" | "y":`)
- **Sequence patterns** (`case [a, b]:`)
- **Sequence patterns with star unpacking** (`case [first, *rest]:`)
- **Mapping patterns** (`case {"key": value}:`)
- **Mapping patterns with rest** (`case {"name": name, **rest}:`)
- **Class patterns with positional and keyword arguments** (`case Point(x, y):`)
- **Guard clauses** (`case x if x > 0:`)
- **AS patterns** (`case [a, b] as lst:`)
- **Named constants** (`case True:`, `case None:`)
- **Dotted names** (`case math.pi:`)
- **Callable patterns** (`case int():`, `case str():`)
- **Nested patterns** (`case [{"name": name, "data": [a, b]}]:`)

## Installation

```bash
pip install patterna
```

## Usage

Import the `match` decorator and apply it to functions that use pattern matching:

```python
from patterna import match

@match
def process_data(data):
    match data:
        case {"type": "point", "x": x, "y": y}:
            return f"Point at ({x}, {y})"
        case [a, b, *rest]:
            return f"Sequence starting with {a} and {b}, followed by {len(rest)} more items"
        case str() as s if len(s) > 10:
            return f"Long string: {s[:10]}..."
        case _:
            return "No match"

# Use the function normally
result = process_data({"type": "point", "x": 10, "y": 20})  # "Point at (10, 20)"
result = process_data([1, 2, 3, 4, 5])  # "Sequence starting with 1 and 2, followed by 3 more items"
result = process_data("Hello, world!")  # "Long string: Hello, wor..."
result = process_data(42)  # "No match"
```

## Examples

### Basic Pattern Matching

```python
from patterna import match

@match
def describe(value):
    match value:
        case 0:
            return "Zero"
        case 1:
            return "One"
        case _:
            return f"Something else: {value}"

print(describe(0))  # "Zero"
print(describe(1))  # "One"
print(describe(42))  # "Something else: 42"
```

### Sequence Patterns

```python
from patterna import match

@match
def process_list(items):
    match items:
        case []:
            return "Empty list"
        case [single]:
            return f"Single item: {single}"
        case [first, second]:
            return f"Two items: {first} and {second}"
        case [first, *rest]:
            return f"Multiple items, starting with {first}, followed by {len(rest)} more"
        case _:
            return "Not a list"

print(process_list([]))  # "Empty list"
print(process_list([42]))  # "Single item: 42"
print(process_list([1, 2]))  # "Two items: 1 and 2"
print(process_list([1, 2, 3, 4]))  # "Multiple items, starting with 1, followed by 3 more"
print(process_list("hello"))  # "Not a list"
```

### Dictionary Patterns

```python
from patterna import match

@match
def process_person(person):
    match person:
        case {"name": name, "age": age} if age >= 18:
            return f"{name} is an adult"
        case {"name": name, "age": age}:
            return f"{name} is a minor"
        case {"name": name, **rest}:
            return f"{name} has incomplete information"
        case _:
            return "Invalid person data"

print(process_person({"name": "Alice", "age": 30}))  # "Alice is an adult"
print(process_person({"name": "Bob", "age": 15}))  # "Bob is a minor"
print(process_person({"name": "Charlie"}))  # "Charlie has incomplete information"
print(process_person({"age": 25}))  # "Invalid person data"
```

### Class Patterns

```python
from patterna import match

class Point:
    __match_args__ = ("x", "y")
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

@match
def describe_point(point):
    match point:
        case Point(0, 0):
            return "Origin"
        case Point(0, y):
            return f"On y-axis at y={y}"
        case Point(x, 0):
            return f"On x-axis at x={x}"
        case Point(x, y) if x == y:
            return f"On diagonal at x=y={x}"
        case Point(x=x, y=y):
            return f"Point at ({x}, {y})"
        case _:
            return "Not a point"

print(describe_point(Point(0, 0)))  # "Origin"
print(describe_point(Point(0, 5)))  # "On y-axis at y=5"
print(describe_point(Point(5, 0)))  # "On x-axis at x=5" 
print(describe_point(Point(3, 3)))  # "On diagonal at x=y=3"
print(describe_point(Point(3, 4)))  # "Point at (3, 4)"
print(describe_point("not a point"))  # "Not a point"
```


## Limitations

While Patterna aims to implement most of Python 3.10's pattern matching features, there are some limitations:

1. **Performance**: The library uses runtime AST parsing and evaluation, which is slower than Python 3.10's native implementation.

2. **Syntax Restrictions**: The Python parser in versions before 3.10 will reject certain syntax constructs, so you should only use the match/case syntax inside functions decorated with `@match`.

3. **Error Messages**: Error messages may differ from those in native pattern matching.

4. **Class Resolution in Complex Nested Patterns**: For complex nested class patterns, using guard clauses with `isinstance()` checks may be more reliable.

## License

This project is licensed under the MIT License - see the LICENSE file for details.