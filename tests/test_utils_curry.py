from hypothesis import given
from hypothesis.strategies import integers

from pymonet.utils import curry


@given(integers())
def test_curry_1_argument(integer1):

    @curry
    def fn(arg1):
        return arg1

    assert fn(integer1) == fn(integer1)


@given(integers(), integers())
def test_curry_2_arguments(integer1, integer2):

    @curry
    def fn(arg1, arg2):
        return arg1 + arg2

    assert fn(integer1)(integer2) == fn(integer1, integer2)


@given(integers(), integers(), integers())
def test_curry_3_arguments(integer1, integer2, integer3):

    @curry
    def fn(arg1, arg2, arg3):
        return arg1 + arg2 + arg3

    assert fn(integer1)(integer2)(integer3) == fn(integer1, integer2, integer3)
    assert fn(integer1, integer2)(integer3) == fn(integer1, integer2, integer3)
    assert fn(integer1)(integer2, integer3) == fn(integer1, integer2, integer3)


@given(integers(), integers(), integers(), integers())
def test_curry_4_arguments(integer1, integer2, integer3, integer4):

    @curry
    def fn(arg1, arg2, arg3, arg4):
        return arg1 + arg2 + arg3 + arg4

    assert fn(integer1)(integer2)(integer3)(integer4) == fn(integer1, integer2, integer3, integer4)
    assert fn(integer1, integer2, integer3)(integer4) == fn(integer1, integer2, integer3, integer4)
    assert fn(integer1, integer2)(integer3, integer4) == fn(integer1, integer2, integer3, integer4)
    assert fn(integer1)(integer2, integer3, integer4) == fn(integer1, integer2, integer3, integer4)
    assert fn(integer1, integer2)(integer3)(integer4) == fn(integer1, integer2, integer3, integer4)
    assert fn(integer1)(integer2, integer3, integer4) == fn(integer1, integer2, integer3, integer4)
