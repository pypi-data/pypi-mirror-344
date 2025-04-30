import textwrap
from patterna import match

# Test Sequence Matching
def test_sequence():
    code = """
    def pair(x):
        match x:
            case [a, b]:
                result = a + b
            case _:
                result = 0
        return result
    """

    namespace = {}
    exec(textwrap.dedent(code), globals(), namespace)
    pair = match(namespace['pair'], source=textwrap.dedent(code))

    assert pair([1, 2]) == 3
    assert pair([1]) == 0
    assert pair("not a list") == 0


# Test Star Patterns in Sequences
def test_star_pattern():
    code = """
    def process_list(x):
        match x:
            case [first, *middle, last]:
                result = (first, middle, last)
            case [first, *rest]:
                result = (first, rest, None)
            case []:
                result = (None, [], None)
            case _:
                result = None
        return result
    """

    namespace = {}
    exec(textwrap.dedent(code), globals(), namespace)
    process_list = match(namespace['process_list'], source=textwrap.dedent(code))

    assert process_list([1, 2, 3, 4, 5]) == (1, [2, 3, 4], 5)
    assert process_list([1, 2]) == (1, [], 2)
    assert process_list([1]) == (1, [], None)
    assert process_list([]) == (None, [], None)
    assert process_list("not a list") is None


# Test AS Patterns
def test_as_pattern():
    code = """
    def process(val):
        match val:
            case [a, b] as lst:
                result = (a, b, len(lst))
            case {"x": x, "y": y} as d:
                result = (x, y, len(d))
            case _:
                result = None
        return result
    """

    namespace = {}
    exec(textwrap.dedent(code), globals(), namespace)
    process = match(namespace['process'], source=textwrap.dedent(code))

    assert process([1, 2]) == (1, 2, 2)
    assert process({"x": 1, "y": 2, "z": 3}) == (1, 2, 3)
    assert process("other") is None


# Test Guards with Assignments
def test_guards_with_assignment():
    code = """
    def process(val):
        match val:
            case [a, b] if (a + b) > 5:
                result = a + b
            case _:
                result = -1
        return result
    """

    namespace = {}
    exec(textwrap.dedent(code), globals(), namespace)
    process = match(namespace['process'], source=textwrap.dedent(code))

    assert process([3, 4]) == 7  # 3 + 4 > 5, so should match
    assert process([1, 2]) == -1  # 1 + 2 < 5, so shouldn't match
    assert process("other") == -1