import pytest
from monetPy.box import Box


def test():
    box = Box(42)
    assert box.map(lambda value: value + 1) == Box(43)
