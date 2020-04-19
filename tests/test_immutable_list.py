import pytest

from pymonet.immutable_list import ImmutableList


def test_eq():
    assert len(ImmutableList.empty()) == 0
    assert len(ImmutableList.of(1)) == 1
    assert len(ImmutableList.of(1).unshift(0)) == 2


def test_immutable():
    lst = ImmutableList(1)
    lst2 = lst.append(2)
    assert lst is not lst2


def test_to_list():
    assert ImmutableList(1).unshift(0).to_list() == [0, 1]


def test_of():
    assert ImmutableList.of(1, 2, 3, 4).to_list() == [1, 2, 3, 4]


def test_map():
    assert ImmutableList.of(1, 2, 3, 4).map(lambda item: item + 1) == ImmutableList.of(2, 3, 4, 5)


def test_filter():
    assert ImmutableList.of(1, 2, 3, 4).filter(lambda item: item % 2 == 0) == ImmutableList.of(2, 4)


def test_empty_filter():
    assert ImmutableList.of(1, 2, 3, 4).filter(lambda item: False) == ImmutableList.empty()


def test_plus_operator():
    assert ImmutableList.of(1, 2) + ImmutableList.of(3, 4) == ImmutableList.of(1, 2, 3, 4)


def test_plus_operator_exception():
    with pytest.raises(ValueError):
        ImmutableList.of(0) + [1]


def test_find_positive():
    assert ImmutableList.of(1, 2, 3, 4).find(lambda item: item % 2 == 0) == 2


def test_find_negative():
    assert ImmutableList.of(1, 2, 3, 4).find(lambda item: item < 0) is None


def test_unshift():
    assert ImmutableList.of(1, 2).unshift(0) == ImmutableList.of(0, 1, 2)


def test_append():
    assert ImmutableList.of(1, 2).append(3) == ImmutableList.of(1, 2, 3)

def test_reduce_addition():
    assert ImmutableList.empty().reduce(lambda acc, curr: acc + curr, 0) == 0
    assert ImmutableList.of(1).reduce(lambda acc, curr: acc + curr, 0) == 1
    assert ImmutableList.of(1, 2).reduce(lambda acc, curr: acc + curr, 0) == 3
    assert ImmutableList.of(1, 2, 3).reduce(lambda acc, curr: acc + curr, 0) == 6

def test_reduce_multiplication():
    assert ImmutableList.empty().reduce(lambda acc, curr: acc * curr, 1) == 1
    assert ImmutableList.of(1).reduce(lambda acc, curr: acc * curr, 1) == 1
    assert ImmutableList.of(1, 2).reduce(lambda acc, curr: acc * curr, 1) == 2
    assert ImmutableList.of(1, 2, 3).reduce(lambda acc, curr: acc * curr, 1) == 6