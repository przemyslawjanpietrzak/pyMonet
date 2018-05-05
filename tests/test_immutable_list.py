from pymonet.immutable_list import ImmutableList


def test():
    assert ImmutableList(1).length == 1
    assert ImmutableList(1).unshift(0).length == 2