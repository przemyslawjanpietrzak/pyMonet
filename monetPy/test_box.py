import pytest
from monetPy.box import Box


def test():
    input = 'input'
    box = Box(input)
    assert box\
        .map(lambda value: '{}_suffix'.format(value))\
        .fold(lambda value: value) == 'input_suffix'
