import textwrap
from patterna import match


# Test Nested Patterns
def test_nested_patterns(point_class):
    Point = point_class  # Get Point class from fixture

    # Make sure Point is available in global scope
    globals()['Point'] = Point

    # The code to be evaluated - using the Point class
    code = """
    def nested(val):
        match val:
            case [{"name": name, "points": [Point(x, y), *_]}]:
                result = (name, x, y)
            case [{"id": id, "data": {"value": value}}]:
                result = (id, value)
            case _:
                result = None
        return result
    """

    # Create globals dict with Point
    global_dict = globals().copy()
    global_dict['Point'] = Point

    # Inject Point into the namespace for exec
    namespace = {'Point': Point}
    exec(textwrap.dedent(code), global_dict, namespace)

    # Use the match decorator with the nested function
    nested = match(namespace['nested'], source=textwrap.dedent(code))

    # Test with nested patterns including Point instances
    assert nested([{"name": "Alice", "points": [Point(1, 2), Point(3, 4)]}]) == ("Alice", 1, 2)
    assert nested([{"id": 42, "data": {"value": 100}}]) == (42, 100)
    assert nested([{"wrong": "format"}]) is None


# Test Complex Nested Patterns with Guard
def test_complex_nested_patterns(point_class):
    Point = point_class  # Get Point class from fixture

    # Make sure Point is available in global scope
    globals()['Point'] = Point

    # Use a more explicit approach for nested class patterns
    code = """
    def nested(val):
        match val:
            case [{"name": name, "points": points}] if points and isinstance(points[0], Point) and len(points) > 0:
                result = (name, points[0].x, points[0].y)
            case [{"id": id, "data": {"value": value}}]:
                result = (id, value)
            case _:
                result = None
        return result
    """

    # Create globals dict with Point
    global_dict = globals().copy()
    global_dict['Point'] = Point

    # Make Point available in the namespace
    namespace = {'Point': Point}
    exec(textwrap.dedent(code), global_dict, namespace)

    # Use the match decorator with source
    nested = match(namespace['nested'], source=textwrap.dedent(code))

    # Test with Point objects
    assert nested([{"name": "Alice", "points": [Point(1, 2), Point(3, 4)]}]) == ("Alice", 1, 2)
    assert nested([{"id": 42, "data": {"value": 100}}]) == (42, 100)
    assert nested([{"wrong": "format"}]) is None


# Test with Multiple Match Statements
def test_multiple_match():
    code = """
    def process(val1, val2):
        match val1:
            case int() as x:
                a = x * 2
            case _:
                a = 0

        match val2:
            case str() as s:
                b = len(s)
            case _:
                b = 0

        return a + b
    """

    namespace = {}
    exec(textwrap.dedent(code), globals(), namespace)
    process = match(namespace['process'], source=textwrap.dedent(code))

    assert process(10, "hello") == 20 + 5
    assert process("not an int", []) == 0
    assert process(5, [1, 2, 3]) == 10