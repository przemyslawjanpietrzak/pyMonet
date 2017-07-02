import pytest

from pymonet.either import Either, Left, Right
from pymonet.utils import identity


def test_either_eq_operator_should_compare_values():

    assert Right(42) == Right(42)
    assert Right(42) != Right(43)

    assert Left(42) == Left(42)
    assert Left(42) != Left(43)

    assert Right(42) != Left(42)


def test_mapper_should_be_applied_only_on_current_value():

    assert Left(42).map(lambda value: value + 1, identity) == Left(43)
    assert Right(42).map(identity, lambda value: value + 1) == Right(43)


def test_is_right_should_return_suitable_value():

    assert Right(42).is_right()
    assert not Left(42).is_right()


def test_is_left_should_return_suitable_value():
    assert Left(42).is_left()
    assert not Right(42).is_left()


def test_fold_should_be_applied_only_on_current_value_and_return_value():

    assert Left(42).fold(lambda value: value + 1, identity) == 43
    assert Right(42).fold(identity, lambda value: value + 1) == 43
