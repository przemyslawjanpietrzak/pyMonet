from pymonet.immutable_list import ImmutableList


def test():
    assert ImmutableList(1).length == 1
    assert ImmutableList(1).unshift(0).length == 2

def test_to_list():
    assert ImmutableList(1).unshift(0).to_list() == [0,1]

def test_of():
    assert ImmutableList.of(1,2,3,4).to_list() == [1,2,3,4]