import textwrap
from patterna import match
import sys


# Test Class Matching
def test_class(point_class):
    Point = point_class  # Get Point class from fixture

    # Make sure Point is available in global scope
    globals()['Point'] = Point

    # The code to be evaluated - note we don't define Point here
    code = """
    def location(p):
        match p:
            case Point(x=0, y=0):
                result = "origin"
            case Point(x=x, y=y):
                result = f"Point({x},{y})"
            case _:
                result = "not a point"
        return result
    """

    # Create globals dict with Point
    global_dict = globals().copy()
    global_dict['Point'] = Point

    # Inject Point into the namespace for exec
    namespace = {'Point': Point}
    exec(textwrap.dedent(code), global_dict, namespace)

    # Use the match decorator with the location function
    location = match(namespace['location'], source=textwrap.dedent(code))

    # Test with Point instances
    assert location(Point(0, 0)) == "origin"
    assert location(Point(3, 4)) == "Point(3,4)"
    assert location("not a point") == "not a point"


# Test Positional Class Matching
def test_positional_class(point_class):
    Point = point_class  # Get Point class from fixture

    # Make sure Point is available in global scope
    globals()['Point'] = Point

    # The code to be evaluated - using the module-level Point class
    code = """
    def location(p):
        match p:
            case Point(0, 0):
                result = "origin"
            case Point(x, y):
                result = f"Point({x},{y})"
            case _:
                result = "not a point"
        return result
    """

    # Create globals dict with Point
    global_dict = globals().copy()
    global_dict['Point'] = Point

    # Inject Point into the namespace for exec
    namespace = {'Point': Point}
    exec(textwrap.dedent(code), global_dict, namespace)

    # Use the match decorator with the location function
    location = match(namespace['location'], source=textwrap.dedent(code))

    # Test with Point instances
    assert location(Point(0, 0)) == "origin"
    assert location(Point(3, 4)) == "Point(3,4)"