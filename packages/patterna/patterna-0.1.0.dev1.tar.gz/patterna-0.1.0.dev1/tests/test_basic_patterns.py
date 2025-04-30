import textwrap
import math
from patterna import match

# Test Literal Matching
def test_literal():
    code = """
    def f(x):
        match x:
            case 1:
                result = "one"
            case _:
                result = "default"
        return result
    """

    # Create a local namespace
    namespace = {}

    # Execute the function definition
    exec(textwrap.dedent(code), globals(), namespace)

    # Get the function and decorate it with properly dedented source
    f = match(namespace['f'], source=code)

    # Test the function
    assert f(1) == "one"
    assert f(42) == "default"


# Test Named Constants
def test_named_constants():
    code = """
    PI = 3.14159

    def f(x):
        match x:
            case 3.14159:  # Using the value directly instead of PI to avoid syntax error
                result = "pi"
            case True:
                result = "true"
            case False:
                result = "false"
            case None:
                result = "none"
            case _:
                result = "other"
        return result
    """

    namespace = {'PI': 3.14159}
    exec(textwrap.dedent(code), globals(), namespace)
    f = match(namespace['f'], source=textwrap.dedent(code))

    assert f(3.14159) == "pi"
    assert f(True) == "true"
    assert f(False) == "false"
    assert f(None) == "none"
    assert f(42) == "other"


# Test Dotted Names
def test_dotted_names():
    code = """
    import math

    def f(x):
        match x:
            case math.pi:
                result = "pi"
            case math.e:
                result = "e"
            case _:
                result = "other"
        return result
    """

    namespace = {'math': math}
    exec(textwrap.dedent(code), globals(), namespace)
    f = match(namespace['f'], source=textwrap.dedent(code))

    assert f(math.pi) == "pi"
    assert f(math.e) == "e"
    assert f(42) == "other"


# Test Callable Matching (int, str)
def test_callable_matching():
    code = """
    def f(x):
        match x:
            case int():
                result = "int"
            case str():
                result = "str"
            case _:
                result = "other"
        return result
    """

    namespace = {}
    exec(textwrap.dedent(code), globals(), namespace)
    f = match(namespace['f'], source=textwrap.dedent(code))

    assert f(1) == "int"
    assert f("hello") == "str"
    assert f([1, 2]) == "other"


# Test Guards
def test_guard():
    code = """
    def size(n):
        match n:
            case x if x > 10:
                result = "big"
            case _:
                result = "small"
        return result
    """

    namespace = {}
    exec(textwrap.dedent(code), globals(), namespace)
    size = match(namespace['size'], source=textwrap.dedent(code))

    assert size(5) == "small"
    assert size(20) == "big"


# Test OR Patterns
def test_or():
    code = """
    def yesno(val):
        match val:
            case "yes" | "y":
                result = "affirmative"
            case "no" | "n":
                result = "negative"
            case _:
                result = "unknown"
        return result
    """

    namespace = {}
    exec(textwrap.dedent(code), globals(), namespace)
    yesno = match(namespace['yesno'], source=textwrap.dedent(code))

    assert yesno("yes") == "affirmative"
    assert yesno("y") == "affirmative"
    assert yesno("n") == "negative"
    assert yesno("hmm") == "unknown"