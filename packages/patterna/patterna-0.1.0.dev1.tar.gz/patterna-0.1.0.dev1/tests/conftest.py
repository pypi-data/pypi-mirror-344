import pytest
import sys

# Define Point class at module level for use in all tests
class Point:
    __match_args__ = ("x", "y")
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Add Point to globals() so it's available everywhere
globals()['Point'] = Point
sys.modules['tests.point'] = type('PointModule', (), {'Point': Point})

@pytest.fixture
def point_class():
    """Fixture to provide the Point class to tests."""
    return Point