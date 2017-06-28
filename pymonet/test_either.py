import pytest
from pymonet.either import Either, Left, Right
from pymonet.utils import identity


def either_operation(either):
    return either\
        .map(lambda value: 'prefix_{}'.format(value), lambda value: value + 1)\
        .fold(identity, identity)


def test_left_either():
    left = Left('some_string')
    result = either_operation(left)
    assert result == 'prefix_some_string'


def test_right_either():
    right = Right(42)
    result = either_operation(right)
    assert result == 43
